"""Descriptor-relative implementation of the existing all-file key-set predicate.

No live entrypoint, discovery outside the supplied root, or authorization logic.
Empty directories remain valid, as in the original rglob/is_file predicate.
"""
import os
from pathlib import Path
import stat
import hashlib
import json
from datetime import datetime, timezone


class MembershipReject(RuntimeError):
    pass


def need(ok, code):
    if not ok:
        raise MembershipReject(code)


def key(value):
    need(type(value) is str and value and '\x00' not in value and
         not value.startswith('/') and all(p not in ('', '.', '..') for p in value.split('/')),
         'NONCANONICAL_MEMBER_KEY')
    return value


def signature(s):
    return (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_uid,s.st_gid,
            s.st_size,s.st_mtime_ns,s.st_ctime_ns)


def _canonical_metadata(value):
    # Same canonical JSON convention as trusted_stage.staging_v1.canonical.
    return (json.dumps(value,sort_keys=True,separators=(',',':'),
                       ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')


class MetadataObservation:
    """Safe public bytes plus potentially sensitive, private in-process metadata.

    There is no key-export/serialization operation. Arbitrary trusted Python
    code can inspect private attributes; this is an output boundary, not an OS
    sandbox or a new authority mechanism. No metadata is persisted by this class.
    """
    __slots__=('_public_bytes','_observed_entries')

    def __init__(self,public_bytes,observed_entries):
        self._public_bytes=public_bytes
        self._observed_entries=observed_entries

    @property
    def public_bytes(self):
        return self._public_bytes

    def __repr__(self):
        return 'MetadataObservation(PRIVATE_METADATA_NOT_EXPORTED)'

    def __reduce_ex__(self,protocol):
        raise MembershipReject('METADATA_PRIVATE_EXPORT_FORBIDDEN')


class Membership:
    def __init__(self, root, expected, *, _metadata_only=False,
                 expected_directories=None, selected_body_keys=None, body_read_budget=None):
        self.root=Path(root).absolute()
        need(type(_metadata_only) is bool,'INVALID_METADATA_MODE')
        self._metadata_only=_metadata_only
        if _metadata_only:
            need(expected is None,'METADATA_EXPECTED_MEMBERS_FORBIDDEN')
            self.expected=None
        else:
            values=list(expected)
            need(len(values)==len(set(values)), 'DUPLICATE_MEMBER_KEY')
            self.expected=frozenset(key(v) for v in values)
        self.expected_directories=None
        if expected_directories is not None:
            need(not _metadata_only,'INVALID_METADATA_MODE')
            directories=list(expected_directories)
            need(len(directories)==len(set(directories)), 'DUPLICATE_MEMBER_KEY')
            self.expected_directories=frozenset(key(v) for v in directories)
            need(not(self.expected & self.expected_directories),'MEMBER_SET_MISMATCH')
        self.selected_body_keys=None
        self.body_read_budget=None
        if selected_body_keys is not None or body_read_budget is not None:
            need(not _metadata_only and selected_body_keys is not None and
                 type(body_read_budget) is int and body_read_budget>=0,'MEMBER_READ_BUDGET')
            selected=list(selected_body_keys)
            need(len(selected)==len(set(selected)),'DUPLICATE_MEMBER_KEY')
            self.selected_body_keys=frozenset(key(v) for v in selected)
            need(self.selected_body_keys<=self.expected,'UNDECLARED_BODY_READ')
            self.body_read_budget=body_read_budget
        self.fds=[];self.anchor=[];self.directories={};self.files={}
        self.body_read_paths=[];self.body_read_bytes=0;self.enumerated_directories=0

    @classmethod
    def observe_metadata(cls,root):
        """Discover namespace metadata only, with no expected declaration.

        This callable grants no live access permission. The complete observed
        table remains private in-process metadata; only public_bytes is the
        qualified outward receipt. Hashes identify metadata, never file bytes
        or an independently accepted authoritative declaration.
        """
        try:
            need(type(root) is str or type(root) is type(Path('/')),'METADATA_ROOT_INVALID')
            root=Path(root)
            need(root.is_absolute() and '..' not in root.parts,'METADATA_ROOT_INVALID')
            started=datetime.now(timezone.utc).isoformat()
            with cls(root,None,_metadata_only=True) as scope:
                entries=[]
                for name,(_,_,identity) in scope.files.items():
                    entries.append((name,'REGULAR_FILE',identity))
                for name,(_,identity,_) in scope.directories.items():
                    if name:entries.append((name,'DIRECTORY',identity))
                entries=tuple(sorted(entries))
                keys=tuple(item[0] for item in entries)
                root_signature=scope.anchor[-1][2]
                root_identity=dict(zip(('device','inode','mode','nlink','uid','gid',
                                        'size','mtime_ns','ctime_ns'),root_signature))
                member_count=len(scope.files)
                directory_count=len(scope.directories)-1
                need(not scope.body_read_paths,'METADATA_BODY_READ_FORBIDDEN')
            # __exit__ has completed the original ancestor and namespace rescan.
            identity={
                'schema':'QTRP_OBSERVED_NAMESPACE_METADATA_V1',
                'scope':'OBSERVED_NAMESPACE_ONLY__NOT_AUTHORITATIVE',
                'root_identity':root_identity,
                'key_set_sha256':hashlib.sha256(_canonical_metadata(keys)).hexdigest(),
                'entry_metadata_sha256':hashlib.sha256(_canonical_metadata(entries)).hexdigest(),
                'entry_count':len(entries),'member_count':member_count,
                'directory_count':directory_count,
                'entry_types':{'REGULAR_FILE':member_count,'DIRECTORY':directory_count},
                'classification_policy':'B_C_UNKNOWN_ALL_INCLUDED__CONTENT_UNINSPECTED',
                'unknown_access_classification_count':len(entries),
                'namespace_stability':'VERIFIED_DURING_OBSERVATION_INTERVAL',
                'member_body_reads':0,'scientific_content_hashes':0,'scientific_parsing':0,
                'authoritative_declaration':False,'real_authority':False}
            receipt={**identity,
                'receipt_identity_sha256':hashlib.sha256(_canonical_metadata(identity)).hexdigest(),
                'observation_started_utc':started,
                'observation_finished_utc':datetime.now(timezone.utc).isoformat()}
            return MetadataObservation(_canonical_metadata(receipt),entries)
        except Exception as exc:
            codes={'METADATA_ROOT_INVALID','INVALID_METADATA_MODE','METADATA_EXPECTED_MEMBERS_FORBIDDEN',
                'METADATA_BODY_OPEN_FORBIDDEN','METADATA_BODY_READ_FORBIDDEN',
                'UNSAFE_ROOT','PATH_SUBSTITUTION','DIRECTORY_ALIAS','DIRECTORY_CHANGED',
                'SYMLINK_MEMBER','INVALID_OBJECT_TYPE','MULTILINK_MEMBER',
                'MEMBER_IDENTITY_CHANGED','ROOT_OR_ANCESTOR_CHANGED','NONCANONICAL_MEMBER_KEY',
                'METADATA_AMBIGUOUS_ENUMERATION'}
            code=exc.args[0] if type(exc) is MembershipReject and len(exc.args)==1 else None
            raise MembershipReject(code if code in codes else 'METADATA_OBSERVATION_FAILED') from None

    def _open(self,name,flags,parent=None):
        if self._metadata_only:
            need(flags&os.O_DIRECTORY and flags&os.O_NOFOLLOW and
                 not flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND),
                 'METADATA_BODY_OPEN_FORBIDDEN')
        fd=os.open(name,flags|os.O_CLOEXEC,dir_fd=parent)
        self.fds.append(fd)
        return fd

    def __enter__(self):
        try:
            components=self.root.parts
            need(components[0]=='/' and all(p not in ('','.','..') for p in components[1:]), 'UNSAFE_ROOT')
            flags=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW
            fd=self._open('/',flags)
            self.anchor.append(('/',fd,signature(os.fstat(fd))))
            absolute=''
            for name in components[1:]:
                absolute+='/'+name
                before=os.stat(name,dir_fd=fd,follow_symlinks=False)
                need(stat.S_ISDIR(before.st_mode) and not stat.S_ISLNK(before.st_mode),'UNSAFE_ROOT')
                child=self._open(name,flags,fd)
                need(signature(os.fstat(child))==signature(before),'PATH_SUBSTITUTION')
                self.anchor.append((absolute,child,signature(before)))
                fd=child
            self.root_fd=fd
            self._scan(initial=True)
            if not self._metadata_only:
                need(set(self.files)==self.expected,'MEMBER_SET_MISMATCH')
            if self.expected_directories is not None:
                need(set(self.directories)-{''}==self.expected_directories,
                     'DIRECTORY_CHANGED')
            return self
        except BaseException:
            self.close()
            raise

    def _scan(self,initial):
        queue=[('',self.root_fd)]
        observed={};directory_names={}
        seen_directories=set()
        while queue:
            relative,fd=queue.pop()
            s=os.fstat(fd);inode=(s.st_dev,s.st_ino)
            need(inode not in seen_directories,'DIRECTORY_ALIAS')
            seen_directories.add(inode)
            names=sorted(os.listdir(fd));self.enumerated_directories+=1
            if self._metadata_only:
                need(len(names)==len(set(names)),'METADATA_AMBIGUOUS_ENUMERATION')
            directory_names[relative]=tuple(names)
            if initial:self.directories[relative]=(fd,signature(s),tuple(names))
            else:
                need(relative in self.directories and self.directories[relative][1:]==(signature(s),tuple(names)),
                     'DIRECTORY_CHANGED')
            for name in names:
                item=key(relative+'/'+name if relative else name)
                if self.expected_directories is not None:
                    # Reject undeclared entries before stat/open or descent.
                    need(item in self.expected or item in self.expected_directories,
                         'UNEXPECTED_MEMBER')
                before=os.stat(name,dir_fd=fd,follow_symlinks=False)
                need(not stat.S_ISLNK(before.st_mode),'SYMLINK_MEMBER')
                if stat.S_ISDIR(before.st_mode):
                    if self.expected_directories is not None:
                        need(item in self.expected_directories,'INVALID_OBJECT_TYPE')
                    if initial:
                        child=self._open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,fd)
                        need(signature(before)==signature(os.fstat(child)),'PATH_SUBSTITUTION')
                    else:
                        need(item in self.directories,'DIRECTORY_CHANGED')
                        child=self.directories[item][0]
                        need(signature(before)==signature(os.fstat(child)),'PATH_SUBSTITUTION')
                    queue.append((item,child))
                else:
                    need(stat.S_ISREG(before.st_mode),'INVALID_OBJECT_TYPE')
                    need(before.st_nlink==1,'MULTILINK_MEMBER')
                    if not self._metadata_only:
                        need(item in self.expected,'UNEXPECTED_MEMBER')
                    observed[item]=(fd,name,signature(before))
        if initial:self.files=observed
        else:need(observed==self.files,'MEMBER_IDENTITY_CHANGED')

    @property
    def paths(self):
        need(not self._metadata_only,'METADATA_BODY_READ_FORBIDDEN')
        return {name:self.root/name for name in self.files}

    def read(self,path, *, max_bytes=None):
        need(not self._metadata_only,'METADATA_BODY_READ_FORBIDDEN')
        path=Path(path)
        try:name=str(path.relative_to(self.root))
        except ValueError:raise MembershipReject('UNDECLARED_BODY_READ') from None
        key(name);need(name in self.files,'UNDECLARED_BODY_READ')
        if self.selected_body_keys is not None:
            need(name in self.selected_body_keys,'UNDECLARED_BODY_READ')
        parent,leaf,before=self.files[name]
        now=os.stat(leaf,dir_fd=parent,follow_symlinks=False)
        need(signature(now)==before,'MEMBER_IDENTITY_CHANGED')
        if max_bytes is not None:
            need(type(max_bytes) is int and max_bytes>=0 and now.st_size<=max_bytes,
                 'MEMBER_READ_BUDGET')
        if self.body_read_budget is not None:
            need(max_bytes is not None and
                 now.st_size<=self.body_read_budget-self.body_read_bytes,
                 'MEMBER_READ_BUDGET')
        fd=self._open(leaf,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,parent)
        need(signature(os.fstat(fd))==before,'PATH_SUBSTITUTION')
        # Default historical behavior is unchanged. Selective verification never
        # performs the size+1 probe: post-read descriptor identity detects growth.
        chunks=[];left=now.st_size+1 if max_bytes is None else now.st_size
        while left:
            block=os.read(fd,min(left,65536))
            if not block:break
            chunks.append(block);left-=len(block);self.body_read_bytes+=len(block)
        raw=b''.join(chunks)
        need(len(raw)==now.st_size and signature(os.fstat(fd))==before,'MEMBER_CHANGED_DURING_READ')
        self.body_read_paths.append(name)
        return raw

    def declared_artifact(self,folder,name):
        need(not self._metadata_only,'METADATA_BODY_READ_FORBIDDEN')
        need(type(name) is str and name not in ('','.','..') and Path(name).name==name,
             'UNSAFE_DYNAMIC_ARTIFACT')
        target=Path(folder)/name
        try:relative=str(target.relative_to(self.root))
        except ValueError:raise MembershipReject('UNDECLARED_DYNAMIC_ARTIFACT') from None
        key(relative)
        need(relative in self.files,'UNDECLARED_DYNAMIC_ARTIFACT')
        return target

    def finish(self):
        for path,fd,before in self.anchor:
            need(signature(os.fstat(fd))==before and signature(os.stat(path,follow_symlinks=False))==before,
                 'ROOT_OR_ANCESTOR_CHANGED')
        self._scan(initial=False)

    def close(self):
        for fd in reversed(self.fds):os.close(fd)
        self.fds=[]

    def __exit__(self,kind,value,tb):
        try:
            if kind is None:self.finish()
        finally:self.close()
        return False

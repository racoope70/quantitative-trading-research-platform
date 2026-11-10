"""Generate fresh synthetic inputs and refresh the existing pinned NP closure."""
import ast,hashlib,importlib.util,json,re,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)+'\n').encode()
sys.path[:0]=[str(ROOT/'candidate'),str(ROOT/'accepted')]
import firewall_v2 as firewall
from real_candidate import release_v1
spec=importlib.util.spec_from_file_location('fresh_partition',ROOT/'accepted/accepted_recovery/reference/v6_accepted/partition_contract_nonproduction_v1.py')
partition=importlib.util.module_from_spec(spec);spec.loader.exec_module(partition)
fixture=ROOT/'candidate/dependencies/synthetic_fixture'
if not fixture.exists():
    fixture.mkdir()
    evidence=[]
    for pos in range(1501,2001):
        row={key:None for key in firewall.EVIDENCE_KEYS}
        row.update(canonical_source_identity=sha(('MODEL_B_NEW_SYNTHETIC_'+str(pos)).encode()),
            authorized_population_position=pos,body_available=False,schema_version='FRESH_SYNTHETIC_ONLY',batch_id='SYNTHETIC')
        evidence.append(row)
    reasons={d:[{'reason_code':'U1_AUTHORITATIVE_BODY_NOT_AVAILABLE','rank':1,'category':'SYNTHETIC_ONLY'}]
        for d in partition.v3.ALLOWED_DISPOSITIONS}
    (fixture/'neutral_semantic_evidence.jsonl').write_bytes(b''.join(canonical(r) for r in evidence))
    (fixture/'evidence.json').write_bytes(canonical(evidence))
    (fixture/'reason_precedence_v2.json').write_bytes(canonical(reasons))
    (fixture/'full_s04_fixture').mkdir()
    (fixture/'full_s04_fixture/semantic_rule_v2.json').write_bytes(canonical({'fixture':'FRESH_MODEL_B_SYNTHETIC_ONLY'}))
    (fixture/'partition.json').write_bytes(canonical(partition.build_partition_manifest(evidence,25,'9'*64)))

# The accepted engine reads the list representation through its reason loader;
# the accepted validator adapter takes the already normalized reason map.
normalized=fixture/'reason_normalized.json'
if not normalized.exists():
    reasons=json.loads((fixture/'reason_precedence_v2.json').read_bytes())
    normalized.write_bytes(canonical({d:{row['reason_code']:{'rank':row['rank'],'category':row['category']}
        for row in entries} for d,entries in reasons.items()}))

# Update only the prospective capture pin, not the historical predecessor.
p=ROOT/'candidate/recovery_compatibility_bounded_v4.json'
binding=json.loads(p.read_bytes())
binding['prospective_source_sha256']['real_candidate/capture_v1.py']=sha((ROOT/'candidate/real_candidate/capture_v1.py').read_bytes())
p.write_bytes(canonical(binding));binding_sha=sha(p.read_bytes())
p=ROOT/'candidate/recovery_bounded_v4.py';text=p.read_text()
text,n=re.subn(r"^COMPATIBILITY_BINDING_SHA256 = '[0-9a-f]{64}'$",'COMPATIBILITY_BINDING_SHA256 = '+repr(binding_sha),text,flags=re.M);assert n==1
p.write_text(text)
p=ROOT/'candidate/real_candidate/checkpoint_v1.py';text=p.read_text()
text,n=re.subn(r"^PHASE_RECOVERY_SOURCE_SHA256 = '[0-9a-f]{64}'$",'PHASE_RECOVERY_SOURCE_SHA256 = '+repr(sha((ROOT/'candidate/recovery_bounded_v4.py').read_bytes())),text,flags=re.M);assert n==1
p.write_text(text)
descriptor=canonical(release_v1.make_descriptor(ROOT))
(ROOT/release_v1.MANIFEST_FILE).write_bytes(descriptor)
(ROOT/release_v1.PIN_FILE).write_text(sha(descriptor)+'\n')
closure={p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for folder in ('accepted','candidate')
    for p in (ROOT/folder).rglob('*') if p.is_file()}
p=ROOT/'composition.py';text=p.read_text()
text=text.replace("_B53_ENGINEERING_ROOT = Path('/private/tmp/QTRP_BATCH0004_C06_B53_OS_SEPARATION_HANDOFF_NP_V1')",'_B53_ENGINEERING_ROOT = Path('+repr(str(ROOT))+')')
lines=text.splitlines()
for i,line in enumerate(lines):
    if line.startswith(' _NONPRODUCTION_SOURCE_CLOSURE = '):lines[i]=' _NONPRODUCTION_SOURCE_CLOSURE = '+repr(closure)
    elif line.startswith(' RELEASE_SHA = '):lines[i]=' RELEASE_SHA = '+repr(sha(descriptor))
    elif line.startswith(' RECOVERY_SHA = '):lines[i]=' RECOVERY_SHA = '+repr(closure['candidate/recovery_bounded_v4.py'])
    elif line.startswith(' RECOVERY_BINDING_SHA = '):lines[i]=' RECOVERY_BINDING_SHA = '+repr(binding_sha)
    elif line.startswith(' SOURCE_SHA256 = '):
        old=ast.literal_eval(line.split('=',1)[1].strip())
        lines[i]=' SOURCE_SHA256 = '+repr({k:closure['candidate/'+k] for k in old})
p.write_text('\n'.join(lines)+'\n')
print(json.dumps({'source_count':len(closure),'release_sha256':sha(descriptor),'composition_sha256':sha(p.read_bytes()),'real_activation':'HARD_DISABLED'}))

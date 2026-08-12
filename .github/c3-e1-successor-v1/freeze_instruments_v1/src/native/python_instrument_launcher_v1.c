#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <signal.h>
#include <grp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <unistd.h>

#define PYTHON "/opt/c3-e1/python-3.12.2/bin/python3"
#define ROOT "/opt/c3-e1/freeze-instruments-v1"
struct map { const char *id; const char *rel; uid_t uid; gid_t gid; int drop_identity; };
static const struct map MAP[] = {
 {"C3_E1_SUCCESSOR_AUDIT_REALTIME_PLUGIN_V1","src/blocker_005/audit_realtime_plugin_v1.py",61003,61003,1},
 {"C3_E1_SUCCESSOR_GUEST_EVIDENCE_MULTIPLEXER_V1","src/blocker_005/guest_evidence_multiplexer_v1.py",61001,61001,0},
 {"C3_E1_SUCCESSOR_HOST_EVIDENCE_SINK_V1","src/blocker_005/host_evidence_sink_v1.py",61010,61010,0},
 {"C3_E1_SUCCESSOR_NFTABLES_TRANSITION_MONITOR_V1","src/blocker_006/nftables_transition_monitor_v1.py",61002,61002,0},
 {"C3_E1_SUCCESSOR_NFTABLES_MONITOR_BOOTSTRAP_V1","src/blocker_006/nftables_monitor_bootstrap_v1.py",0,0,0},
 {"C3_E1_SUCCESSOR_OBSERVATION_AUTHORITY_V1","src/blocker_007/observation_authority_v1.py",61000,61000,0},
 {"C3_E1_SUCCESSOR_EXTERNAL_ATTESTATION_VERIFIER_V1","src/blocker_013/external_attestation_verifier_v1.py",61013,61013,0},
 {"C3_E1_SUCCESSOR_RUNTIME_INSTANTIATION_LAUNCHER_V1","src/blocker_014/runtime_instantiation_launcher_v1.py",0,0,0},
 {"C3_E1_SUCCESSOR_HOST_RUNTIME_LIFECYCLE_PROVIDER_V1","src/blocker_014/host_runtime_lifecycle_provider_v1.py",61011,61011,0},
 {"C3_E1_SUCCESSOR_ATTESTATION_TRANSACTION_CONTROLLER_V1","src/blocker_014/attestation_transaction_controller_v1.py",61012,61012,0},
 {NULL,NULL,0,0,0}
};
static const struct map *lookup(const char *id){ for(size_t i=0;MAP[i].id;i++) if(strcmp(id,MAP[i].id)==0) return &MAP[i]; return NULL; }
static int checked_setenv(const char *k,const char *v){ if(setenv(k,v,1)!=0){perror(k);return -1;} return 0; }
static int normalize_signals(void){
 sigset_t empty; if(sigemptyset(&empty)!=0 || sigprocmask(SIG_SETMASK,&empty,NULL)!=0){perror("signal mask");return -1;}
 const int sigs[]={SIGPIPE,SIGHUP,SIGTERM,SIGINT}; for(size_t i=0;i<sizeof(sigs)/sizeof(sigs[0]);i++) if(signal(sigs[i],SIG_DFL)==SIG_ERR){perror("signal disposition");return -1;} return 0;
}
static int close_unadmitted_fds(void){
 struct rlimit nf; if(getrlimit(RLIMIT_NOFILE,&nf)!=0){perror("getrlimit");return -1;} rlim_t lim=nf.rlim_cur; if(lim==RLIM_INFINITY || lim>1048576) lim=1048576;
 for(int fd=3;fd<(int)lim;fd++){ if(close(fd)!=0 && errno!=EBADF){perror("close fd");return -1;} }
 return 0;
}
int main(int argc,char **argv){
 if(argc!=2){fprintf(stderr,"instrument identity required\n");return 64;}
 const struct map *m=lookup(argv[1]); if(!m){fprintf(stderr,"unknown instrument identity\n");return 65;}
 if(clearenv()!=0){perror("clearenv");return 66;}
 if(checked_setenv("LC_ALL","C.UTF-8")||checked_setenv("LANG","C.UTF-8")||checked_setenv("TZ","UTC")||checked_setenv("HOME","/nonexistent")||checked_setenv("PATH","/usr/bin:/bin")) return 67;
 if(umask(0077)!=(mode_t)-1){} /* umask itself cannot fail */
 if(chdir("/")!=0){perror("chdir");return 68;}
 if(normalize_signals()!=0) return 69;
 struct rlimit z={0,0}; if(setrlimit(RLIMIT_CORE,&z)!=0){perror("setrlimit core");return 70;}
 if(close_unadmitted_fds()!=0) return 71;
 if(m->drop_identity){ if(setgroups(0,NULL)!=0){perror("setgroups");return 72;} if(setgid(m->gid)!=0){perror("setgid");return 73;} if(setuid(m->uid)!=0){perror("setuid");return 74;} }
 else if(m->uid!=0 && (getuid()!=m->uid || getgid()!=m->gid)){fprintf(stderr,"unexpected service uid/gid\n");return 75;}
 if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)!=0){perror("PR_SET_NO_NEW_PRIVS");return 76;}
 char script[PATH_MAX]; if(snprintf(script,sizeof(script),"%s/%s",ROOT,m->rel)>=(int)sizeof(script)) return 77;
 const char *bootstrap="import json,runpy,sys; from pathlib import Path; common=Path('/opt/c3-e1/freeze-instruments-v1/src/common'); env=runpy.run_path(str(common/'python_runtime_envelope_v1.py')); manifest=json.loads(Path('/opt/c3-e1/freeze-instruments-v1/python_runtime_closure_manifest_v1.json').read_text()); expected=manifest.get('sys_path');\nif not isinstance(expected,list): raise SystemExit('Python runtime closure not frozen'); sys.path[:]=expected; env['verify_runtime'](expected_sys_path=expected,import_roots=expected,require_flags=True,manifest=manifest); runpy.run_path(sys.argv[1],run_name='__main__')";
 char *const av[]={PYTHON,"-I","-B","-S","-X","utf8","-c",(char*)bootstrap,script,NULL};
 execve(PYTHON,av,environ); perror("execve"); return 78;
}

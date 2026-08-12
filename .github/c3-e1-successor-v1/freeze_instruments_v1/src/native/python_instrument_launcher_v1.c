#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <unistd.h>

#define PYTHON "/opt/c3-e1/python-3.12.2/bin/python3"
#define ROOT "/opt/c3-e1/freeze-instruments-v1"
struct map { const char *id; const char *rel; };
static const struct map MAP[] = {
 {"C3_E1_SUCCESSOR_AUDIT_REALTIME_PLUGIN_V1","src/blocker_005/audit_realtime_plugin_v1.py"},
 {"C3_E1_SUCCESSOR_GUEST_EVIDENCE_MULTIPLEXER_V1","src/blocker_005/guest_evidence_multiplexer_v1.py"},
 {"C3_E1_SUCCESSOR_HOST_EVIDENCE_SINK_V1","src/blocker_005/host_evidence_sink_v1.py"},
 {"C3_E1_SUCCESSOR_NFTABLES_TRANSITION_MONITOR_V1","src/blocker_006/nftables_transition_monitor_v1.py"},
 {"C3_E1_SUCCESSOR_NFTABLES_MONITOR_BOOTSTRAP_V1","src/blocker_006/nftables_monitor_bootstrap_v1.py"},
 {"C3_E1_SUCCESSOR_OBSERVATION_AUTHORITY_V1","src/blocker_007/observation_authority_v1.py"},
 {"C3_E1_SUCCESSOR_EXTERNAL_ATTESTATION_VERIFIER_V1","src/blocker_013/external_attestation_verifier_v1.py"},
 {"C3_E1_SUCCESSOR_RUNTIME_INSTANTIATION_LAUNCHER_V1","src/blocker_014/runtime_instantiation_launcher_v1.py"},
 {"C3_E1_SUCCESSOR_HOST_RUNTIME_LIFECYCLE_PROVIDER_V1","src/blocker_014/host_runtime_lifecycle_provider_v1.py"},
 {"C3_E1_SUCCESSOR_ATTESTATION_TRANSACTION_CONTROLLER_V1","src/blocker_014/attestation_transaction_controller_v1.py"},
 {NULL,NULL}
};
static const char *lookup(const char *id){ for(size_t i=0;MAP[i].id;i++) if(strcmp(id,MAP[i].id)==0) return MAP[i].rel; return NULL; }
int main(int argc,char **argv){
 if(argc!=2){fprintf(stderr,"instrument identity required\n");return 64;}
 const char *rel=lookup(argv[1]); if(!rel){fprintf(stderr,"unknown instrument identity\n");return 65;}
 if(clearenv()!=0) return 66;
 setenv("LC_ALL","C.UTF-8",1); setenv("LANG","C.UTF-8",1); setenv("TZ","UTC",1); setenv("HOME","/nonexistent",1); setenv("PATH","/usr/bin:/bin",1);
 umask(0077); chdir("/");
 sigset_t empty; sigemptyset(&empty); sigprocmask(SIG_SETMASK,&empty,NULL);
 signal(SIGPIPE,SIG_DFL); signal(SIGHUP,SIG_DFL); signal(SIGTERM,SIG_DFL); signal(SIGINT,SIG_DFL);
 struct rlimit z={0,0}; setrlimit(RLIMIT_CORE,&z);
 struct rlimit nf; if(getrlimit(RLIMIT_NOFILE,&nf)==0){ rlim_t lim=nf.rlim_cur; if(lim==RLIM_INFINITY || lim>1048576) lim=1048576; for(int fd=3; fd<(int)lim; ++fd) close(fd); }
 if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)!=0){perror("PR_SET_NO_NEW_PRIVS");return 67;}
 char script[PATH_MAX]; if(snprintf(script,sizeof(script),"%s/%s",ROOT,rel)>= (int)sizeof(script)) return 68;
 char scriptdir[PATH_MAX]; strncpy(scriptdir,script,sizeof(scriptdir)); scriptdir[sizeof(scriptdir)-1]='\0'; char *slash=strrchr(scriptdir,'/'); if(!slash) return 70; *slash='\0';
 const char *bootstrap="import json,runpy,sys; from pathlib import Path; common=Path('/opt/c3-e1/freeze-instruments-v1/src/common'); env=runpy.run_path(str(common/'python_runtime_envelope_v1.py')); manifest=json.loads(Path('/opt/c3-e1/freeze-instruments-v1/python_runtime_closure_manifest_v1.json').read_text()); expected=manifest.get('sys_path');\nif not isinstance(expected,list): raise SystemExit('Python runtime closure not frozen'); sys.path[:]=expected; env['verify_runtime'](expected_sys_path=expected,import_roots=expected,require_flags=True); runpy.run_path(sys.argv[1],run_name='__main__')";
 char *const av[]={PYTHON,"-I","-B","-S","-X","utf8","-c",(char*)bootstrap,script,scriptdir,NULL};
 execve(PYTHON,av,environ); perror("execve"); return 69;
}

from __future__ import annotations
import ctypes,hashlib,os,socket,subprocess,time,uuid
from fd_policy_v1 import normalize_fd,verify_inherited,object_identity
from identity_io_v1 import canonical_bytes,canonical_sha256,read_json,require_file_identity,validate_schema_file,assert_resolved
from ipc_peer_auth_v1 import send_fd_with_credentials
PR_SET_NO_NEW_PRIVS=38
class LaunchError(RuntimeError): pass

def validate_frozen_output(cfg):
    if str(cfg['frozen_build_output_manifest_path']).startswith('UNRESOLVED') or str(cfg['raw_disk_path']).startswith('UNRESOLVED'): raise LaunchError('Stage-2 frozen output identity unresolved')
    m=read_json(cfg['frozen_build_output_manifest_path']); req={'manifest_type','artifact_format','architecture','raw_disk_byte_count','raw_disk_sha256','boot_artifacts_contained_in_frozen_disk'}
    if set(m)!=req or m['artifact_format']!='RAW_FULL_DISK_V1' or m['architecture']!='amd64' or not m['boot_artifacts_contained_in_frozen_disk']: raise LaunchError('frozen build manifest invalid')
    require_file_identity(cfg['raw_disk_path'],m['raw_disk_sha256'],m['raw_disk_byte_count']); return m,canonical_sha256(m)
def validate_verity(cfg):
    v=cfg['dm_verity']; req={'version','hash_algorithm','data_block_size','hash_block_size','num_data_blocks','salt','root_hash','hash_tree_path','hash_tree_sha256','hash_tree_byte_count','options'}
    if set(v)!=req or v['version']!=1 or v['hash_algorithm']!='sha256' or v['data_block_size']!=4096 or v['hash_block_size']!=4096: raise LaunchError('dm-verity geometry/config')
    assert_resolved(v,'dm-verity Stage-2 identity')
    if isinstance(v['num_data_blocks'],bool) or not isinstance(v['num_data_blocks'],int) or v['num_data_blocks']<=0: raise LaunchError('dm-verity data-block count')
    if {'ignore_corruption','check_at_most_once','ignore_zero_blocks'}&set(v['options']): raise LaunchError('prohibited dm-verity option')
    require_file_identity(v['hash_tree_path'],v['hash_tree_sha256'],v['hash_tree_byte_count']); return v
def open_verified_mapping(cfg):
    v=validate_verity(cfg); require_file_identity(cfg['veritysetup_path'],cfg['veritysetup_sha256'])
    args=[cfg['veritysetup_path'],'open',cfg['raw_disk_path'],cfg['dm_mapping_name'],v['hash_tree_path'],v['root_hash'],'--readonly','--hash',v['hash_algorithm'],'--data-block-size',str(v['data_block_size']),'--hash-block-size',str(v['hash_block_size']),'--data-blocks',str(v['num_data_blocks']),'--salt',v['salt']]
    cp=subprocess.run(args,shell=False,capture_output=True)
    if cp.returncode: raise LaunchError(f'verity mapping construction failed: {cp.returncode}')
    return os.open('/dev/mapper/'+cfg['dm_mapping_name'],os.O_RDONLY|os.O_CLOEXEC)
def verify_qemu_machine(cfg):
    require_file_identity(cfg['qemu_path'],cfg['qemu_sha256']); cp=subprocess.run([cfg['qemu_path'],'-machine','help'],shell=False,capture_output=True)
    if cp.returncode: raise LaunchError('qemu machine help failed')
    tok=cfg['qemu_machine_token'].encode()
    if not any(line.split() and line.split()[0]==tok for line in cp.stdout.splitlines()): raise LaunchError('versioned machine token absent')
    return hashlib.sha256(cp.stdout).hexdigest()
def drop_credentials(cfg):
    os.setgroups([]); os.setgid(cfg['qemu_gid']); os.setuid(cfg['qemu_uid']); libc=ctypes.CDLL(None,use_errno=True)
    if libc.prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)!=0: raise LaunchError('no_new_privs failed')
    caps={}
    for line in open('/proc/self/status'):
        if line.startswith(('CapEff:','CapPrm:','CapAmb:')): caps[line.split(':',1)[0]]=int(line.split()[1],16)
    if set(caps)!={'CapEff','CapPrm','CapAmb'} or any(caps.values()): raise LaunchError('capabilities remain after drop')
def launch_record(cfg,ru,no,msha,rawsha,v,bid,pid):
    required_identity_fields=['admitted_environment_specification_sha256','qemu_sha256','qemu_machine_configuration_sha256','guest_firmware_sha256','host_evidence_channel_configuration_sha256','host_attestation_state_reference']
    assert_resolved({k:cfg[k] for k in required_identity_fields},'launch identity')
    fd_binding=canonical_sha256({'fd':3,'verified_block_object_identity':bid})
    obj={'record_type':'RUNTIME_INSTANTIATION_ATTESTATION_RECORD','admitted_environment_specification_sha256':cfg['admitted_environment_specification_sha256'],'frozen_build_output_manifest_sha256':msha,'raw_disk_sha256':rawsha,'dm_verity_configuration_sha256':canonical_sha256(v),'dm_verity_root_hash':v['root_hash'],'dm_verity_hash_tree_sha256':v['hash_tree_sha256'],'verified_block_object_identity':bid,'qemu_binary_sha256':cfg['qemu_sha256'],'qemu_machine_configuration_sha256':cfg['qemu_machine_configuration_sha256'],'preopened_fd_binding_identity':fd_binding,'qemu_process_identity':f"pid={pid};expected_exec_sha256={cfg['qemu_sha256']}",'runtime_instance_uuid':ru,'observation_nonce':no,'guest_firmware_identity':cfg['guest_firmware_sha256'],'host_evidence_channel_configuration_sha256':cfg['host_evidence_channel_configuration_sha256'],'host_attestation_state_reference':cfg['host_attestation_state_reference'],'launch_timestamp_monotonic':time.monotonic_ns(),'launch_timestamp_utc':time.time_ns()}
    validate_schema_file(obj,cfg['record_schema_path']); return obj,canonical_sha256(obj)
def main():
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_014/blocker_014_config_v1.json'); m,msha=validate_frozen_output(cfg); v=validate_verity(cfg); verify_qemu_machine(cfg); fd=normalize_fd(open_verified_mapping(cfg),3); verify_inherited((0,1,2,3)); bid=object_identity(3); ru=str(uuid.uuid4()); no=os.urandom(32).hex(); rec,rsha=launch_record(cfg,ru,no,msha,m['raw_disk_sha256'],v,bid,os.getpid()); pidfd=os.pidfd_open(os.getpid()); s=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET); s.connect(cfg['lifecycle_handoff_socket']); send_fd_with_credentials(s,canonical_bytes({'record_type':'LAUNCHER_PIDFD_HANDOFF','runtime_instance_uuid':ru,'observation_nonce':no,'runtime_instantiation_attestation_record':rec,'runtime_instantiation_attestation_record_sha256':rsha}),pidfd); s.close(); os.close(pidfd); drop_credentials(cfg)
    if '-qmp' in cfg['qemu_argv'] or '-monitor' in cfg['qemu_argv']: raise LaunchError('QEMU control channel prohibited')
    os.execve(cfg['qemu_path'],[cfg['qemu_path'],*cfg['qemu_argv']],cfg['qemu_environment'])
if __name__=='__main__': main()

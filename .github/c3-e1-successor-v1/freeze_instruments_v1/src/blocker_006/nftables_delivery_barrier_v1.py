class StabilityError(RuntimeError):pass
def evaluate(*,snapshot_a_valid,snapshot_b_valid,snapshot_a_sha256,snapshot_b_sha256,genid_open,genid_after_b,genid_final,notification_count,barrier_healthy):
 if not(snapshot_a_valid and snapshot_b_valid):raise StabilityError('complete snapshots required')
 if snapshot_a_sha256!=snapshot_b_sha256:raise StabilityError('snapshot identities differ')
 if not(genid_open==genid_after_b==genid_final):raise StabilityError('generation changed')
 if notification_count!=0:raise StabilityError('mutation invalidates stability pair')
 if not barrier_healthy:raise StabilityError('barrier unhealthy')
 return 'PASS'
def barrier_record(**kw):
 req={'barrier_id','runtime_instance_uuid','observation_nonce','snapshot_a_sha256','snapshot_b_sha256','genid_open','genid_after_b','genid_final','monitor_source_sequence_at_request','monitor_source_sequence_at_ack','requested_so_rcvbuf','effective_so_rcvbuf','enobufs_observed','msg_trunc_observed','nlmsg_overrun_observed','receiver_continuity','notification_count_during_window'}
 if set(kw)!=req:raise StabilityError('barrier fields mismatch')
 return {'record_type':'NFTABLES_NOTIFICATION_BARRIER',**kw}

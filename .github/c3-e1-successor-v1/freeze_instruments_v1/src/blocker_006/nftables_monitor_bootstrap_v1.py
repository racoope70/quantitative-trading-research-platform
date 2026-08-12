from __future__ import annotations
import os,socket
from ipc_peer_auth_v1 import send_fd_with_credentials
from identity_io_v1 import read_json,assert_resolved
class BootstrapError(RuntimeError): pass

def create_notification_socket(groups,requested_rcvbuf):
    if not isinstance(groups,int) or groups<=0: raise BootstrapError('exact notification groups required')
    s=socket.socket(socket.AF_NETLINK,socket.SOCK_RAW,socket.NETLINK_NETFILTER)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,requested_rcvbuf)
    effective=s.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
    if effective<=0: s.close(); raise BootstrapError('effective SO_RCVBUF unavailable')
    s.bind((0,groups))
    return s,effective

def handoff(sock,ipc):
    send_fd_with_credentials(ipc,b'NFTABLES_NOTIFICATION_FD_V1',sock.fileno())

def main():
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_006/blocker_006_config_v1.json')
    assert_resolved({'notification_groups':cfg['notification_groups']},'nftables notification groups')
    notification,effective=create_notification_socket(cfg['notification_groups'],cfg['requested_so_rcvbuf'])
    peer=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET)
    try:
        peer.connect(cfg['monitor_bootstrap_peer_socket'])
        handoff(notification,peer)
        ack=peer.recv(256)
        if ack!=b'NFTABLES_NOTIFICATION_FD_ACCEPTED_V1': raise BootstrapError('monitor FD handoff not acknowledged')
        if effective!=notification.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF): raise BootstrapError('notification socket buffer identity drift')
    finally:
        peer.close(); notification.close()
if __name__=='__main__': main()

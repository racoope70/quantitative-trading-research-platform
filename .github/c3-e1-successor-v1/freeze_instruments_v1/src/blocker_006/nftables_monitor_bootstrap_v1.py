from __future__ import annotations
import array,socket
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_NFTABLES_MONITOR_BOOTSTRAP_V1'; NETLINK_NETFILTER=12

def create_notification_socket(groups:int,rcvbuf:int):
    s=socket.socket(socket.AF_NETLINK,socket.SOCK_RAW,NETLINK_NETFILTER); s.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,rcvbuf); s.bind((0,groups)); return s,s.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
def transfer_fd(control:socket.socket,fd:int):
    fds=array.array('i',[fd]); control.sendmsg([b'NFTFD1'],[(socket.SOL_SOCKET,socket.SCM_RIGHTS,fds)])
def main(): raise SystemExit('exact nftables multicast groups are Stage-1 kernel-material dependent')
if __name__=='__main__': main()

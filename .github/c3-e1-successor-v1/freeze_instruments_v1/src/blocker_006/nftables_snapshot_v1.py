from __future__ import annotations
import errno,hashlib,socket,struct
NLMSG_ERROR=2;NLMSG_DONE=3;NLMSG_OVERRUN=4;NLM_F_DUMP_INTR=0x10;HDR=struct.Struct('=IHHII');ERR=struct.Struct('=i')
class NetlinkDumpError(RuntimeError):pass
def iter_msgs(dg):
 off=0
 while off<len(dg):
  if len(dg)-off<HDR.size:raise NetlinkDumpError('truncated nlmsghdr')
  n,t,f,s,p=HDR.unpack_from(dg,off)
  if n<HDR.size or off+n>len(dg):raise NetlinkDumpError('invalid nlmsg length')
  raw=dg[off:off+n];yield {'type':t,'flags':f,'seq':s,'payload':raw[HDR.size:],'raw':raw};off+=(n+3)&~3
 if off!=len(dg):raise NetlinkDumpError('trailing/alignment bytes')
def validate_dump(datagrams,expected_seq,recv_flags=()):
 if any(recv_flags):raise NetlinkDumpError('loss/truncation flag')
 done=False;records=[]
 for dg in datagrams:
  for m in iter_msgs(dg):
   if done:raise NetlinkDumpError('data after NLMSG_DONE')
   if m['seq']!=expected_seq:raise NetlinkDumpError('sequence mismatch')
   if m['flags']&NLM_F_DUMP_INTR:raise NetlinkDumpError('NLM_F_DUMP_INTR')
   if m['type']==NLMSG_OVERRUN:raise NetlinkDumpError('NLMSG_OVERRUN')
   if m['type'] in (NLMSG_ERROR,NLMSG_DONE):
    if len(m['payload'])<4:raise NetlinkDumpError('return code missing')
    code=ERR.unpack_from(m['payload'])[0]
    if code!=0:raise NetlinkDumpError(f'netlink completion error {code}')
    if m['type']==NLMSG_DONE:done=True
   else:records.append(m['raw'])
 if not done:raise NetlinkDumpError('NLMSG_DONE missing')
 return records
def _transaction_identity(request,datagrams):
 raw=b''.join(datagrams)
 return {
  'request_byte_count':len(request),
  'request_sha256':hashlib.sha256(request).hexdigest(),
  'request_hex':request.hex(),
  'response_datagram_count':len(datagrams),
  'response_byte_count':len(raw),
  'response_sha256':hashlib.sha256(raw).hexdigest(),
  'response_datagrams_hex':[x.hex() for x in datagrams],
 }
def recv_complete_dump(sock,request,request_seq,max_datagram=1048576,requested_so_rcvbuf=None):
 if requested_so_rcvbuf is None or isinstance(requested_so_rcvbuf,bool) or not isinstance(requested_so_rcvbuf,int) or requested_so_rcvbuf<=0:raise NetlinkDumpError('configured requested SO_RCVBUF required')
 effective=sock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
 sent=sock.send(request)
 if sent!=len(request):raise NetlinkDumpError('short netlink request send')
 dgs=[]
 while True:
  try:data,anc,flags,addr=sock.recvmsg(max_datagram)
  except OSError as e:
   if e.errno==errno.ENOBUFS:raise NetlinkDumpError('ENOBUFS') from e
   raise
  if flags&socket.MSG_TRUNC:raise NetlinkDumpError('MSG_TRUNC')
  dgs.append(data)
  if any(m['type']==NLMSG_DONE for m in iter_msgs(data)):break
 records=validate_dump(dgs,request_seq)
 return {'request_seq':request_seq,'requested_so_rcvbuf':requested_so_rcvbuf,'effective_so_rcvbuf':effective,'raw_transaction':_transaction_identity(request,dgs),'records':records}

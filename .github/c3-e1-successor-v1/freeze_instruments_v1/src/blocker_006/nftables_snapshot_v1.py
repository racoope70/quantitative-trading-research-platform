from __future__ import annotations
import struct
NLMSG_ERROR=2; NLMSG_DONE=3; NLMSG_OVERRUN=4; NLM_F_DUMP_INTR=0x10
_HDR=struct.Struct('IHHII'); _ERR=struct.Struct('i')
class NetlinkDumpError(RuntimeError): pass

def iter_nlmsgs(datagram:bytes):
    off=0
    while off<len(datagram):
        if len(datagram)-off<_HDR.size: raise NetlinkDumpError('truncated nlmsghdr')
        length,typ,flags,seq,pid=_HDR.unpack_from(datagram,off)
        if length<_HDR.size or off+length>len(datagram): raise NetlinkDumpError('invalid nlmsg length')
        payload=datagram[off+_HDR.size:off+length]
        yield {'type':typ,'flags':flags,'seq':seq,'pid':pid,'payload':payload,'raw':datagram[off:off+length]}
        off+=(length+3)&~3
    if off!=len(datagram): raise NetlinkDumpError('alignment/trailing bytes')

def validate_dump(datagrams,expected_seq:int,recv_flags=()):
    if any(recv_flags): raise NetlinkDumpError('loss/truncation flag')
    done=False; records=[]
    for dg in datagrams:
        for m in iter_nlmsgs(dg):
            if m['seq']!=expected_seq: raise NetlinkDumpError('transaction sequence mismatch')
            if m['flags'] & NLM_F_DUMP_INTR: raise NetlinkDumpError('NLM_F_DUMP_INTR')
            if m['type']==NLMSG_OVERRUN: raise NetlinkDumpError('NLMSG_OVERRUN')
            if m['type'] in (NLMSG_ERROR,NLMSG_DONE):
                if len(m['payload'])<_ERR.size: raise NetlinkDumpError('completion missing return code')
                err=_ERR.unpack_from(m['payload'])[0]
                if err!=0: raise NetlinkDumpError(f'netlink completion error {err}')
                if m['type']==NLMSG_DONE: done=True
            else: records.append(m['raw'])
    if not done: raise NetlinkDumpError('NLMSG_DONE missing')
    return records

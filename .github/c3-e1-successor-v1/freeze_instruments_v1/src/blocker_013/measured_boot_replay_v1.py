from __future__ import annotations
import hashlib,struct
class ReplayError(RuntimeError): pass
ALG_SIZES={0x0004:20,0x000B:32,0x000C:48,0x000D:64}; ALG_HASH={0x0004:'sha1',0x000B:'sha256',0x000C:'sha384',0x000D:'sha512'}
EV_NO_ACTION=0x00000003

def extend(pcr,digest,alg):
    h=hashlib.new(alg); h.update(pcr); h.update(digest); return h.digest()
def replay_sha256_events(ds,initial=b'\0'*32):
    p=initial
    for d in ds:
        if len(d)!=32: raise ReplayError('SHA256 width')
        p=extend(p,d,'sha256')
    return p

def _legacy_event(raw,off):
    if len(raw)-off<32: raise ReplayError('truncated legacy event header')
    pcr,etype=struct.unpack_from('<II',raw,off); digest=raw[off+8:off+28]; n=struct.unpack_from('<I',raw,off+28)[0]; off+=32
    if off+n>len(raw): raise ReplayError('truncated legacy event data')
    data=raw[off:off+n]
    return {'pcr_index':pcr,'event_type':etype,'digests':{0x0004:digest},'event_data':data},off+n

def _parse_specid(data):
    if not data.startswith(b'Spec ID Event03'): raise ReplayError('unsupported first legacy event')
    if len(data)<28: raise ReplayError('truncated SpecID event')
    off=16+4+1+1+1+1
    if off+4>len(data): raise ReplayError('truncated SpecID algorithm count')
    count=struct.unpack_from('<I',data,off)[0]; off+=4
    algs={}
    if count<1 or count>64: raise ReplayError('SpecID algorithm count')
    for _ in range(count):
        if off+4>len(data): raise ReplayError('truncated SpecID algorithm')
        alg,size=struct.unpack_from('<HH',data,off); off+=4
        if alg in algs or size<=0 or size>128: raise ReplayError('invalid SpecID algorithm')
        algs[alg]=size
    if off>=len(data): raise ReplayError('truncated SpecID vendor size')
    vendor=data[off]; off+=1
    if off+vendor!=len(data): raise ReplayError('SpecID vendor length')
    return algs

def _event2(raw,off,alg_sizes):
    if len(raw)-off<12: raise ReplayError('truncated event2 header')
    pcr,etype,count=struct.unpack_from('<III',raw,off); off+=12
    if count<1 or count>64: raise ReplayError('digest count')
    ds={}
    for _ in range(count):
        if off+2>len(raw): raise ReplayError('truncated alg')
        alg=struct.unpack_from('<H',raw,off)[0]; off+=2; n=alg_sizes.get(alg)
        if not n: raise ReplayError('unsupported/unannounced digest alg')
        if off+n>len(raw): raise ReplayError('truncated digest')
        if alg in ds: raise ReplayError('duplicate digest alg')
        ds[alg]=raw[off:off+n]; off+=n
    if off+4>len(raw): raise ReplayError('truncated event size')
    n=struct.unpack_from('<I',raw,off)[0]; off+=4
    if off+n>len(raw): raise ReplayError('truncated event')
    e={'pcr_index':pcr,'event_type':etype,'digests':ds,'event_data':raw[off:off+n]}
    return e,off+n

def parse_event_log(raw,format_identity='TCG_PC_CLIENT_EVENT_LOG_V1'):
    if format_identity not in ('TCG_PC_CLIENT_EVENT_LOG_V1','TCG_PCR_EVENT2_LE_V1'): raise ReplayError('event log format not admitted')
    if not raw: raise ReplayError('empty event log')
    events=[]; off=0; alg_sizes=dict(ALG_SIZES)
    if format_identity=='TCG_PC_CLIENT_EVENT_LOG_V1':
        first,off=_legacy_event(raw,off)
        if first['event_type']!=EV_NO_ACTION: raise ReplayError('SpecID first event required')
        alg_sizes=_parse_specid(first['event_data']); events.append(first)
    while off<len(raw):
        e,off=_event2(raw,off,alg_sizes); events.append(e)
    return events

def replay(events,pcr_selection,algorithm_id=0x000B):
    if algorithm_id not in ALG_HASH: raise ReplayError('algorithm')
    size=ALG_SIZES[algorithm_id]; pcrs={int(i):b'\0'*size for i in pcr_selection}
    for e in events:
        if e['pcr_index'] in pcrs and algorithm_id in e['digests']: pcrs[e['pcr_index']]=extend(pcrs[e['pcr_index']],e['digests'][algorithm_id],ALG_HASH[algorithm_id])
    return pcrs

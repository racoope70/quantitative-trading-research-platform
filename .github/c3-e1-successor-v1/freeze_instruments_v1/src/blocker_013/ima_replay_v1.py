from __future__ import annotations
import hashlib
class IMAReplayError(RuntimeError):pass
def u32(raw,off,order):
 if off+4>len(raw):raise IMAReplayError('truncated u32')
 return int.from_bytes(raw[off:off+4],order),off+4
def parse_native_binary_measurements(raw,descriptor):
 req={'format_identity','byteorder','template_hash_algorithm','template_hash_size','allowed_templates'}
 if set(descriptor)!=req or descriptor['format_identity']!='IMA_NATIVE_BINARY_CANONICAL_V1' or descriptor['byteorder'] not in ('little','big'):raise IMAReplayError('IMA descriptor mismatch')
 alg=descriptor['template_hash_algorithm'];size=descriptor['template_hash_size']
 if alg not in hashlib.algorithms_available or hashlib.new(alg).digest_size!=size:raise IMAReplayError('template hash descriptor mismatch')
 off=0;out=[];order=descriptor['byteorder']
 while off<len(raw):
  pcr,off=u32(raw,off,order)
  if off+size>len(raw):raise IMAReplayError('truncated template hash')
  th=raw[off:off+size];off+=size;n,off=u32(raw,off,order)
  if n<1 or off+n>len(raw):raise IMAReplayError('template name length')
  name=raw[off:off+n].rstrip(b'\0').decode('ascii');off+=n
  if name not in descriptor['allowed_templates']:raise IMAReplayError('unapproved template')
  dlen,off=u32(raw,off,order)
  if off+dlen>len(raw):raise IMAReplayError('template data length')
  data=raw[off:off+dlen];off+=dlen
  if hashlib.new(alg,data).digest()!=th:raise IMAReplayError('native template digest mismatch')
  out.append({'pcr_index':pcr,'template_hash':th,'template_name':name,'template_data':data})
 return out
def replay_records(records,pcr_index=10,algorithm='sha256',initial=None):
 size=hashlib.new(algorithm).digest_size;p=b'\0'*size if initial is None else initial
 for r in records:
  if r['pcr_index']!=pcr_index:continue
  if len(r['template_hash'])!=size:raise IMAReplayError('PCR digest width requires exact kernel descriptor')
  p=hashlib.new(algorithm,p+r['template_hash']).digest()
 return p
def replay_template_digests(ds,initial=b'\0'*32):
 p=initial
 for d in ds:p=hashlib.sha256(p+d).digest()
 return p

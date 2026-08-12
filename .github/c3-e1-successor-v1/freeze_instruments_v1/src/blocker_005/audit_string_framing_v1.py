class FramingError(RuntimeError):pass
class LineFramer:
 def __init__(self,max_record=1048576):self.buf=bytearray();self.max=max_record
 def feed(self,data):
  self.buf.extend(data);out=[]
  while True:
   i=self.buf.find(b'\n')
   if i<0:break
   n=i+1
   if n>self.max:raise FramingError('audit record exceeds maximum')
   out.append(bytes(self.buf[:n]));del self.buf[:n]
  if len(self.buf)>self.max:raise FramingError('unterminated audit record exceeds maximum')
  return out
 def finish(self):
  if self.buf:raise FramingError('EOF with partial audit record')

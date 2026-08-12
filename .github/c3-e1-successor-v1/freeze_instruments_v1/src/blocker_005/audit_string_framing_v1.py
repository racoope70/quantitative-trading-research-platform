from __future__ import annotations
class FramingError(ValueError): pass
class LineFramer:
    def __init__(self,max_record=1048576): self.buf=bytearray(); self.max=max_record
    def feed(self,chunk:bytes):
        self.buf.extend(chunk); out=[]
        while True:
            i=self.buf.find(b'\n')
            if i<0:
                if len(self.buf)>self.max: raise FramingError('audit record exceeds maximum')
                return out
            n=i+1
            if n>self.max: raise FramingError('audit record exceeds maximum')
            out.append(bytes(self.buf[:n])); del self.buf[:n]
    def finish(self):
        if self.buf: raise FramingError('partial EOF record')

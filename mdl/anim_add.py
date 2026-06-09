import struct
class FRead(object): #Generic file reader
    def __init__(self,f,big_endian=False):
        self.endian='<'
        if(big_endian):
            self.endian ='>'
        self.file = f
    def swapEndian(self):
        if(self.endian == '>'):
            self.endian = '<'
        else:
            self.endian = '>'
    def u32(self):
        return struct.unpack(self.endian+'I', self.file.read(4))[0]
    def seek(self,offset,whence=0):
        self.file.seek(offset,whence)
    def tell(self):
        return self.file.tell()
    def read(self,x):
        return self.file.read(x)
    def read_return(self,off,size):
        ret = self.tell()
        self.seek(off)
        dat = self.read(size)
        self.seek(ret)
        return dat
class FWrite(object): #Generic file writer
    def __init__(self,f,big_endian=False):
        self.endian='<'
        if(big_endian):
            self.endian ='>'
        self.file = f
    def swapEndian(self):
        if(self.endian == '>'):
            self.endian = '<'
        else:
            self.endian = '>'
    def u32(self,val):
        self.file.write(struct.pack(self.endian+'I', val))
    def write(self,x):
        return self.file.write(x)
    
import sys

f = open(sys.argv[1],'rb')

fin = FRead(f,False)

count = fin.u32()
magic = fin.u32()

offsets = []
for x in range(count):
    offsets.append(fin.u32())
fin.seek(0,2)
offsets.append(fin.tell())

chunks = []

for x in range(count):
    print((offsets[x+1] - offsets[x]))
    chunks.append(fin.read_return(offsets[x],(offsets[x+1] - offsets[x])))
print(chunks)

del(fin)
f.close()

ani = open(sys.argv[2],'rb')

chunks.append(ani.read())

out = open(sys.argv[1],'wb')

fout = FWrite(out,False)

nsize = len(chunks)

fout.u32(nsize)
fout.u32(magic)

curOff = 8 + (4*nsize)
for x in chunks:
    fout.u32(curOff)
    curOff += len(x)
for x in chunks:fout.write(x)

out.close()
del(fout)
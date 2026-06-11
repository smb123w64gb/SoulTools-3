import struct,sys,os

def u8(file):
    return struct.unpack("B", file.read(1))[0]
def u16(file):
    return struct.unpack("<H", file.read(2))[0]
def u32(file):
    return struct.unpack("<I", file.read(4))[0]


class IRXPKG(object):
    def __init__(self):
        self.files = {}
    def read(self,f):
        for x in range(25):
            name = str(f.read(16).replace(b'\x00', b'').decode("utf-8"))
            print(name)
            size = u32(f)
            f.seek(44,1)
            data = f.read(size)
            self.files[name] = data

irx_file = open(sys.argv[1], "rb")
irxpack = IRXPKG()
irxpack.read(irx_file)

outDir = str(sys.argv[1]+"_Extract/")
os.makedirs(outDir, exist_ok=True)
for name,x in irxpack.files.items():
    file = open(outDir + name ,'wb')
    file.write(x)
    file.close()

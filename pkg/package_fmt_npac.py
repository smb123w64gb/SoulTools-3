import struct,sys,os

def u32(file):
    return struct.unpack(">I", file.read(4))[0]
def rR(f,o,l):#Read n Return, Takes file,offset,size returns data
    c = f.tell()
    f.seek(o)
    d = f.read(l)
    f.seek(c)
    return d

class PKG(object):
    def __init__(self):
        self.files = []
    def read(self,f):
        curIdx = 0
        while(curIdx != 0xFFFFFFFF):
            magic = u32(f)
            packsize = u32(f)
            filesize = u32(f)
            curIdx = u32(f)
            f.seek(0x10,1)
            self.files.append(f.read(filesize))
            f.seek(packsize-0x20-filesize,1)
pkg_file = open(sys.argv[1], "rb")
pkg_in = PKG()
pkg_in.read(pkg_file)
pkg_file.close()
outDir = str(sys.argv[1]+"_Extract/")
os.makedirs(outDir, exist_ok=True)
for idx,x in enumerate(pkg_in.files):
    if(x):
        fil = open(outDir + str("%04i" % idx) + ".nud",'wb')
        fil.write(x)
        fil.close()
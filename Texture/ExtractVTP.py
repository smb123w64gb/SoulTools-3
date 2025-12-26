import struct,sys

def u8(file):
    return struct.unpack("B", file.read(1))[0]
def u32(file):
    return struct.unpack("<I", file.read(4))[0]
def rR(f,o,l):#Read n Return, Takes file,offset,size returns data
    c = f.tell()
    f.seek(o)
    d = f.read(l)
    f.seek(c)
    return d
model = open(sys.argv[1],'rb')
type_in = u8(model)
texture_off = 0
texture_size = 0
if(type_in == 9 or type_in == 9):
    model.seek(0x24)
    texture_off = u32(model)
    model.seek(0x34)
    texture_size = u32(model) - texture_off
elif(type_in == 8):
    model.seek(0x14)
    texture_off = u32(model)
    model.seek(0x24)
    texture_size = u32(model) - texture_off
else:
    print("Header is not suported %s" % hex(type_in))

if(texture_off):
    texture_out = open(sys.argv[1]+'.vxt','wb')
    texture_out.write(rR(model,texture_off,texture_size))
    texture_out.close()
model.close()
import sys
import struct
import tristrip_rust
#https://github.com/Al-Hydra/Blender-XFBIN-Importer/tree/main/blender/utils/tristrip/tristrip_rust

def VertPS2(val):
    return struct.pack("<fffI", val[0],val[1],val[2],val[3])
def NormPS2(val):
    return struct.pack("<fff", val[0],val[1],val[2])
def UVPS2(val):
    return struct.pack("<ff", val[0],val[1])
def f32(val):
    return struct.pack("<f", val)
def w32(val):
    return struct.pack("<I", val)
def w16(val):
    return struct.pack("<H", val)
def w8(val):
    return struct.pack("B", val)

preabmle = bytes([
    0x01, 0x01, 0x00, 0x01, 0x00, 0x80, 0x01, 0x6C, 
])
finalpreamble = bytes([
    0x00, 0x40, 0x3E, 0x30, 0x12, 0x03, 0x00, 0x00, 0x0F, 0x00, 0x00, 0x00, 0x04, 0x01, 0x00, 0x01, 
])

class Model(object):
    def __init__(self):
        self.verts = []
        self.norms = []
        self.texcr = []
        self.color = []
        self.boneIdx = 0

        self.poly = []
    def readVert(self,v):
        if(len(v)>11):
            self.verts.append([float(v[0]),float(v[1]),float(v[2])])
            self.norms.append([float(v[3]),float(v[4]),float(v[5])])
            self.color.append([int(v[6]),int(v[7]),int(v[8]),int(v[9])])
            self.texcr.append([float(v[10]),float(v[11])])
        else:
            self.verts.append([float(v[0]),float(v[1]),float(v[2])])
            self.norms.append([float(v[3]),float(v[4]),float(v[5])])
            self.color.append([int(255),int(255),int(255),int(255)])
            self.texcr.append([float(v[6]),float(v[7])])
    def readPoly(self,v):
        self.poly.append([int(v[1]),int(v[2]),int(v[3])])
    def toBlob(self):
        
        stripped = tristrip_rust.stripify(self.poly,False)
        print(stripped)
        trilen = 0
        for x in stripped:
            trilen += len(x)
        out = bytearray()
        out.extend(preabmle) #Comonly found for static mesh
        out.extend(w8(trilen))
        out.append(0x80)
        out.extend(w16(0))
        out.extend(finalpreamble)

        out.append(0x3) #PosData
        out.append(0x80)
        out.extend(w8(trilen))
        out.append(0x6C)#UnpackMode?
        for x in stripped:
            stripEnd = len(x)-1
            for idy,y in enumerate(x):
                if(idy>1):
                    out.extend(VertPS2([self.verts[y][0],self.verts[y][1],self.verts[y][2],4080]))
                else:
                    out.extend(VertPS2([self.verts[y][0],self.verts[y][1],self.verts[y][2],36848]))

        out.append(4) #Normal
        out.append(0x80)
        out.extend(w8(trilen))
        out.append(0x68) #UnpackMode?
        for x in stripped:
            for y in x:
                out.extend(NormPS2([self.norms[y][0],self.norms[y][1],self.norms[y][2]]))
        
        out.append(2) #Color
        out.append(0x80)
        out.extend(w8(trilen))
        out.append(0x60)
        for x in stripped:
            for y in x:
                out.extend(w32(0x43000000)) #Bruh idk how this color thing works yet

        out.append(1) #UV
        out.append(0x80)
        out.extend(w8(trilen))
        out.append(0x64)
        for x in stripped:
            for y in x:
                out.extend(UVPS2([self.texcr[y][0],self.texcr[y][1]]))
        return out



obj_file = open(sys.argv[1],'r')
mdl_txt = Model()
start_read = False
for x in obj_file.readlines():
        if(start_read):
            if(vertCount):
                mdl_txt.readVert(x.split())
                vertCount -= 1
            elif(polyCount):
                mdl_txt.readPoly(x.split())
                polyCount -= 1
        if(x.find('element vertex ') == 0):
            vertCount = int(x.split()[-1])
        if(x.find('element face ') == 0):
            polyCount = int(x.split()[-1])
        if(x.find('end_header')==0):
            start_read = True

test = mdl_txt.toBlob()
outtest = open(sys.argv[1]+".bin",'wb')
outtest.write(test)
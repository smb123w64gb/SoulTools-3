import struct
from ctypes import *
from enum import auto, Enum

def u8(file):
    return struct.unpack("B", file.read(1))[0]
 
def u16(file):
    return struct.unpack("<H", file.read(2))[0]
 
def u32(file):
    return struct.unpack("<I", file.read(4))[0]

def u64(file):
    return struct.unpack("<Q", file.read(8))[0]
 
def f32(file):
    return struct.unpack("<f", file.read(4))[0]

def w64(file,val):
    file.write(struct.pack("<Q", val))

def w32(file,val):
    file.write(struct.pack("<I", val))

def w16(file,val):
    file.write(struct.pack("<H", val))

def w8(file,val):
    file.write(struct.pack("B", val))
class Dma_Tag_bits(Structure):
    _fields_ = [
            ("QWC", c_uint, 16),
            ("PAD", c_uint, 10),
            ("PCE", c_uint, 2),
            ("ID", c_uint, 3),
            ("IRQ", c_uint, 1),
            ("ADDR", c_uint, 31),
            ("SPR", c_uint, 1),
        ]
class DMA_Tag_Type(Enum):
    P2_DMA_TAG_REFE = 0
    P2_DMA_TAG_CNT = 1
    P2_DMA_TAG_NEXT = 2
    P2_DMA_TAG_REF = 3
    P2_DMA_TAG_REFS = 4
    P2_DMA_TAG_CALL = 5
    P2_DMA_TAG_RET = 6
    P2_DMA_TAG_END = 7

class Dma_Tag(object):
    def __init__(self):
        self.bits = Dma_Tag_bits()
        self.OPT1 = 0
        self.OPT2 = 0
    def read(self,f):
        self.bits = Dma_Tag_bits.from_buffer_copy(f.read(8))
        self.OPT1 = u32(f)
        self.OPT2 = u32(f)
    def write(self,f):
        w64(f,self.bits.asbyte)
        w32(f,self.OPT1)
        w32(f,self.OPT2)
    def __str__(self):
        sring = ''
        sring += str("%s,Offset:%s"%(DMA_Tag_Type(self.bits.ID).name,hex(self.bits.ADDR)))
        return sring

class VTP(object):
    def __init__(self):
        self.header = self.Header()
        self.dma_ents = []
    def read(self,f):
        self.header.read(f)
        f.seek(self.header.dmaTableHeader)
        for x in range(self.header.dmaCount):
            entrys = self.DMATable()
            entrys.read(f)
            self.dma_ents.append(entrys)
    class Header(object):
        def __init__(self):
            self.Magic = 2
            self.offset2DMAs = 4
            self.offsetCount = 4
            self.dmaCount = 1
            self.textureCount = 1
            self.dmaTableHeader = 0
            self.textureTableHeader = 0
            self.creditsOne = 0
            self.creditsTwo = 0
            self.extendOffsetOne = 0
            self.extendOffsetTwo = 0
        def __str__(self):
            stringout = ''
            stringout+= str('VTP Ver %i\n' % self.Magic)
            stringout+=str('Offset Count %i\n' % self.offsetCount)
            stringout+=str('DMA offset @ %i\n' % self.offset2DMAs)
            stringout+=str('DMA Chain Count %i\n' % self.dmaCount)

            stringout+=str('\nTexture Count %i\n' % self.textureCount)
            return stringout

        def read(self,f):
            self.Magic = u8(f)
            self.offset2DMAs = u8(f)
            self.offsetCount = u8(f)
            u8(f)
            self.dmaCount = u8(f)
            self.textureCount = u8(f)
            u16(f)
            self.dmaTableHeader = u32(f)
            self.textureTableHeader = u32(f)
            self.creditsOne = u32(f)
            self.creditsTwo = u32(f)
            self.extendOffsetOne = u32(f)
            self.extendOffsetTwo = u32(f)
        def write(self,f):
            w8(f,self.Magic)
            w8(f,self.offset2DMAs)
            w8(f,self.offsetCount)
            w8(f,0)

            w8(f,self.dmaCount)
            w8(f,self.textureCount)
            w16(f,0)
            w32(f,self.dmaTableHeader)
            w32(f,self.textureTableHeader)
            w32(f,self.creditsOne)
            w32(f,self.creditsTwo)
            w32(f,self.extendOffsetOne)
            w32(f,self.extendOffsetTwo)
    class UploadInfo(object):
        def __init__(self):
            headTag = Dma_Tag()
            
    class DMATable(object):
        class DMATableHeader(object):
            def __init__(self):
                self.offset = 0x20
                self.count = 0
                self.magic = 0x2C40
                self.unk = 0 #SC3 Specal
            def read(self,f):
                self.offset = u64(f)
                self.count = u16(f)
                self.magic = u16(f)
            def write(self,f):
                w64(self.offset)
                w16(self.count)
                w16(self.magic)
        def __init__(self):
            self.TableHeader = self.DMATableHeader()
            self.DMAChains = []
        def read(self,f):
            self.TableHeader.read(f)
            ret = f.tell()
            f.seek(self.TableHeader.offset)
            for x in range(self.TableHeader.count):
                tag = Dma_Tag()
                tag.read(f)
                self.DMAChains.append(tag)
            #end Tag why not
            tag = Dma_Tag()
            tag.read(f)
            self.DMAChains.append(tag)
            f.seek(ret)

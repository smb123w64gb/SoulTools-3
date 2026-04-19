import sys
import struct

def u8(file):
    return struct.unpack("B", file.read(1))[0]

def u16(file):
    return struct.unpack("<H", file.read(2))[0]
def b16(file):
    return struct.unpack(">H", file.read(2))[0]

fIN = open(sys.argv[1],'rb')

class StateMech(object):
    def __init__(self):
        self.BEValue = 0
        self.SpecalReturn = 0
        self.resultBuffer = 0
        self.curOff = 0
    def readState(self,f):
        state = u8(f)
        leadbit = state & 0x80
        state = state & 0x7f
        if(state == 2 or state == 6):
            print("endOfcmd")
            return 0
        if(state == 3 or state == 4 or state == 0x2a):
            arg1 = b16(f)
            print("%04i JMP: %s" %(self.curOff,hex(arg1)))
        if(state == 0x25):
            indexFunc = u8(f)
            arg1 = u8(f)
            print("%04i FUC:%s : %s" %(self.curOff,hex(indexFunc),hex(arg1)))
        else:
            arg1 = b16(f)
            print("%04i CMD:%s : %s" %(self.curOff,hex(state),arg1))
            self.curOff+=3
        return 1
test = StateMech()
while(test.readState(fIN)):
    pass
import sys
import struct

funcAdr = ["00189c20","00189c20","00173470","00173470","001b2020","001b18e8","001b1908","001b1928","001b1948","001b23f0","001b2420","001b5660","001b26e0","001b1968","001b1dd8","001b1e00","001b1e28","001b1e50","001b5660","001b5660","001b2620","001b19c0","001b1aa8","001b1c40","001b1c80","001b2020","001b1a88","001b1e98","001b1ec0","001b1ee8","001b1f10","001b1e98","001b1ec0","001b1ee8","001b1f10","001b56d0","001b5660","001b56b8"]

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
        elif(state == 8):
            print("%04i END" %(self.curOff))
            self.curOff+=1
        elif(state == 0x14):
            print("%04i AND" %(self.curOff))
            self.curOff+=1
        elif(state == 0x15):
            print("%04i OR" %(self.curOff))
            self.curOff+=1
        elif(state == 0x16):
            print("%04i NotZero" %(self.curOff))
            self.curOff+=1
        elif(state == 0x17):
            print("%04i LeftShift" %(self.curOff))
            self.curOff+=1
        elif(state == 0x18):
            print("%04i RightShift" %(self.curOff))
            self.curOff+=1
        elif(state == 3 or state == 4 or state == 0x2a):
            arg1 = b16(f)
            print("%04i JMP: %s" %(self.curOff,arg1))
            self.curOff+=3
        elif(state == 0x25):
            indexFunc = u8(f)
            arg1 = u8(f)
            print("%04i FUN_%s(Current_Player,%s,0x4f6bd0)" %(self.curOff,funcAdr[indexFunc],hex(arg1)))
            self.curOff+=3
        elif(state == 0x28):
            arg1 = b16(f)
            print("%04i JMPIF:%s" %(self.curOff,arg1))
            self.curOff+=3
        elif(state == 0xB or state == 9):
            arg1 = b16(f)
            self.resultBuffer = arg1
            print("%04i Store: %s" %(self.curOff,hex(arg1)))
            self.curOff+=3
        elif(state == 1):
            arg1 = b16(f)
            print("%04i Intro:%s : %s" %(self.curOff,hex(state),arg1))
            self.curOff+=3
        return 1
test = StateMech()
while(test.readState(fIN)):
    pass
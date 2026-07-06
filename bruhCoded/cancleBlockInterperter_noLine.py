import sys
import struct

funcAdr = [
    "FUN_0000",
    "CheckVal",
"FUN_0002",
"FUN_0003",
"FUN_0004",
"FUN_0005",
"ReturnBlk",
"FUN_0007",
"FUN_0008",
"FUN_0009",
"FUN_0010",
"FUN_0011",
"FUN_0012",
"FUN_0013",
"FUN_0014",
"FUN_0015",
"FUN_0016",
"FUN_0017",
"FUN_0018",
"FUN_0019",
"FUN_0020",
"FUN_0021",
"FUN_0022",
"FUN_0023",
"FUN_0024",
"FUN_0025",
"FUN_0026",
"FUN_0027",
"FUN_0028",
"FUN_0029",
"FUN_0030",
"FUN_0031",
"FUN_0032",
"FUN_0033",
"FUN_0034",
"FUN_0035",
"FUN_0036",
"FUN_0037",
"FUN_0038",
"FUN_0039"
]
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
        self.resultBuffer = []
        self.jumpPoint = []
        self.curOff = 0
        self.curVar = 0
    def readState(self,f):
        if self.curOff in self.jumpPoint:
            print("Addr_%04i:" %(self.curOff))
        state = u8(f)
        leadbit = state & 0x80
        state = state & 0x7f
        if(state == 2 or state == 6):
            print("\tendOfcmd")
            return 0
        elif(state == 8):
            
            print("\treturn Val%02i" % (self.curVar-1))
            self.curVar -= 1
            self.curOff+=1
        elif(state == 0x14):
            print("\tAND" )
            self.curOff+=1
        elif(state == 0x15):
            print("\tOR" )
            self.curOff+=1
        elif(state == 0x16):
            print("\tNotZero" )
            self.curOff+=1
        elif(state == 0x17):
            print("\tLeftShift" )
            self.curOff+=1
        elif(state == 0x18):
            print("\tRightShift" )
            self.curOff+=1
        elif(state == 3 or state == 4 or state == 0x2a):
            arg1 = b16(f)
            print("\tJMP: Addr_%04i" %(arg1))
            self.jumpPoint.append(arg1)
            self.curOff+=3
        elif(state == 0x25):
            indexFunc = u8(f)
            arg1 = u8(f)
            curStr = str("\tVal%02i = %s(" % (self.curVar,funcAdr[indexFunc]))
            self.curVar+=1
            for x in range(arg1):
                if(x>0):
                    curStr += ","
                curStr += str("%s"%hex(self.resultBuffer.pop()))
            curStr += ")"
            print(curStr)
            self.curOff+=3
        elif(state == 0x28):
            arg1 = b16(f)
            
            print("\tif(Val%02i):goto Addr_%04i" %(self.curVar-1,arg1))
            self.curVar-=1
            self.jumpPoint.append(arg1)
            self.curOff+=3
        elif(state == 0xB or state == 9):
            arg1 = b16(f)
            self.resultBuffer.append(arg1)
            #print("\tStore: %s" %(hex(arg1)))
            self.curOff+=3
        elif(state == 1):
            arg1 = b16(f)
            print("\tIntro:%s : %s" %(hex(state),arg1))
            self.curOff+=3
        return 1
test = StateMech()
print("Entry:")
while(test.readState(fIN)):
    pass
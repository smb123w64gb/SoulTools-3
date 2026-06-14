from fileRW import *
import sys


class cmnHrt(object):
    class ActionLookup(object):
        def __init__(self):
            self.name = 0
            self.desc = 0 #offsets to the names
            self.entrys = []
        def read(self,f: FRead):
            self.name = f.u16()
            self.desc = f.u16()
            for x in range(6):
                actionz = []
                for y in range(4):
                    actionz.append(f.u16())
                self.entrys.append(actionz)
    def __init__(self):
        self.entrys = []
    def read(self,f: FRead):
        for x in range(f.u32()):
            act = self.ActionLookup()
            act.read(f)
            self.entrys.append(act)

infile = open(sys.argv[1],'rb')
fileRead = FRead(infile)
actions  = cmnHrt()
actions.read(fileRead)
topMax = 0
topMin = 0xFFFF
totals = {}
for x in actions.entrys:
    for iny,y in enumerate(x.entrys):
        strNgy = ''+str("%03i"%iny)
        for z in y:
            lower = (0x7FF&z)
            upper = z>>11
            if upper not in totals:totals[upper] = {}
            if lower not in totals[upper]:totals[upper][lower] = 0
            totals[upper][lower] += 1
            '''print(upper)
            if(topMax<(0x7FF&z)):#11 bit huh
                topMax = (0x7FF&z)
            if(topMin>(0x7FF&z)):
                topMin = (0x7FF&z)
            strNgy += '\t' + hex(z)
        print(strNgy)

print(topMax)
print(topMin)'''
for x,y in totals.items():
    print(str(x)+'\t'+str(len(y)))
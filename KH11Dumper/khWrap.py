import sys
from kh11 import *
from fileRW import *
import json

infile = open(sys.argv[1],'rb')
indata = infile.read()
infile.close()
inread = FRead(indata)
moveset = KH11()
moveset.read(inread)

del(inread)

'''
Ok we need to clean up json out of
Actions
Hurtboxes
Export scripts as bin
Export internal anims
Cam stuff idk yet....


Folderize the 4 types, highlight ones that have things like hitboxes or grabdmg.
'''

'''lizt = ['Normal','Movement','Hurt','Subroutine']
iny = 0
for indx,x in enumerate([moveset.Normal,moveset.Movement,moveset.Hurt,moveset.Subroutine]):
    for y in x:
        if(y.motionIdx2 > 0x1000):
            print("%s_%03i:%s"%(lizt[indx],iny,hex(y.motionIdx2)))
        iny+=1'''
'''outfile = open(sys.argv[1] + '.rewote','wb')
outwrite = FWrite(outfile)
moveset.write(outwrite)
outfile.close()
del(outwrite)'''




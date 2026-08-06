import sys
from kh11 import *
from fileRW import *
import json
import os

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
grabz = {}
huryz = {}
for indx,x in enumerate([moveset.Normal,moveset.Movement,moveset.Hurt,moveset.Subroutine]):
    for y in x:
        cur_a_indx = y.attack_index
        if(cur_a_indx>=0):
            if(cur_a_indx < 0x1000):
                if(not cur_a_indx in huryz):
                    huryz[cur_a_indx] = 1
                else:
                    huryz[cur_a_indx] += 1
                print("hurtbox:%i"%cur_a_indx)
            else:
                grabindx = (cur_a_indx&0x7FF)
                if(not grabindx in grabz):
                    grabz[grabindx] = 1
                else:
                    grabz[grabindx] += 1
                print("Grabbox %i"%grabindx)
print(grabz)
for x in huryz:
    print(huryz[x])'''

'''outfile = open(sys.argv[1] + '.rewote','wb')
outwrite = FWrite(outfile)
moveset.write(outwrite)
outfile.close()
del(outwrite)'''

lizt = ['Normal','Movement','Hurt','Subroutine']

outDir = str(sys.argv[1]+"_Extract/")
os.makedirs(outDir, exist_ok=True)

for x in lizt:
    os.makedirs(outDir+x+'/', exist_ok=True)

for indx,x in enumerate([moveset.Normal,moveset.Movement,moveset.Hurt,moveset.Subroutine]):
    for indy,y in enumerate(x):
        subDir = outDir + lizt[indx] + '/'
        outjson = open(str("%s%04i.json"%(subDir,indy)),'w')
        outbin = open(str("%s%04i.bin"%(subDir,indy)),'wb')
        aout = y.to_json()
        outjson.write(aout[0])
        outbin.write(bytes(aout[1]))
        outjson.close()
        outbin.close()
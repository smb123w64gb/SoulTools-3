import sys
from kh11 import *
from fileRW import *

infile = open(sys.argv[1],'rb')
inread = FRead(infile)
moveset = KH11()
moveset.read(inread)

for idx,x in enumerate(moveset.Normal):
    #print(x)
    print(x.cmd_data)
    out = open(sys.argv[1]+str(".Nor.%04i.scmd"%idx),'wb')
    out.write(bytearray(x.cmd_data))
    out.close()
for idx,x in enumerate(moveset.Movement):
    #print(x)
    #print(x.cmd_data)
    out = open(sys.argv[1]+str(".Sub.%04i.scmd"%idx),'wb')
    out.write(bytearray(x.cmd_data))
    out.close()

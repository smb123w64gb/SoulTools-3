import sys
from kh11 import *
from fileRW import *

infile = open(sys.argv[1],'rb')
inread = FRead(infile)
moveset = KH11()
moveset.read(inread)

for x in moveset.Normal:
    print(x)
    #print(x.cmd_data)
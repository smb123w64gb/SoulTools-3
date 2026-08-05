import sys
from kh11 import *
from fileRW import *
import json

infile = open(sys.argv[1],'rb')
inread = FRead(infile)
moveset = KH11()
moveset.read(inread)
infile.close()
del(inread)
for x in moveset.Normal:
    print(x.to_json())
'''outfile = open(sys.argv[1] + '.rewote','wb')
outwrite = FWrite(outfile)
moveset.write(outwrite)
outfile.close()
del(outwrite)'''


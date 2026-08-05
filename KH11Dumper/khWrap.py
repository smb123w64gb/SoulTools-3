import sys
from kh11 import *
from fileRW import *

infile = open(sys.argv[1],'rb')
inread = FRead(infile)
moveset = KH11()
moveset.read(inread)
infile.close()
del(inread)
outfile = open(sys.argv[1] + '.rewote','wb')
outwrite = FWrite(outfile)
moveset.write(outwrite)
outfile.close()
del(outwrite)


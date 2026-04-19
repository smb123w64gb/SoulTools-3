def getString(f,offset = None):
        if(offset is not None):
            ret = f.tell()
            f.seek(offset)
        result = ""
        tmpChar = f.read(1)
        while ord(tmpChar) != 0:
            result += tmpChar.decode("shift_jis")
            tmpChar = f.read(1)
        if(offset):
            f.seek(ret)
        return result

import sys

test = open(sys.argv[1],'rb')
stringz = []
cur = 'test'
while(len(cur)):
     cur = getString(test)
     stringz.append(cur)
stringz.pop()
print(stringz)
from  fileRW import *
class Anim(object):
    def __init__(self):
        self.files = []
        self.magic = 0
    def read(self,f:FRead):
        count = f.u32()
        self.magic = f.u32()#Some magical Pixy dust
        mappings = []
        for _a in range(count):
            mappings.append(f.u32())
        f.seek(0,2)
        mappings.append(f.tell())
        sizes = []
        for a in range(count):
            sizes.append(mappings[a+1]-mappings[a])
        mappings.pop()
        for idx,a in enumerate(mappings):
            print(hex(8+(idx*4)))
            if(sizes[idx]):
                f.seek(a)
                self.files.append(f.read(sizes[idx]))
    def write(self,f:FWrite):
        f.u32(len(self.files))
        f.u32(self.magic)
        startData = 8 + (4*len(self.files))
        for x in self.files:
            f.u32(startData)
            startData+=len(x)
        for x in self.files:
            f.write(x)
from fileRW import *

class KH11(object):
    class Header(object):
        def __init__(self):
            self.MAGIC = b'KH11'
            self.day = 0
            self.month = 0
            self.year = 0
            self.sec = 0
            self.min = 0
            self.hour = 0
            self.numEntries = 0
            self.unk4 = 0
            self.attack_list = -1
            self.throw_info = -1
            self.moveGrpIdx1 = 0
            self.moveGrpCount1 = 0
            self.moveGrpIdx2 = 0
            self.moveGrpCount2 = 0
            self.hurtIdx = 0
            self.hurtCount = 0
            self.neutralIdx = 0
            self.neutralCount = 0

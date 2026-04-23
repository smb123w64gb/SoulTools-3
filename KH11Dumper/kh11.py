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
        def read(self,f:FRead):
            self.MAGIC = f.read(4)

            self.day = f.u8()
            self.month = f.u8()
            self.year = f.u16()
            self.sec = f.u8()
            self.min = f.u8()
            self.hour = f.u8()
            f.u8()

            self.numEntries = f.u16()
            self.unk4 = f.u16()

            self.attack_list = f.u32()
            self.throw_info = f.u32()

            self.moveGrpIdx1 = f.u16()
            self.moveGrpCount1 = f.u16()
            self.moveGrpIdx2 = f.u16()
            self.moveGrpCount2 = f.u16()
            self.hurtIdx = f.u16()
            self.hurtCount = f.u16()
            self.neutralIdx = f.u16()
            self.neutralCount = f.u16()
        def write(self,f:FWrite):
            f.write(self.MAGIC)
            f.u8(self.day)
            f.u8(self.month)
            f.u16(self.year)
            f.u8(self.sec)
            f.u8(self.min)
            f.u8(self.hour)
            f.u8(0)
            f.u16(self.numEntries)
            f.u16(self.unk4)
            f.u32(self.attack_list)
            f.u32(self.throw_info)
            f.u16(self.moveGrpIdx1)
            f.u16(self.moveGrpCount1)
            f.u16(self.moveGrpIdx2)
            f.u16(self.moveGrpCount2)
            f.u16(self.hurtIdx)
            f.u16(self.hurtCount)
            f.u16(self.neutralIdx)
            f.u16(self.neutralCount)
    class ActionInfo(object):
        def __init__(self):
            self.motionIdx = -1
            self.unkMotion = 0
            self.unk0 = 0
            self.motion_multiplier = 100.0
            self.speed_multiplier = 100.0
            self.unk1 = 0
            self.unk2 = 0
            self.unk3 = 0
            self.unk4 = 0.0
            self.unk5 = 0
            self.unk6 = 0
            self.unk7 = 0
            self.unk8 = 0
            self.unknown_multiplier = 0.0
            self.frameCount = 0
            self.frameCountUnk = 0
            self.cancel_address = 0
            self.attack_index = -1
        def read(self,f:FRead):
            self.motionIdx = f.s16()
            self.unkMotion = f.u16()
            self.unk0 = f.u32()
            self.motion_multiplier = f.f32()
            self.speed_multiplier = f.f32()
            self.unk1 = f.u32()
            self.unk2 = f.u32()
            self.unk3 = f.u32()
            self.unk4 = f.f32()
            self.unk5 = f.u32()
            self.unk6 = f.u32()
            self.unk7 = f.u32()
            self.unk8 = f.u32()
            self.unknown_multiplier = f.f32()
            self.frameCount = f.s16()
            self.frameCountUnk = f.u16()
            self.cancel_address = f.u32()
            self.attack_index = f.s32()
        def write(self,f:FWrite):
            f.s16(self.motionIdx)
            f.u16(self.unkMotion)
            f.u32(self.unk0)
            f.f32(self.motion_multiplier)
            f.f32(self.speed_multiplier)
            f.u32(self.unk1)
            f.u32(self.unk2)
            f.u32(self.unk3)
            f.f32(self.unk4)
            f.u32(self.unk5)
            f.u32(self.unk6)
            f.u32(self.unk7)
            f.u32(self.unk8)
            f.f32(self.unknown_multiplier)
            f.s16(self.frameCount)
            f.u16(self.frameCountUnk)
            f.u32(self.cancel_address)
            f.s32(self.attack_index)
    class AttackInfo(object):
        def __init__(self):
            pass
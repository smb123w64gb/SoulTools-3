from fileRW import *
from datetime import datetime

def readcmd(f:FRead):
    values = []
    while(1):
        state = f.u8()
        
        values.append(state)
        state = state & 0x7f
        match state:
            case 1 | 3 | 4 | 9 | 0xB | 0x25 | 0x28 | 0x2a:
                values.append(f.b16())
            case 2 | 6:
                return values
            case _:
                pass
def cmdLnFind(action,f:FRead):
        ret = f.tell()
        f.seek(action.cmd_address)
        data = readcmd(f)
        f.seek(ret)
        return data

class KH11(object):
    def __init__(self):
        self.header = self.Header()

        self.Normal = []
        self.Movement = []
        self.Hurt = []
        self.Subroutine = []

        self.HurtBoxes = []

        self.GrabDmgs = []
    def read(self,f:FRead):
        self.header.read(f)
        remainder = self.header.numEntries
        if(self.header.moveGrpCount1 != 0xFFFF):
            for x in range(self.header.moveGrpCount1):
                act = self.ActionInfo()
                act.read(f)
                self.Normal.append(act)
                remainder -= 1
        if(self.header.moveGrpCount2 != 0xFFFF and remainder>0):
            for x in range(self.header.moveGrpCount2):
                act = self.ActionInfo()
                act.read(f)
                self.Movement.append(act)
                remainder-=1
        if(self.header.hurtCount != 0xFFFF and remainder>0):
            for x in range(self.header.hurtCount):
                act = self.ActionInfo()
                act.read(f)
                self.Hurt.append(act)
                remainder-=1
        if(self.header.neutralCount != 0xFFFF and remainder>0):
            for x in range(self.header.neutralCount):
                act = self.ActionInfo()
                act.read(f)
                self.Subroutine.append(act)
                remainder-=1
        hurtCount = 0
        grabDmgCnt = 0
        for x in [self.Normal,self.Movement,self.Hurt,self.Subroutine]:
            for y in x:
                if(y.attack_index>=0):
                    
                    cur = y.attack_index
                    if(cur & 0x1000):
                        grabDmgCnt = (cur & 0xFFF)+1
                    else:
                        hurtCount = cur+1
        for x in range(hurtCount):
            hit = self.AttackInfo()
            hit.read(f)
            self.HurtBoxes.append(hit)
        for x in range(grabDmgCnt):
            self.GrabDmgs.append(f.u16())
    def write(self,f:FWrite):
        #Recalc time :)
        self.header.day = int(datetime.day)
        self.header.month = int(datetime.month)
        self.header.year = int(datetime.year)
        self.header.sec = int(datetime.second)
        self.header.min = int(datetime.min)
        self.header.hour = int(datetime.hour)
        #ok for real counts
        entrycount = 0
        for x in [self.Normal,self.Movement,self.Hurt,self.Subroutine]:
            entrycount += len(x)
        attackoff = 0x28+(entrycount * 0x40)
        throwoff = attackoff + (len(self.HurtBoxes)*0x58)
        scriptcur = throwoff + (len(self.GrabDmgs)*2)

        self.header.attack_list = attackoff
        self.header.throw_info = throwoff

        self.header.moveGrpCount1 = len(self.Normal)
        

        self.header.write(f)

        
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
            self.cmd_address = 0
            self.attack_index = -1
            self.cmd_data = []
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
            self.cmd_address = f.u32()
            self.attack_index = f.s32()
            self.cmd_data = cmdLnFind(self,f)
        def __str__(self):
            strOut = ''
            if(not 0x1000 & self.attack_index):
                strOut += 'Hurtbox:' + hex(self.attack_index)
            elif(self.attack_index > 0):
                strOut += 'GrabIndex:' + hex(self.attack_index&0xFFF)
            #strOut += str('Mot0: %04i | Mot1: %04i'%(self.motionIdx,self.unkMotion))

            return strOut
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
            f.u32(self.cmd_address)
            f.s32(self.attack_index)
    class AttackInfo(object):
        def __init__(self):
            self.hitbox = 0
            self.unk1 = 0
            self.unk2 = 0
            self.normal_vec = 0
            self.normal_launch_vec = 0
            self.counter_vec = 0
            self.counter_launch_vec = 0
            self.airborne_vec = 0
            self.block_vec = 0
            self.grounded_vec = 0
            self.type = 0
            self.notsure = 0
            self.start = 0
            self.active = 0
            self.damage = 0
            self.activeNOT = 0
            self.not_dmg = 0
            self.block_stun = 0
            self.hit_stun = 0
            self.counter_stun = 0
            self.unsure2 = 0
            self.dmg_type = 0
            self.counter_type = 0
            self.unk3 = 0
            self.unk4 = 0
            self.unk5 = 0
            self.unk6 = 0
        def read(self,f:FRead):
            self.hitbox = f.u32()
            self.unk1 = f.u16()
            self.unk2 = f.u16()
            self.normal_vec = f.u16_3()
            self.normal_launch_vec = f.u16_3()
            self.counter_vec = f.u16_3()
            self.counter_launch_vec = f.u16_3()
            self.airborne_vec = f.u16_3()
            self.block_vec = f.u16_3()
            self.grounded_vec = f.u16_3()
            self.type = f.u16()
            self.notsure = f.u16()
            self.start = f.u16()
            self.active = f.u16()
            self.damage = f.s16()
            self.activeNOT = f.u16()
            self.not_dmg = f.u16()
            self.block_stun = f.u16()
            self.hit_stun = f.u16()
            self.counter_stun = f.u16()
            self.unsure2 = f.u16()
            self.dmg_type = f.u16()
            self.counter_type = f.u16()
            self.unk3 = f.u16()
            self.unk4 = f.u16()
            self.unk5 = f.u32()
            self.unk6 = f.u32()
        def write(self,f:FWrite):
            f.u32(self.hitbox)
            f.u16(self.unk1)
            f.u16(self.unk2)
            f.u16_3(self.normal_vec)
            f.u16_3(self.normal_launch_vec)
            f.u16_3(self.counter_vec)
            f.u16_3(self.counter_launch_vec)
            f.u16_3(self.airborne_vec)
            f.u16_3(self.block_vec)
            f.u16_3(self.grounded_vec)
            f.u16(self.type)
            f.u16(self.notsure)
            f.u16(self.start)
            f.u16(self.active)
            f.s16(self.damage)
            f.u16(self.activeNOT)
            f.u16(self.not_dmg)
            f.u16(self.block_stun)
            f.u16(self.hit_stun)
            f.u16(self.counter_stun)
            f.u16(self.unsure2)
            f.u16(self.dmg_type)
            f.u16(self.counter_type)
            f.u16(self.unk3)
            f.u16(self.unk4)
            f.u32(self.unk5)
            f.u32(self.unk6)
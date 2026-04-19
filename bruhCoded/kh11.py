import struct

def u8(file):
    return struct.unpack("B", file.read(1))[0]

def u16(file):
    return struct.unpack("<H", file.read(2))[0]

def u32(file):
    return struct.unpack("<I", file.read(4))[0]

def u64(file):
    return struct.unpack("<Q", file.read(8))[0]

def f32(file):
    return struct.unpack("<f", file.read(4))[0]

class Vec3Short:
    def __init__(self, file):
        self.x = struct.unpack("<h", file.read(2))[0]  # s16
        self.y = struct.unpack("<h", file.read(2))[0]
        self.z = struct.unpack("<h", file.read(2))[0]

    def __repr__(self):
        return f"Vec3Short(x={self.x}, y={self.y}, z={self.z})"


class Attacks:
    def __init__(self, file):
        self.hitbox = u16(file)
        self.unk1 = u16(file)
        self.unk2 = u32(file)

        self.normal_vec = Vec3Short(file)
        self.normal_launch_vec = Vec3Short(file)
        self.counter_vec = Vec3Short(file)
        self.counter_launch_vec = Vec3Short(file)
        self.airborne_vec = Vec3Short(file)
        self.block_vec = Vec3Short(file)
        self.grounded_vec = Vec3Short(file)

        self.unk = Vec3Short(file)

        self.stange_guard = u16(file)
        self.startup = u16(file)
        self.active = u16(file)
        self.dmg = u16(file)

        self.block_stun = u16(file)
        self.hit_stun = u16(file)
        self.counter_stun = u16(file)

    def __repr__(self):
        return f"Attacks(hitbox={self.hitbox}, dmg={self.dmg})"

class Moves:
    def __init__(self, file):
        self.motionIdx = struct.unpack("<h", file.read(2))[0]  # s16
        self.unkMotion = u16(file)
        self.unk0 = u32(file)
        self.motion_multiplier = f32(file)
        self.speed_multiplier = f32(file)
        self.unk1 = u32(file)
        self.unk2 = u32(file)
        self.unk3 = u32(file)
        self.unk4 = f32(file)
        self.unk5 = u32(file)
        self.unk6 = u32(file)
        self.unk7 = u32(file)
        self.unk8 = u32(file)
        self.unknown_multiplier = f32(file)
        self.frameCount = struct.unpack("<h", file.read(2))[0]  # s16
        self.frameCountUnk = u16(file)
        self.cancel_address = u32(file)
        self.attack_index = struct.unpack("<i", file.read(4))[0]  # s32

    def __repr__(self):
        return f"Moves(motionIdx={self.motionIdx}, attack_index={self.attack_index})"


class KHeader:
    def __init__(self, file):
        self.magic = u32(file)
        self.day = u8(file)
        self.month = u8(file)
        self.year = u16(file)
        self.sec = u8(file)
        self.min = u8(file)
        self.hour = u16(file)
        self.numEntries = u16(file)
        self.unk4 = u16(file)  # This is used to size aChunk
        self.attack_list = u32(file)
        self.throw_info = u32(file)
        self.moveGrpIdx1 = u16(file)
        self.moveGrpCount1 = u16(file)
        self.moveGrpIdx2 = u16(file)
        self.moveGrpCount2 = u16(file)
        self.hurtIdx = u16(file)
        self.hurtCount = u16(file)
        self.neutralIdx = u16(file)
        self.neutralCount = u16(file)

    def __repr__(self):
        return f"KHeader(magic={self.magic}, numEntries={self.numEntries})"


def parse_kh_file(file_path):
    with open(file_path, "rb") as f:
        hdr = KHeader(f)
        
        chunks = []
        for _ in range(hdr.numEntries):
            chunks.append(Moves(f))
        return {
            "header": hdr,
            "moves": chunks,
        }
    
import sys

#note to self, just pass the open file so i can grab the cmd blocks.

data = parse_kh_file(sys.argv[1])
print(data["header"])
lenz = []
for move in data["moves"]:
    print(hex(move.cancel_address))
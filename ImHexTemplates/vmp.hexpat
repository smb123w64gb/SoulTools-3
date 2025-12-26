import std.io;
struct tVector4f{
    float X;
    float Y;
    float Z;
    float W;
}[[static,name(std::format("{},{},{},{}", X, Y, Z, W))]];
struct tVector3f{
    float X;
    float Y;
    float Z;
}[[static,name(std::format("{},{},{}", X, Y,Z))]];

struct Header{
    u32 Type;
    u8 Unk04;
    u8 Unk05;
    u8 Unk06;
    u8 Unk07;
    u16 Object1Count;
    u16 BoneCount;
    u32 VertCount;
    padding[16]; //SC3 Specal
    u32 BoneOffset;
    u32 tex_file_addr;
    u32 Object1Offset;
    u32 table5_addr;
    u32 table4_addr;
    u32 BoneHeaderOffset;
    u32 unk016;
    u32 table1_addr;
    u32 table2_addr;
    u32 table3_addr;
    u32 table6_addr;
};
struct boneInfo { // bone positions relative to its parent
    tVector4f EndPositionXYZScale;
    tVector4f StartPositionXYZScale;
    tVector3f Rotation; // eulerangles, degrees (n*360)
    u32 BoneNameOffset;
    tVector3f ukn_bone1;
    u8 ukn_bone2;
    u8 BoneParentIdx;
    u8 BoneIdx; // used for name look up?
    u8 ukn_bone3;
};
struct objectLayer{
    u8 type;
    u8 count;
    u8 unk0;
    u8 unk1;
    match(type){
    
    }
};
struct VMP{
Header HDR;
u32 ObjectOffset[HDR.Object1Count] @ HDR.table1_addr;
boneInfo Bones[HDR.BoneCount] @ HDR.BoneOffset;
u8 texture[HDR.BoneHeaderOffset - HDR.tex_file_addr] @ HDR.tex_file_addr;
};

VMP model @ 0;
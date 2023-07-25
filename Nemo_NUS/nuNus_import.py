from struct import unpack
import bpy
import bmesh

def ReadNUS_pointclouds_one(f, vertices=[], faces=[]):
    f.seek(0)
    ChunkRead = f.read()
    f.seek(0)
    for i in range(len(ChunkRead)):
        Chunk = f.read(4)
        if Chunk == b"0TSG":
            Size = unpack(">I", f.read(4))[0]
            ObjectCount = unpack(">I", f.read(4))[0]
            for i in range(int(Size)-12):
                offset = f.read(24)
                if offset == b"\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01":
                    unknown = unpack(">I", f.read(4))[0]
                    vertexCount = unpack(">I", f.read(4))[0]
                    for i in range(vertexCount):
                        vx = unpack(">f", f.read(4))[0]
                        vy = unpack(">f", f.read(4))[0]
                        vz = unpack(">f", f.read(4))[0]
                        r = unpack("B", f.read(1))[0] / 255.0
                        g = unpack("B", f.read(1))[0] / 255.0
                        b = unpack("B", f.read(1))[0] / 255.0
                        a = unpack("B", f.read(1))[0] / 255.0
                        uvx = unpack(">f", f.read(4))[0]
                        uvy = unpack(">f", f.read(4))[0]
                        vertices.append([vx,vy,vz])

                    unk1 = unpack(">H", f.read(2))[0]
                    unk2 = unpack("B", f.read(1))[0]
                    unk3 = unpack(">H", f.read(2))[0]
                    unk4 = unpack("B", f.read(1))[0]
                    unk5 = unpack(">H", f.read(2))[0]
                    unk6 = unpack("B", f.read(1))[0]
                    unk7 = unpack(">H", f.read(2))[0]
                    unk8 = unpack("B", f.read(1))[0]
                    unk9 = unpack(">H", f.read(2))[0]
                    unk10 = unpack("B", f.read(1))[0]
                    unk11 = unpack(">H", f.read(2))[0]
                    unk12 = unpack("B", f.read(1))[0]
                    FaceSize = unpack(">H", f.read(2))[0]
                    type1 = unpack("B", f.read(1))[0]
                    if type1==1:
                        
                        unknown_entrysize1 = unpack(">H", f.read(2))[0]#2
                        unknown = unpack("B", f.read(1))[0]#3
                        unknown2 = unpack(">H", f.read(2))[0]#5
                        unknown3 = unpack("B", f.read(1))[0]#6
                        unknown_entrysize2 = unpack(">H", f.read(2))[0]#8
                        unknown4 = unpack("B", f.read(1))[0]#9
                        unknown5 = unpack(">H", f.read(2))[0]#11
                        unknown6 = unpack("B", f.read(1))[0]#12
                        unknown7 = unpack(">H", f.read(2))[0]#14
                        unknown8 = unpack("B", f.read(1))[0]#15
                        unknown9 = unpack(">H", f.read(2))[0]#17
                        unknown10 = unpack("B", f.read(1))[0]#18
                        unknown11 = unpack(">H", f.read(2))[0]#20
                        unknown12 = unpack("B", f.read(1))[0]#21
                        unknown13 = unpack(">H", f.read(2))[0]#23
                        unknown14 = unpack("B", f.read(1))[0]#24
                        unknown15 = unpack(">H", f.read(2))[0]#26
                        unknown16 = unpack("B", f.read(1))[0]#27
                        unknown17 = unpack(">H", f.read(2))[0]#29
                        unknown18 = unpack("B", f.read(1))[0]#30
                        unknown19 = unpack(">H", f.read(2))[0]#32
                        unknown20 = unpack("B", f.read(1))[0]#33
                        unknown21 = unpack(">H", f.read(2))[0]#35
                        unknown22 = unpack("B", f.read(1))[0]#33
                        #TODO negative 0x98
                        facecount = unpack("B", f.read(1))[0]
                        #facecount loop
                        for i in range(facecount-2):
                            fa = unpack(">H", f.read(2))[0] >> 8
                            f.seek(1,1)
                            fb = unpack(">H", f.read(2))[0] >> 8
                            f.seek(1,1)
                            fc = unpack(">H", f.read(2))[0] >> 8
                            f.seek(1,1)
                            f.seek(-4,1)
                    elif type1==0:
                        
                        unknown_entrysize1 = unpack(">H", f.read(2))[0]#2
                        unknown = unpack("B", f.read(1))[0]#3
                        unknown2 = unpack(">H", f.read(2))[0]#5
                        unknown3 = unpack("B", f.read(1))[0]#6
                        unknown_entrysize2 = unpack(">H", f.read(2))[0]#8
                        unknown4 = unpack("B", f.read(1))[0]#9
                        unknown5 = unpack(">H", f.read(2))[0]#11
                        unknown6 = unpack("B", f.read(1))[0]#12
                        unknown7 = unpack(">H", f.read(2))[0]#14
                        unknown8 = unpack("B", f.read(1))[0]#15
                        unknown9 = unpack(">H", f.read(2))[0]#17
                        unknown10 = unpack("B", f.read(1))[0]#18
                        unknown11 = unpack(">H", f.read(2))[0]#20
                        unknown12 = unpack("B", f.read(1))[0]#21
                        unknown13 = unpack(">H", f.read(2))[0]#23
                        unknown14 = unpack("B", f.read(1))[0]#24
                        unknown15 = unpack(">H", f.read(2))[0]#26
                        unknown16 = unpack("B", f.read(1))[0]#27
                        unknown17 = unpack(">H", f.read(2))[0]#29
                        unknown18 = unpack("B", f.read(1))[0]#30
                        unknown19 = unpack(">H", f.read(2))[0]#32
                        unknown20 = unpack("B", f.read(1))[0]#33
                        unknown21 = unpack(">H", f.read(2))[0]#35
                        unknown22 = unpack("B", f.read(1))[0]#36
                        #TODO negative 0x98 #38
                        facecount = unpack("B", f.read(1))[0] # 39
                        #facecount loop
                        for i in range(facecount-2):
                            fa = unpack(">I", f.read(4))[0] >> 16
                            f.seek(2,1)
                            fb = unpack(">I", f.read(4))[0] >> 16
                            f.seek(2,1)
                            fc = unpack(">I", f.read(4))[0] >> 16
                            f.seek(2,1)
                            f.seek(-12,1)
                    #needs a loop
                        
                                                            
    mesh = bpy.data.meshes.new("dragonjan")
    mesh.from_pydata(vertices, [], faces)
    object = bpy.data.objects.new("dragonjan", mesh)
    bpy.context.collection.objects.link(object)

def NUSRead(filepath):
    with open(filepath, "rb") as f:
        ReadNUS_pointclouds_one(f, vertices=[], faces=[])

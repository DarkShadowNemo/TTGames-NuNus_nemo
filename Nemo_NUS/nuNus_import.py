from struct import unpack
import bpy        

def ReadNUS_pointclouds_one(f, vertices=[]):
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

                    readOne = f.read(60)
                    f.seek(-60,1)
                    if len(readOne) == 60:
                        
                        f.seek(16,1)
                        FaceSize = unpack(">I", f.read(4))[0]
                        Facetype_ = unpack("B", f.read(1))[0]
                        if Facetype_ == 0:
                            f.seek(1,1) # eight
                            f.seek(1,1) # 0xA0 flag
                            ############
                            #zero
                            f.seek(1,1)
                            f.seek(1,1)
                            f.seek(1,1)
                            f.seek(1,1)
                            #############
                            f.seek(1,1) # eight
                            f.seek(1,1) # 0xB0 flag
                            #############
                            #zero
                            f.seek(1,1)
                            f.seek(1,1)
                            f.seek(1,1)
                            #############
                            repeatedfafbfc = unpack("B", f.read(1))[0]
                            if repeatedfafbfc == 36:
                                f.seek(1,1) # eight
                                f.seek(1,1) # 0xA2 flag
                                ###########
                                #zero
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                                ############
                                f.seek(1,1) # eight
                                f.seek(1,1) # 0xB2 flag
                                ############
                                #zero
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                            elif repeatedfafbfc == 24:
                                f.seek(1,1) # eight
                                f.seek(1,1) # 0xA2 flag
                                ###########
                                #zero
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                                ############
                                f.seek(1,1) # eight
                                f.seek(1,1) # 0xB2 flag
                                ############
                                #zero
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                        elif Facetype_ == 1:
                            f.seek(1,1) # eight
                            f.seek(1,1) # 0xA0 flag
                            ############
                            #zero
                            f.seek(1,1)
                            f.seek(1,1)
                            f.seek(1,1)
                            f.seek(1,1)
                            #############
                            f.seek(1,1) # eight
                            f.seek(1,1) # 0xB0 flag
                            #############
                            #zero
                            f.seek(1,1)
                            f.seek(1,1)
                            f.seek(1,1)
                            #############
                            repeatedfafbfc = unpack("B", f.read(1))[0]
                            if repeatedfafbfc == 36:
                                f.seek(1,1) # eight
                                f.seek(1,1) # 0xA2 flag
                                ###########
                                #zero
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                                ############
                                f.seek(1,1) # eight
                                f.seek(1,1) # 0xB2 flag
                                ############
                                #zero
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                            elif repeatedfafbfc == 24:
                                f.seek(1,1) # eight
                                f.seek(1,1) # 0xA2 flag
                                ###########
                                #zero
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                                ############
                                f.seek(1,1) # eight
                                f.seek(1,1) # 0xB2 flag
                                ############
                                #zero
                                f.seek(1,1)
                                f.seek(1,1)
                                f.seek(1,1)
                            
    mesh = bpy.data.meshes.new("dragonjan")
    mesh.from_pydata(vertices, [], [])
    object = bpy.data.objects.new("dragonjan", mesh)
    bpy.context.collection.objects.link(object)

def NUSRead(filepath):
    with open(filepath, "rb") as f:
        ReadNUS_pointclouds_one(f, vertices=[])

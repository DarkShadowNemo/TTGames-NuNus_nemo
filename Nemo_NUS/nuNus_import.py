from struct import unpack
import bpy
        

def ReadNUS_TSG(f, vertices=[], faces=[]):
    f.seek(0)
    while 1:
        Chunk = f.read(4)
        if Chunk == b"0TSG":
            Size = unpack(">I", f.read(4))[0]
            ObjectCount = unpack(">I", f.read(4))[0]
            for i in range(int(Size)-12):
                f.seek(24,1)
                #offset = f.read(24)
                #if offset == b"\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01":
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
                f.seek(16,1)
                FaceSize = unpack(">I", f.read(4))[0]
                Facetype_ = unpack("B", f.read(1))[0]
                if Facetype_ == 1:
                    pass
                elif Facetype_ == 0:
                    pass
            break
        elif Chunk == b"SDNB":
            break
        
    mesh = bpy.data.meshes.new("dragonjan")
    mesh.from_pydata(vertices, [], faces)
    object = bpy.data.objects.new("dragonjan", mesh)
    bpy.context.collection.objects.link(object)

from struct import unpack, pack, calcsize
import bpy

vertices=[]
faces=[]
uvs=[]
colors=[]

def ReadNUS(f):
    f.seek(0)
    ChunkRead = f.read()
    f.seek(0)
    for i in range(len(ChunkRead)):
        Chunk = f.read(4)
        if Chunk == b"0TSG":
            FileSize = unpack(">I", f.read(4))[0]
            ObjectCount = unpack(">I", f.read(4))[0]
            for i in range(1):
                models_n = unpack(">I", f.read(4))[0]
                for i in range(models_n):
                    type1 = unpack(">I", f.read(4))[0]
                    if type1 == 0:
                       UnknownData = f.read(20)
                       VertexCount = unpack(">I", f.read(4))[0]
                       for i in range(VertexCount):
                           vx = unpack(">f", f.read(4))[0]
                           vy = unpack(">f", f.read(4))[0]
                           vz = unpack(">f", f.read(4))[0]
                           r = unpack("B", f.read(1))[0] / 255.0
                           g = unpack("B", f.read(1))[0] / 255.0
                           b = unpack("B", f.read(1))[0] / 255.0
                           a = unpack("B", f.read(1))[0] / 255.0
                           uvx = unpack(">f", f.read(4))[0]
                           uvy = unpack(">f", f.read(4))[0]
                           vertices.append([vx,vz,vy])
                           colors.append([r,g,b,a])
                           uvs.append([uvx,uvy])
                              
                       unpack(">H", f.read(2))[0]
                       unpack("B", f.read(1))[0]
                       unpack(">H", f.read(2))[0]
                       unpack("B", f.read(1))[0]
                       unpack(">H", f.read(2))[0]
                       unpack("B", f.read(1))[0]
                       unpack(">H", f.read(2))[0]
                       unpack("B", f.read(1))[0]
                       unpack(">H", f.read(2))[0]
                       unpack("B", f.read(1))[0]
                       unpack(">H", f.read(2))[0]
                       unpack("B", f.read(1))[0]
                       faceCountSize = unpack(">H", f.read(2))[0]+1
                       faceType = unpack("B", f.read(1))[0]
                       for i in range(faceCountSize-1):
                           if faceType == 0:
                              data = unpack(">H", f.read(2))[0]
                              if data == 0x9800:
                                 facecount = unpack("B", f.read(1))[0]
                                 for i in range(facecount-2):
                                     fa = unpack(">I", f.read(4))[0]>>16
                                     f.seek(2,1)
                                     fb = unpack(">I", f.read(4))[0]>>16
                                     f.seek(2,1)
                                     fc = unpack(">I", f.read(4))[0]>>16
                                     f.seek(2,1)
                                     f.seek(-12,1)
                                     faces.append([fa,fb,fc])
                           elif faceType == 1:
                                data = unpack(">H", f.read(2))[0]
                                if data == 0x9800:
                                   facecount = unpack("B", f.read(1))[0]
                                   for i in range(facecount-2):
                                       fa = unpack(">H", f.read(2))[0]>>8
                                       f.seek(1,1)
                                       fb = unpack(">H", f.read(2))[0]>>8
                                       f.seek(1,1)
                                       fc = unpack(">H", f.read(2))[0]>>8
                                       f.seek(1,1)
                                       f.seek(-6,1)
                                       faces.append([fa,fb,fc])
    mesh = bpy.data.meshes.new("dragonjan")
    mesh.from_pydata(vertices, [], faces)
    object = bpy.data.objects.new("dragonjan", mesh)
    bpy.context.collection.objects.link(object)
    
def NUSRead(filepath):
    with open(filepath, "rb") as f:
        ReadNUS(f)

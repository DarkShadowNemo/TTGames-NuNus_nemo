from struct import unpack, pack, calcsize
import bpy
import bmesh

def ReadNUS_pointclouds_one(f):
    f.seek(0)
    Chunk = f.read(4)
    if Chunk == b"0CSG":
        global FileSize
        FileSize = unpack(">I", f.read(4))[0]
        if FileSize == 641653:
            nametable = f.read(4)
            if nametable == b"LBTN":
                global nametableSize1
                global nametableSize2
                global nametableAll 
                nametableSize1 = unpack(">I", f.read(4))[0]
                nametableSize2 = unpack(">I", f.read(4))[0]
                for i in range(nametableSize1-12):
                    nametableAll = unpack("B", f.read(1))[0]
                TST = f.read(4)
                if TST == b"0TST":
                    global TextureSetSize1
                    TextureSetSize1 = unpack(">I", f.read(4))[0]
                    HST = f.read(4)
                    if HST == b"0HST":
                        global TextureCount
                        unpack(">I", f.read(4))[0]
                        TextureCount = unpack(">I", f.read(4))[0]
                        MXT = f.read(4)
                        if MXT == b"0MXT":
                            global TXSize1
                            global TXType1
                            global TXWidth1
                            global TXHeight1
                            global TXPixLen1
                            global TXSize2
                            global TXType2
                            global TXWidth2
                            global TXHeight2
                            global TXPixLen2
                            TXSize1 = unpack(">I", f.read(4))[0]
                            TXType1 = unpack(">I", f.read(4))[0]
                            TXWidth1 = unpack(">I", f.read(4))[0]
                            TXHeight1 = unpack(">I", f.read(4))[0]
                            TXPixLen1 = unpack(">I", f.read(4))[0]
                            for i in range(TXPixLen1):
                                pixel1 = unpack("B", f.read(1))[0]
                            MXT2 = unpack(">I", f.read(4))[0]
                            TXSize2 = unpack(">I", f.read(4))[0]
                            TXType2 = unpack(">I", f.read(4))[0]
                            TXWidth2 = unpack(">I", f.read(4))[0]
                            TXHeight2 = unpack(">I", f.read(4))[0]
                            TXPixLen2 = unpack(">I", f.read(4))[0]
def WriteNUS(f):
    f.write(b"0CSG")
    f.write(pack(">I", FileSize))
    f.write(b"LBTN")
    f.write(pack(">I", nametableSize1))
    f.write(pack(">I", nametableSize2))
    for i in range(nametableSize1-12):
        f.write(pack("B", nametableAll))
    f.write(b"0TST")
    f.write(pack(">I", TextureSetSize1))
    f.write(b"0HST")
    f.write(pack(">I", 12))
    f.write(pack(">I", TextureCount))
    f.write(b"0MXT")
    f.write(pack(">I", TXSize1))
    f.write(pack(">I", TXType1))
    f.write(pack(">I", TXWidth1))
    f.write(pack(">I", TXHeight1))
    f.write(pack(">I", TXPixLen1))
    for i in range(TXPixLen1):
        f.write(pack("B", 0))
    f.write(b"0MXT")
    f.write(pack(">I", TXSize2)) 
    f.write(pack(">I", TXType2))
    f.write(pack(">I", TXWidth2))
    f.write(pack(">I", TXHeight2))
    f.write(pack(">I", TXPixLen2))
    for i in range(TXPixLen2):
        f.write(pack("B", 0))

def NUSRead(filepath):
    with open(filepath, "rb") as f:
        ReadNUS_pointclouds_one(f)

def NUSWrite(filepath):
    with open(filepath, "wb") as f:
        WriteNUS(f)

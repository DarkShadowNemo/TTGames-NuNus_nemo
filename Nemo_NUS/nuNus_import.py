from struct import unpack, pack, calcsize
import bpy
from collections import namedtuple
from math import tan, atan
import bmesh
import mathutils
from io import BytesIO as bio

vertices=[]
faces=[]
uvs=[]
rgba=[]
txlist=[]
materials=[]
texanim_structs = []
msh_offsets = []

#returns not working width is not defined even though i did define it so you might have to add texture manually

Indent = namedtuple('Indent', 'signature end')
Image32 = namedtuple('Image32', 'width height data')

def DXTBlend(v1, v2): return (v1 * 3 + v2 * 5) >> 3
def Convert3To8(v): return (v << 5) | (v << 2) | (v >> 1)
def Convert4To8(v): return (v << 4) | v
def Convert5To8(v): return (v << 3) | (v >> 2)
def Convert6To8(v): return (v << 2) | (v >> 4)

def dxt1nemo_to_rgba(dxt1data, width, height) -> Image32:
    assert not width % 8 and not height % 8, f'Image dimensions (received: {width}x{height}) must be divisible by 8.'
    newdata = bio(b'\0'*(4*width*height))
    def DecodeDXTBlock(xoffset, yoffset):
        c1, c2, pixels = unpack('>2HL', dxt1data.read(8))
        blue1	= Convert5To8( c1        & 0b11111 )
        green1	= Convert6To8((c1 >> 5)  & 0b111111)
        red1	= Convert5To8((c1 >> 11) & 0b11111 )
        blue2	= Convert5To8( c2        & 0b11111 )
        green2	= Convert6To8((c2 >> 5)  & 0b111111)
        red2	= Convert5To8((c2 >> 11) & 0b11111 )
        palette = (
            bytes((red1, green1, blue1, 0xFF)),
            bytes((red2, green2, blue2, 0xFF)),
            *(
                (
                    bytes((DXTBlend(red2, red1), DXTBlend(green2, green1), DXTBlend(blue2, blue1), 0xFF)),
                    bytes((DXTBlend(red1, red2), DXTBlend(green1, green2), DXTBlend(blue1, blue2), 0xFF)),
                ) if c1 > c2 else (
                    bytes(((red1 + red2)//2, (green1 + green2)//2, (blue1 + blue2)//2, 0xFF)),
                    bytes(((red1 + red2)//2, (green1 + green2)//2, (blue1 + blue2)//2, 0)),
                    )
                )
            )
        pixels = (
            (pixels >> 30)       ,
            (pixels >> 28) & 0b11,
            (pixels >> 26) & 0b11,
            (pixels >> 24) & 0b11,
            (pixels >> 22) & 0b11,
            (pixels >> 20) & 0b11,
            (pixels >> 18) & 0b11,
            (pixels >> 16) & 0b11,
            (pixels >> 14) & 0b11,
            (pixels >> 12) & 0b11,
            (pixels >> 10) & 0b11,
            (pixels >> 8 ) & 0b11,
            (pixels >> 6 ) & 0b11,
            (pixels >> 4 ) & 0b11,
            (pixels >> 2 ) & 0b11,
            (pixels      ) & 0b11,
            )
        pixel = 0
        for y in range(4):
            for x in range(4):
                newdata.seek(
                    + 4*width*(y + yoffset)
                    + 4*(x + xoffset) )
                newdata.write(palette[pixels[pixel]])
                pixel += 1
        for y in range(0, height, 8):
            for x in range(0, width, 8):# Z-Z-Z shape tile order
                DecodeDXTBlock(x    , y    )
                DecodeDXTBlock(x + 4, y    )
                DecodeDXTBlock(x    , y + 4)
                DecodeDXTBlock(x + 4, y + 4)
        return Image32(width, height, newdata.getvalue())

def rgb5a3nemo_to_rgba(rgb5a3data, width, height):
    outbuffer = bio(b'\0'*(4*width*height))
    for ymacro in range(0, height, 4):
        for xmacro in range(0, width, 4):
            for ymicro in range(4):
                for xmicro in range(4):
                    short, = unpack('>H', rgb5a3data.read(2))
                    outbuffer.seek(
                        + 4*width*(ymacro + ymicro)
                        + 4*(xmacro + xmicro) )
                    outbuffer.write(bytes(
                        (	Convert5To8((short>>10)&0b11111),
                                Convert5To8((short>>5 )&0b11111),
                                Convert5To8((short    )&0b11111),0xFF) if short & 0x8000 else
                        (	Convert4To8((short>>8 )&0b1111),
                                Convert4To8((short>>4 )&0b1111),
                                Convert4To8((short    )&0b1111),
                                Convert3To8((short>>12)),)
                        ))
    return Image32(width, height, outbuffer.getvalue())

def chunk64nemo_to_rgba(chunk64data, width, height):
    outbuffer = bio(b'\0'*(4*width*height))
    for ymacro in range(0, height, 4):
        for xmacro in range(0, width, 4):
            division1, division2, = unpack('>16H', chunk64data.read(0x20)), unpack('>16H', chunk64data.read(0x20))
            for ymicro in range(4):
                for xmicro in range(4):
                    outbuffer.seek(
                        + 4*width*(ymacro + ymicro)
                        + 4*(xmacro + xmicro) )
                    n = (division1[2*ymicro + xmicro] << 16) | division2[2*ymicro + xmicro] | 0xFF
                    outbuffer.write( pack('>L', n) )
    return Image32(width, height, outbuffer.getvalue())
    
    
        
        
    
    
    

def ReadNUS(f):
    global TextureCount
    global TXMSize
    global TXMType
    global TXMLen
    global lbtnsize1
    global lbtnsize2
    global CSGFileSize
    global TSTSize1
    f.seek(0)
    ChunkRead = f.read()
    f.seek(0)
    for i in range(len(ChunkRead)):
        Chunk = f.read(4)
        if Chunk == b"0CSG":
            image_assignid = 0
            CSGFileSize = unpack(">I", f.read(4))[0]
            lbtn = f.read(4)
            lbtnsize1 = unpack(">I", f.read(4))[0]
            lbtnsize2 = unpack(">I", f.read(4))[0]
            for i in range(lbtnsize1-12):
                f.seek(1,1)
            tst = f.read(4)
            TSTSize1 = unpack(">I", f.read(4))[0]
            hst = f.read(4)
            hstSize1 = unpack(">I", f.read(4))[0]
            TextureCount = unpack(">I", f.read(4))[0]
        elif Chunk == b"0MXT":
            TXMSize = unpack(">I", f.read(4))[0]
            TXMType = unpack(">I", f.read(4))[0]
            TXMWidth = unpack(">I", f.read(4))[0]
            TXMHeight = unpack(">I", f.read(4))[0]
            TXMLen = unpack(">I", f.read(4))[0]

            if TXMType == 0x80:
                pass
            elif TXMType == 0x81:
                pass
            elif TXMType == 0x82:
                pass
            
        elif Chunk == b"0TSG":
            FileSize = unpack(">I", f.read(4))[0]
            ObjectCount = unpack(">I", f.read(4))[0]
            for i in range(ObjectCount-ObjectCount+1):
                
                models_n = unpack(">I", f.read(4))[0]
                f.seek(models_n+3,1)
                type1 = unpack(">I", f.read(4))[0]
                if type1 == 0:
                    unk1 = unpack(">I", f.read(4))[0]
                    unk2 = unpack(">I", f.read(4))[0]
                    unk3 = unpack(">I", f.read(4))[0]
                    unk4 = unpack(">I", f.read(4))[0]
                    VertexCount = unpack(">I", f.read(4))[0]
                    for i in range(VertexCount):
                        vx = unpack(">f", f.read(4))[0]
                        vy = unpack(">f", f.read(4))[0]
                        vz = unpack(">f", f.read(4))[0]
                        r = unpack("B", f.read(1))[0] / 127.0
                        g = unpack("B", f.read(1))[0] / 127.0
                        b = unpack("B", f.read(1))[0] / 127.0
                        a = unpack("B", f.read(1))[0] / 255.0
                        uvx = unpack(">f", f.read(4))[0]
                        uvy = unpack(">f", f.read(4))[0]
                        vertices.append([vx,vz,vy])
                        rgba.append([r,g,b,a])
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
                    faceCountSize = unpack(">H", f.read(2))[0]
                    faceType = unpack("B", f.read(1))[0]
                    for i in range(faceCountSize):
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
                               f.seek(12,1)
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
                               f.seek(6,1)
                    for i in range(faceCountSize):
                        #todo go backwards in a loop
                        pass
                elif type1 == 10:
                    pass
            break
    mesh = bpy.data.meshes.new("0")
    mesh.from_pydata(vertices, [], faces)
    object = bpy.data.objects.new("0", mesh)
    bpy.context.collection.objects.link(object)
    meshC = mesh.vertex_colors.new()

    for fac in mesh.polygons:
        fac.use_smooth = True

    uv_tex = mesh.uv_layers.new()
    uv_layer = mesh.uv_layers[0].data
    vert_loops = {}
    for l in mesh.loops:
        vert_loops.setdefault(l.vertex_index, []).append(l.index)
    for i, coord in enumerate(uvs):
        for li in vert_loops[i]:
            uv_layer[li].uv = coord
    index=0
    for vcol in mesh.vertex_colors[0].data:
        vcol.color = rgba[i]
        index+=i
    mesh.vertex_colors.active = meshC

def WriteNUS(f):
    f.write(b"0CSG")
    f.write(pack(">I", CSGFileSize))
    f.write(b"LBTN")
    f.write(pack(">I", lbtnsize1)) # hardcoded
    f.write(pack(">I", lbtnsize2)) # hardcoded
    for i in range(lbtnsize1-12):
        f.write(pack("B", 0)) # hardcoded
    f.write(b"0TST")
    f.write(pack(">I", TSTSize1))
    
        
    
        
    
def NUSRead(filepath):
    with open(filepath, "rb") as f:
        ReadNUS(f)

def NUSWrite(filepath):
    with open(filepath, "wb") as f:
        WriteNUS(f)

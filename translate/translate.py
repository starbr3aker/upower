import re
import sys
sys.path.append('../')
from checkInstructionType import checkInstructionType

INST_TAB = {
	"add": (31,0,266,0),
	"addi": (14),
	"addis": (15),
	"and": (31,28),
	"andi": (28),
	"extsw": (31,986,0),
	"nand": (31,476,0),
	"or": (31,444,0),
	"ori": (24),
	"subf": (31,0,40,0),
	"xor": (31,316,0),
	"xori":(26),
	"ld": (58,0),
	"lwz": (32),
	"std": (62,0),
	"stw": (36),
	"stwu": (37),
	"lhz": (40),
	"lha": (42),
	"sth":(44),
	"lbz": (34),
	"stb": (38),
	"rlwinm": (21,0),
	"sld": (31,27,0),
	"srd":(31,539,0),
	"srad": (31,794,0),
	"sradi": (31,413,0),
	"b": (18,0,0),
	"ba":(18,1,0),
	"bl": (18,0,1),
	"bclr": (19,0),
	"bc": (19,0,0),
	"bca": (19,1,0),
	"cmp": (31,0,0),
	"cmpi": (11)
}


def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if val != 0:
        val = val - (1 << bits)      
    return -val


def x(string,binary):
    """Translaate X format"""
    op = binary[0]
    xo = binary[1] << 20
    rc = binary[2] << 30
    temp = re.findall(r'\d+', string) 
    reg = list(map(int, temp)) 
    reg[0] = reg[0] << 5
    reg[1] = reg[1] << 10
    if len(reg) == 3:
        reg[2] = reg[2] << 15
    b32 = format((op + sum(reg) + xo + rc),"032b")
    print(b32)
    return b32


def xo(string,binary):
    """Translate XO format"""
    op = binary[0]
    oe = binary[1] << 20
    xo = binary[2] << 21
    rc = binary[3] << 30
    temp = re.findall(r'\d+', string) 
    reg = list(map(int, temp)) 
    reg[0] = reg[0] << 5
    reg[1] = reg[1] << 10
    if len(reg) == 3:
        reg[2] = reg[2] << 15
    b32 = format((op + sum(reg) + xo + oe + rc),"032b")
    print(b32)
    return b32


def xs(string,binary):
    """Translate XS format"""
    op = binary[0]
    xo = binary[1] << 20
    sh = 0
    rc = binary[2] << 30
    temp = re.findall(r'\d+', string) 
    reg = list(map(int, temp)) 
    reg[0] = reg[0] << 5
    reg[1] = reg[1] << 10
    reg[2] = reg[2] << 15
    b32 = format((op + sum(reg) + xo + rc + sh),"032b")
    print(b32)
    return b32


def d(string,binary):
    """Translate D format"""
    op = binary[0]
    temp = re.findall(r'-?\d+', string) 
    reg = list(map(int, temp))
    if(reg[1]<0):
        nf = 1
        reg[1]  = -reg[1]
    reg[0] = reg[0] << 5
    reg[2] = reg[2] << 10
    if nf:
        i=reg[1]
        k=0
        while i>1:
            i = i / 2
            k = k + 1
        reg[1] = twos_comp(reg[1],k)
        b16 = format(reg[1],"b")
        i=len(b16)
        while i <= 15:
            if i <= (k-1):
                b16 = "0" + b16
            else:
                b16 = "1" + b16
            i = i + 1
        b32 = format((op + reg[0] + reg[2]),"016b")
        b32 = b16 + b32
    else:
        reg[1] = reg[1] << 15
        b32 = format((op + reg[0] + reg[2] +reg[1]),"016b")
    print(b32)
    return b32


def ds(string,binary):
    """Translate DS format"""
    op = binary[0]
    xo = binary[1]
    temp = re.findall(r'-?\d+', string) 
    reg = list(map(int, temp))
    if(reg[1]<0):
        nf = 1
        reg[1]  = -reg[1]
    reg[0] = reg[0] << 5
    reg[2] = reg[2] << 10
    if nf:
        i = reg[1]
        k = 0
        while i>1:
            i = i / 2
            k = k + 1
        reg[1] = twos_comp(reg[1],k)
        b16 = format(reg[1],"b")
        i = len(b16)
        while i <= 13:
            if i <= (k-1):
                b16 = "0" + b16
            else:
                b16 = "1" + b16
            i = i + 1
        xo = format(xo,"002b")
        b32 = format((op + reg[0] + reg[2]),"016b")
        b32 = xo + b16 + b32
    else:
        reg[1] = reg[1] << 15
        xo = xo<<29
        b32 = format((op + reg[0] + reg[2] + reg[1] + xo),"016b")
    print(b32)
    return b32


def m(string,binary):
    """Translate M format"""
    op = binary[0]
    rc = binary[1] << 30
    temp = re.findall(r'\d+', string) 
    reg = list(map(int, temp)) 
    reg[0] = reg[0] << 5
    reg[1] = reg[1] << 10
    reg[2] = reg[2] << 15
    reg[3] = reg[3] << 20
    reg[4] = reg[4] << 25
    b32 = format((op + sum(reg) + rc),"032b")
    print(b32)
    return b32


def b(string,binary,label):
    """Translate B format"""
    op = binary[0]
    aa = binary[1]<<29
    lk = binary[2] <<30
    temp = re.findall(r'-?\d+', string) 
    reg = list(map(int, temp))
    reg[0] = reg[0] << 5
    reg[1] = reg[1] << 10
    line = string.split(",")[2].replace(",", "")
    line = label.get(line)
    line = line << 15
    aa = format(aa,"b")
    lk = format(lk,"b")
    b32 = format((op + reg[0] + line + reg[1] + lk + aa),"016b")
    print(b32)
    return b32

    
def i(string,binary,label):
    po = binary[0]
    aa = binary[1] << 29
    lk = binary[2] << 30
    line = string.split(",")[2].replace(",", "")
    line = label.get(line)
    line = line << 5
    b32 = format((po + aa + lk + line),"032b")
    print(b32)
    return b32

def translate(string,label):
    """Translating to a 32b instruction"""
    string=string.lstrip()
    instr = string.split(" ",1)
    form = checkInstructionType(instr[0])
    binary = INST_TAB.get(instr[0])
    if form == 1 :
        x(instr[1],binary)
    elif form == 2 :
        xo(instr[1],binary)
    elif form == 3:
        xs(instr[1],binary)
    elif form == 4:
        d(instr[1],binary)
    elif form == 5:
        ds(instr[1],binary)
    elif form == 6:
        m(instr[1],binary)
    elif form == 7:
        b(instr[1],binary,label)
    elif form == 8:
        i(instr[1],binary,label)

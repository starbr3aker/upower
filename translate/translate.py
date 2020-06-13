import re
import sys
sys.path.append('../')
from checkInstructionType import checkInstructionType


INST_TAB = {
	"add": (31,0,266,0),
	"addi": (14),
    "la": (16),
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
B = 0x0000_0000_0040_0000


def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if val != 0:
        val = val - (1 << bits)      
    return -val


def x(string,binary):
    """Translaate X format"""
    op = binary[0] << 26
    xo = binary[1] << 1
    rc = binary[2]
    temp = re.findall(r'\d+', string) 
    reg = list(map(int, temp))
    sum1 = 0
    if len(reg) == 4:
        print(reg[2])
        reg[0] = reg[0] << 21
        reg[2] = reg[2] << 16
        reg[3] = reg[3] << 11
        rc = reg[1]
        sum1 = reg[0] + reg[2] + reg[3]
    else:
        reg[0] = reg[0] << 21
        reg[1] = reg[1] << 16
        if len(reg) == 3:
            reg[2] = reg[2] << 11
        sum1 = reg[0] + reg[2] + reg[1]
    b32 = format((op + sum1 + xo + rc),"032b")
    return b32


def xo(string,binary):
    """Translate XO format"""
    op = binary[0] << 26
    oe = binary[1] << 10
    xo = binary[2] << 1
    rc = binary[3] 
    temp = re.findall(r'\d+', string) 
    reg = list(map(int, temp)) 
    reg[0] = reg[0] << 21
    reg[1] = reg[1] << 16
    if len(reg) == 3:
        reg[2] = reg[2] << 11
    b32 = format((op + sum(reg) + xo + oe + rc),"032b")
    return b32


def xs(string,binary):
    """Translate XS format"""
    op = binary[0] << 26
    xo = binary[1] << 1
    sh = 0
    rc = binary[2] 
    temp = re.findall(r'\d+', string) 
    reg = list(map(int, temp)) 
    reg[0] = reg[0] << 21
    reg[1] = reg[1] << 16
    reg[2] = reg[2] << 11
    b32 = format((op + sum(reg) + xo + rc + sh),"032b")
    return b32


def d(string,binary):
    """Translate D format"""
    op = binary << 26
    temp = re.findall(r'-?\d+', string) 
    reg = list(map(int, temp))
    nf = 0
    if((op >> 26)>30):
        if(reg[1]<0):
            nf = 1
            reg[1]  = -reg[1]
        reg[0] = reg[0] << 21
        reg[2] = reg[2] << 16
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
            b32 = b32 + b16
        else:
            reg[1] = reg[1]
            b32 = format((op + reg[0] + reg[2] +reg[1]),"016b")
    else:
        if(reg[2]<0):
            nf = 1
            reg[1]  = -reg[1]
        reg[0] = reg[0] << 21
        reg[1] = reg[1] << 16
        if nf:
            i=reg[2]
            k=0
            while i>1:
                i = i / 2
                k = k + 1
            reg[2] = twos_comp(reg[2],k)
            b16 = format(reg[2],"b")
            i=len(b16)
            while i <= 15:
                if i <= (k-1):
                    b16 = "0" + b16
                else:
                    b16 = "1" + b16
                i = i + 1
            b32 = format((op + reg[0] + reg[1]),"016b")
            b32 = b32 + b16
        else:
            reg[2] = reg[2]
            b32 = format((op + reg[0] + reg[2] +reg[1]),"032b")
    return b32


def ds(string,binary):
    """Translate DS format"""
    op = binary[0] << 26
    xo = binary[1] 
    temp = re.findall(r'-?\d+', string) 
    reg = list(map(int, temp))
    nf = 0
    if(reg[1]<0):
        nf = 1
        reg[1]  = -reg[1]
    reg[0] = reg[0] << 21
    reg[2] = reg[2] << 16
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
        b32 = b32 + b16 + xo
    else:
        reg[1] = reg[1] << 2
        xo = xo
        b32 = format((op + reg[0] + reg[2] + reg[1] + xo),"016b")
    return b32


def m(string,binary):
    """Translate M format"""
    op = binary[0] << 26
    rc = binary[1] 
    temp = re.findall(r'\d+', string) 
    reg = list(map(int, temp)) 
    reg[0] = reg[0] << 21
    reg[1] = reg[1] << 16
    reg[2] = reg[2] << 11
    reg[3] = reg[3] << 6
    reg[4] = reg[4] << 1
    b32 = format((op + sum(reg) + rc),"032b")
    return b32


def b(string,binary,label):
    """Translate B format"""
    op = binary[0] << 26
    aa = binary[1] << 1
    lk = binary[2]
    temp = re.findall(r'-?\d+', string) 
    reg = list(map(int, temp))
    reg[0] = reg[0] << 16
    line = string.split(",")[1].replace(",", "")
    line=line.lstrip()
    line=line.rstrip()
    line = label.get(line)
    line = line << 2
    b32 = format((op + reg[0] + line + lk + aa),"032b")
    return b32

    
def i(string,binary,label):
    po = binary[0] << 26
    aa = binary[1] << 1
    lk = binary[2] 
    line = string.split()[0]
    line = line.lstrip()
    line = line.rstrip()
    line = label.get(line)
    line = line << 2
    b32 = format((po + aa + lk + line),"032b")
    return b32

def translate(string,label,symtab):
    """Translating to a 32b instruction"""
    print(string)
    global B
    string=string.lstrip()
    instr = string.split(" ",1)
    b32 = "1"
    form = checkInstructionType.checkType(instr[0])
    binary = INST_TAB.get(instr[0])
    if form == 1 :
        b32 = x(instr[1],binary)
    elif form == 2 :
        b32 = xo(instr[1],binary)
    elif form == 3:
        b32 = xs(instr[1],binary)
    elif form == 4:
        b32 = d(instr[1],binary)
    elif form == 5:
        b32 = ds(instr[1],binary)
    elif form == 6:
        b32 = m(instr[1],binary)
    elif form == 7:
        b32 = b(instr[1],binary,label)
    elif form == 8:
        b32 = i(instr[1],binary,label)
    elif instr[0] == "sc":
        b32 = format(12,"032b")
    elif instr[0] == "la":
        chstr = instr[1].split(",")
        pos = chstr[1].split("(")
        pos[1] = pos[1].replace(")","")
        cstr = (str(chstr[0]) + "," + str(pos[0]) + "," + str(symtab.get(pos[1]) - 2 * B))
        b32 = d(cstr,INST_TAB.get("la"))
    elif(string == ".end"):
        b32 = "0"

    print(b32)
    return b32


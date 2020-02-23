import re


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
    return b32


def b(string,binary):
    """Translate B format"""
    #Please confirm if BD can be neg
    op = binary[0]
    aa = binary[1]
    lk = binary[2]
    temp = re.findall(r'-?\d+', string) 
    reg = list(map(int, temp))
    if(reg[2]<0):
        nf = 1
        reg[2]  = -reg[2]
    reg[0] = reg[0] << 5
    reg[1] = reg[1] << 10
    if nf:
        i = reg[2]
        k = 0
        while i>1:
            i = i / 2
            k = k + 1
        reg[2] = twos_comp(reg[2],k)
        b16 = format(reg[2],"b")
        i = len(b16)
        while i <= 13:
            if i <= (k-1):
                b16 = "0" + b16
            else:
                b16 = "1" + b16
            i = i + 1
        aa = format(aa,"b")
        lk = format(lk,"b")
        b32 = format((op + reg[0] + reg[2]),"016b")
        b32 = lk + aa + b16 + b32
    else:
        reg[2] = reg[2] << 15
        aa = aa << 29
        lk = lk << 30
        b32 = format((op + reg[0] + reg[2] + reg[1] + lk + aa),"016b")
    return b32

    
def i(string,binary):
    po = binary[0]
    aa = binary[1] << 29
    lk = binary[2] << 30
    temp = re.findall(r'\d+', string) 
    reg = list(map(int, temp))
    reg[0]=reg[0] << 5
    b32 = format((po + aa + lk + reg[0]),"032b")
    return b32


def translate(string,symtab):
    """Translating to a 32b instruction"""
    instr = string.split(" ",1)
    form = check_instruction_type(instr[0])
    binary = symtab.get(instr[0])
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
        b(instr[1],binary)
    elif form == 8:
        i(instr[1],binary)
import re


def x(str,binary):
    """Translaate X format"""
    op = binary[0]
    xo = binary[1]<<20
    rc = binary[2]<<30
    temp = re.findall(r'\d+', str) 
    reg = list(map(int, temp)) 
    reg[0] = reg[0] << 5
    reg[1] = reg[1] << 10
    if(len(reg) == 3):
        reg[2] = reg[2] << 15
    b32=format((op + sum(reg) + xo + rc),"032b")
    return b32


def xo(str,binary):
    """Translate XO format"""
    op = binary[0]
    oe = binary[1] << 20
    xo = binary[2] << 21
    rc = binary[3] << 30
    temp = re.findall(r'\d+', str) 
    reg = list(map(int, temp)) 
    reg[0] = reg[0] << 5
    reg[1] = reg[1] << 10
    if(len(reg) == 3):
        reg[2] = reg[2] << 15
    b32=format((op + sum(reg) + xo + oe + rc),"032b")
    return b32


#def xs(str,binary):


def d(str,binary):
    """Translate D format"""
    op = binary
    temp = re.findall(r'\d+', str) 
    reg = list(map(int, temp)) 
    reg[0]=reg[0]<<5
    reg[1]=reg[1]<<15
    reg[2]=reg[2]<<10
    print(sum(reg))
    print(reg[1])
    b32=format((op + sum(reg)),"032b")
    print(b32)
    return b32


def translate(str,symtab):
    """Translating to a 32b instruction"""
    instr = str.split(" ",1)
    form = check_instruction_type(instr[0])
    binary = symtab.get(instr[0])
    if(form == 1):
        x(instr[1],binary)
    elif(form == 2):
        xo(instr[1])
        
d("R3,-15(R5)",(31,28,0))
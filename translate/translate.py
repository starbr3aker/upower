import re


FORMTAB = {
           ("and","extsw","nand","or","xor",
           	"sld","srd","srad","cmp") : 1
           ("add","subf") : 2
           }
def translate(str,symtab)
    """Translating to a 32b instruction"""
    instr = str.split(" ",1)
    form = check_instruction_type(instr[0])
    binary = symtab.get(instr[0])
    if(FORMTAB.get(instr[0]) == 1):
        op = binary[0]
        xo = binary[1]
        rc = binary[2]
    elif(FORMTAB.get(instr[0]) == 2):
        op = binary[0]
        oe = binary[1]
        xo = binary[2]
        rc = binary[3]
    
def instructionType(str):
    """ Determines if the ASM instruction is a comment or asn assembler directive or a label or 
     and instruction """

    str=str.split()
    if(str[0]=="#"):
        return "Comment"
    elif(str[0][0]=="."):
        return "Assembler Directive"
    elif(str[0][-1]==":"):
        return "Label"
    else:
        return "Instruction"

def mnemonic(str):
    """ Returns the mnemonic of the ASM instruction """
    return str[0]

def inputOperands(str):
    """ Returns the input operands mentioned in the ASM instruction """

def outputOperands(str):
    """ Returns the output operands mentioned in the ASM instruction """

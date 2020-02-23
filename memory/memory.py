import sys
sys.path.append('../')
from readasm import readasm

# static pointer points to the beginning of the static data segment
global stackp
stackp = 0x0000_0000_1000_0000

def makemap(listofvars):
    """Make a map from a list of variable names. Temp solution for memory"""
    map = {i: 0 for i in listofvars}
    print(map)
    return map


def insert(map, variables):
    """Insert into the memory map. Temp solution for memory"""
    for variable in variables:
        map[variable] = stackp
        stackp += 4
        if(stackp>=0x0000_0000_1800_0000):
            print("Static data segment is full.")
            exit()

    return map


def fetch(map, variables, variable):
    """Fetch from the memory map. Temp solution for memory"""
    for address in map:
        if (address==variable):
            return variables[variable]
        else:
            continue
    # in case the label does not exist in the data segment
    return None

def dataMap(data):
    variables=dict()
    listoflabels=list()
    # variable is a dictionary that contains the label and its value
    for i in data:
        i=i.split()
        label=i[0].split(':')[0]
        listoflabels.append(label)
        value=i[2]
        if(value.isdigit):
            variables[label]=int(value)
        else:
            variables[label]=value
    return variables, listoflabels
        

def initialise():
    """Main memory implementation with dictionary. Isn't faithful recreation of memory because of RAM constraints."""
    A = 0x0000_0000_0000_0000
    B = 0x0000_0000_0040_0000
    C = 0x0000_0000_1000_0000
    D = 0x0000_0000_1800_0000
    E = 0x0000_003F_FFFF_FFF0
    pc = B
    sp = E
    # textend = 2 * B
    # staticend = 3 * B
    sp = 4 * B

    reserved = {i: 0 for i in range(A, B, 4)}
    print("reserved memory initialised")
    text = {i: 0 for i in range(B, C, 4)}
    print("text memory initialised")
    static = {i: 0 for i in range(C, D, 4)}
    print("static memory initialised")
    dynamic = {i: 0 for i in range(D, E, 4)}
    print("dynamic memory initialised")

    return (pc, sp, reserved, text, static, dynamic)

data, text=readasm('../asm_files/2.s')

variables, listoflabels = dataMap(data)
makemap(listoflabels)
insert(map, variables)

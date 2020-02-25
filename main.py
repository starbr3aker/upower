from readasm import readasm  # noqa: F401
from main import syscall
import checkInstructionType  # noqa: F401
import memory  # noqa: F401

pc = 0
textstart = 0
textend = 0
staticstart = 0
staticend = 0
dynamicstart = 0
dynamicend = 0
sp = 0
reserved = {}
text = {}
static = {}
dynamic = {}
register = {}
symtab = {}
labels = []
dtype = []
values = []

SymTab_Lable = {}

class Instruction:
    def __init__(self, mnemnomic, output, input, address):
        self.mnemnomic = mnemnomic
        self.output = output
        self.input = input
        self.address = address

    def readAddres(self)
        return self.address

Instruction_Set = []


def initialise():
    """Main memory implementation with dictionary. Isn't faithful recreation of memory because of RAM constraints."""
    A = 0x0000_0000_0000_0000
    B = 0x0000_0000_0040_0000

    global pc
    pc = B
    global staticend
    staticend = 2 * B
    global sp
    sp = 4 * B
    global staticstart
    staticstart = 2 * B
    global dynamicstart
    dynamicstart = 3 * B
    global dynamicend
    dynamicend = 3 * B

    global textstart
    global textend
    textstart = 1 * B
    textend = 1 * B

    global reserved
    reserved = {i: 0 for i in range(A, B)}
    print("reserved memory initialised")
    global text
    text = {i: 0 for i in range(B, 2 * B)}
    print("text memory initialised")
    global static
    static = {i: 0 for i in range(2 * B, 3 * B)}
    print("static memory initialised")
    global dynamic
    dynamic = {i: 0 for i in range(3 * B, 4 * B)}
    print("dynamic memory initialised")

    global register
    register = {"r{}".format(i): 0 for i in range(32)}
    print("32 registers ready")

def addToSymTab(lable, type, address):
    if(type): #If its a lable
        SymTab_Lable[lable] = address

def RedSymTab_Lable(lable): # Returns the memory of the lable
    return SymTab_Lable[lable]

initialise()


def makesymboltable(path):
    global staticstart
    global staticend
    data, _ = readasm(path)
    global labels
    global dtype
    global values
    global symtab
    for i in data:
        labels.append(i.split(maxsplit=2)[0].replace(":", ""))
        dtype.append(i.split(maxsplit=2)[1].replace(".", ""))
        values.append(i.split(maxsplit=2)[2])

    # print(labels)
    # print(dtype)
    # print(values)

    for i in range(len(labels)):
        if dtype[i] == "word":
            if len(values[i].split(",")) > 1:
                print(values[i])
                valueslist = values[i].split(",")
                for j in range(len(valueslist)):
                    static[staticend] = int(valueslist[j].strip())
                    print(static[staticend])
                    staticend = staticend + 1
            else:
                static[staticend] = int(values[i])
                symtab.update({labels[i]: staticend})
                staticend = staticend + 1
        elif dtype[i] == "asciiz":
            values[i] = values[i].replace('"', "")
            static[staticend] = len(values[i])
            symtab.update({labels[i]: staticend})
            for j in range(len(values[i])):
                static[staticend] = values[i][j]
                staticend = staticend + 1

    for i in range(len(text)):
        line = text[i]
        if line[0] != '#' : #Ignore Comments
            if ":" in line: #Chk for Lable
                lable = line.split(":",1)
                lable[1] = lable[1].strip()
                lable[0] = lable[0].strip()
                type = not lable[1];
                addToSymTab(lable[0], type, i)
            else: #Instructions
                line = line.replace(","," ")
                line = line.split(" ")
                line = [i for i in line if i]
                #print(line)
                mnemnomic = line[0]
                output = line[1]
                inp = []
                for i in range (2, len(line)):
                    inp.append(line[i])

                Instruction_Set.append(Instruction(mnemnomic, output, input, i))

    # print(symtab)
    # for i in range(len(labels)):
    #     print(static[symtab[labels[i]]])

    return symtab


# makesymboltable("asm_files/1.s")


def storeintoregister(address, value):
    global register
    register[address] = value
    return None


def readfromregister(address):
    return register[address]


def readfromlabel(label, address):
    """Read value from label, and store that value into the address in register"""
    global dtype
    global labels
    global register
    global symtab
    idx = 0  # index of label in labels

    register[address] = symtab[label]

    return dtype[idx]


def exec(line, pos):
    instr = line.split()[0]
    global register
    global symtab
    global static
    # print(instr)
    # print(line)
    if instr == "add":
        res = line.split()[1].replace(",", "")
        t1 = line.split()[2].replace(",", "")
        t2 = line.split()[3].replace(",", "")
        t1 = register[t1]
        t2 = register[t2]
        register[res] = t1 + t2
        print("{} + {} = {}, at {}".format(t1, t2, t1 + t2, res))
    if instr == "addi":
        res = line.split()[1].replace(",", "")
        t1 = line.split()[2].replace(",", "")
        t2 = line.split()[3].replace(",", "")
        t1 = register[t1]
        t2 = int(t2)
        register[res] = t1 + t2
        print("{} + {} = {}, at {}".format(t1, t2, t1 + t2, res))
    if instr == "ld" or instr == "lhz":
        line = line.replace(",", "")
        target = line.split()[1]
        print(line)
        loc = line.split()[2]
        disp = loc.split("(")[0]
        loc = loc.split("(")[1].replace(")", "")
        if loc in symtab.keys():
            register[target] = static[symtab[loc] + int(disp)]
        else:
            register[target] = static[register[loc] + int(disp)]
        print("{} is now {}/*".format(target, register[target]))
    if instr == "std":
        line = line.replace(",", "")
        source = line.split()[1]
        print(line)
        dest = line.split()[2]
        disp = dest.split("(")[0]
        dest = dest.split("(")[1].replace(")", "")
        static[symtab[dest] + int(disp)] = register[target]
        print(
            "{} is now {}/*".format(
                symtab[dest] + int(disp), static[symtab[source] + int(disp)]
            )
        )

    if instr == "sc":
        syscall(register[2], regdict, *args)
        
    return pos
def execute(path):
    symtab = makesymboltable(path)  # noqa: F841
    _, text = readasm(path)
    global register
    register["r2"] = 3
    register["r3"] = 4

    for i in range(len(Instruction_Set)):
         i = exec(text[Instruction_Set[i].readAddres()], i);

    # for line in text:
    #
    #     exec(line)

execute("asm_files/test.s")

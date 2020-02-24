from readasm import readasm  # noqa: F401
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
        labels.append(i.split()[0].replace(":", ""))
        dtype.append(i.split()[1].replace(".", ""))
        values.append(i.split()[2])

    # print(labels)
    # print(dtype)
    # print(values)

    for i in range(len(labels)):
        if dtype[i] == "word":
            static[staticend] = values[i]
            symtab.update({labels[i]: staticend})
            staticend = staticend + 1
        elif dtype[i] == "asciiz":
            values[i] = values[i].replace('"', "")
            static[staticend] = len(values[i])
            symtab.update({labels[i]: staticend})
            for j in range(len(values[i])):
                static[staticend] = values[i][j]
                staticend = staticend + 1

    # print(symtab)

    return symtab


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


def exec(line):
    instr = line.split()[0]
    global register
    global symtab
    global static
    # print(instr)
    print(line)
    if instr == "add":
        res = line.split()[1].replace(",", "")
        t1 = line.split()[2].replace(",", "")
        t2 = line.split()[3].replace(",", "")
        t1 = register[t1]
        t2 = register[t2]
        register[res] = t1 + t2
        print("r{} + r{} = {}, at r{}".format(t1, t2, t1 + t2, res))
    if instr == "ld" or instr == "lhz":
        line = line.replace(",", "")
        target = line.split()[1]
        print(line)
        loc = line.split()[2]
        disp = loc.split("(")[0]
        loc = loc.split("(")[1].replace(")", "")
        print("{} {} {}/*".format(target, disp, loc))


def execute(path):
    symtab = makesymboltable(path)  # noqa: F841
    _, text = readasm(path)
    for line in text:
        exec(line)


execute("asm_files/test.s")

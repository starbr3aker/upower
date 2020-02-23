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
reg = {}


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

    global reg
    reg = {i: 0 for i in range(32)}
    print("32 registers ready")


initialise()


def makesymboltable(path):
    global staticstart
    global staticend
    data, text = readasm(path)
    labels = []
    dtype = []
    values = []
    symtab = {}
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


makesymboltable("asm_files/1.s")

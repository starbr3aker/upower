from readasm import readasm  # noqa: F401
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

labeltable = {}


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
    register = {"{}".format(i): 0 for i in range(32)}
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

    # print(symtab)
    # for i in range(len(labels)):
    #     print(static[symtab[labels[i]]])

    return symtab


# makesymboltable("asm_files/1.s")


def makelabeltable(path):
    global text
    data, textlines = readasm(path)

    for line in textlines:
        if ":" in line:
            text.update({line: textlines.index(line) + 1})


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
    # print(line)
    if instr == "add":
        res = line.split()[1].replace(",", "")
        t1 = line.split()[2].replace(",", "")
        t2 = line.split()[3].replace(",", "")
        t1 = register[t1]
        t2 = register[t2]
        register[res] = t1 + t2
        print(">>{} + {} = {}, at register{}".format(t1, t2, t1 + t2, res))
    if instr == "addi":
        res = line.split()[1].replace(",", "")
        t1 = line.split()[2].replace(",", "")
        t1 = register[t1]
        t2 = line.split()[3].replace(",", "")
        if t2 in symtab.keys():
            register[res] = symtab[t2] + t1
            print(">>register {} ={} + {}".format(res, symtab[t2], t1))
        else:
            register[res] = t1 + int(t2)
            print(">>register {} = {} + {}".format(res, t1, t2))

    if instr == "ld" or instr == "lhz":
        line = line.replace(",", "")
        target = line.split()[1]
        loc = line.split()[2]
        disp = loc.split("(")[0]
        loc = loc.split("(")[1].replace(")", "")
        if loc in symtab.keys():
            register[target] = symtab[loc] + int(disp)
        else:
            register[target] = static[register[loc] + int(disp)]
        print(">>register {} is now {}/*".format(target, register[target]))
    if instr == "std":
        line = line.replace(",", "")
        source = line.split()[1]
        dest = line.split()[2]
        disp = dest.split("(")[0]
        dest = dest.split("(")[1].replace(")", "")
        if dest in symtab.keys():
            static[symtab[dest] + int(disp)] = register[source]
            print(
                ">>Address {} is now {}/*".format(
                    symtab[dest] + int(disp), static[symtab[source] + int(disp)]
                )
            )
        else:
            static[register[dest] + int(disp)] = register[source]
            print(
                ">>Address {} is now {}/*".format(
                    register[dest] + int(disp), static[register[dest] + int(disp)]
                )
            )
    if line == "sc LEV":
        print(">>Safely exiting the program...")


def execute(path):
    global symtab
    symtab = makesymboltable(path)
    _, text = readasm(path)
    for line in text:
        print(line)
        exec(line)


execute("asm_files/3.s")

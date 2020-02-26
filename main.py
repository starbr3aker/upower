from readasm import readasm  # noqa: F401

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
    global textmem
    textmem = {i: 0 for i in range(B, 2 * B)}
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
                # print(values[i])
                symtab.update({labels[i]: staticend})
                valueslist = values[i].split(",")
                for j in range(len(valueslist)):
                    static[staticend] = int(valueslist[j].strip())
                    # print(static[staticend])
                    staticend = staticend + 1
            else:
                static[staticend] = int(values[i])
                symtab.update({labels[i]: staticend})
                staticend = staticend + 1
        elif dtype[i] == "asciiz":
            values[i] = values[i].replace('"', "")
            static[staticend] = len(values[i])
            symtab.update({labels[i]: staticend})
            staticend = staticend + 1
            for j in range(len(values[i])):
                static[staticend] = values[i][j]
                staticend = staticend + 1

    print(symtab)
    # for i in range(len(labels)):
    #     print(static[symtab[labels[0]]])

    return symtab


def makelabeltable(path):
    global textmem
    data, textlines = readasm(path)

    for line in textlines:
        if ":" in line:
            textmem.update({line.replace(":", ""): textlines.index(line) + 1})
            print({line.replace(":", ""): textlines.index(line) + 1})


def extractstring(address):
    """Takes a string from a dictionary (memory unit). The length of the string must be in the location of address"""
    global static
    # print(static[int(address)])
    len = int(static[address])
    string = ""
    for i in range(len):
        string = string + str(static[address + i + 1])

    return string


def syscall(instruction, *args):
    """Executes a system call. Corresponding dictionary of registers is passed, with the addresses of the arguments."""
    global register
    global static
    print("Trigger syscall{}".format(instruction))
    if instruction == 1:
        return print("Printing integer value {}".format(register[args[0]]))
    elif instruction == 4:
        string = extractstring(register[args[0]])
        print("Printing string\n{}".format(string))
    elif instruction == 10:
        print("Exiting.")
    else:
        return print("This path hasn't been programmed yet.")


def exec(line, i):
    instr = line.split()[0]
    global register
    global symtab
    global static
    global staticstart
    # print(instr)
    # print(line)

    # print(static[8388608])
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
        t1 = int(t1)
        t2 = line.split()[3].replace(",", "")
        register[res] = int(t1) + register[t2]
        print(">>register {} = {} + r{} = {}".format(res, t1, t2, register[res]))
    if instr == "la":
        res = line.split()[1].replace(",", "")
        t1 = line.split()[2].replace(",", "")
        t1 = register[t1]
        t2 = line.split()[3].replace(",", "")
        if t2 in symtab.keys():
            register[res] = symtab[t2] + t1
            print(">>register {} ={} + {}".format(res, symtab[t2], t1))
        else:
            print("Error: Label not found")

    if instr == "ld" or instr == "lhz":
        line = line.replace(",", "")
        target = line.split()[1]
        loc = line.split()[2]
        disp = loc.split("(")[0]
        loc = loc.split("(")[1].replace(")", "")
        # print((target))
        # print((loc))
        # print(type(int(disp)))
        if loc in symtab.keys():
            register[target] = symtab[loc] + int(disp)
        else:
            print(register[target])
            if register[loc] + int(disp) < staticstart:
                register[target] = 0
                print("Error, access out of bounds.")
            else:
                register[target] = static[register[loc] + int(disp)]
        print(">>register {} is now {}".format(target, register[target]))
    if instr == "std":
        line = line.replace(",", "")
        source = line.split()[1]
        dest = line.split()[2]
        disp = dest.split("(")[0]
        dest = dest.split("(")[1].replace(")", "")
        if dest in symtab.keys():
            static[symtab[dest] + int(disp)] = register[source]
            print(
                ">>Address {} is now {}".format(
                    symtab[dest] + int(disp), static[symtab[source] + int(disp)]
                )
            )
        else:
            static[register[dest] + int(disp)] = register[source]
            print(
                ">>Address {} is now {}".format(
                    register[dest] + int(disp), static[register[dest] + int(disp)]
                )
            )
    if instr == "sc":
        parameter = register["0"]
        syscall(parameter, "3")
    if instr == "bca":
        print(line)
        line = line.replace(",", "")
        # bo = line.split()[1].replace(",", "")
        bl = line.split()[1].replace(",", "")
        addr = line.split()[2].replace(",", "")
        # bo = register[bo]
        print("Going to label{} ".format(addr))
        if bl == "28" and register["7"] == 1:
            return textmem.get(addr)
        elif bl == "29" and register["7"] == 2:
            return textmem.get(addr)
        elif bl == "30" and register["7"] == 4:
            return textmem.get(addr)
    if instr == "b":
        ln = line.split()[1]
        print("Going to label " + ln)
        return textmem.get(ln)
    if instr == "cmp":
        ra = line.split()[3].replace(",", "")
        rb = line.split()[4].replace(",", "")
        bf = line.split()[1].replace(",", "")
        # print(ra)
        # print(rb)
        # print(bf)
        ra = register[ra]
        rb = register[rb]
        # print(ra)
        # print(rb)
        if bf == "7" and ra < rb:
            register["7"] = 1
        if bf == "7" and ra > rb:
            register["7"] = 2
        if bf == "7" and ra == rb:
            register["7"] = 4
        print(register["7"])

    return i + 1


def execute(path):
    global symtab
    symtab = makesymboltable(path)
    makelabeltable(path)
    _, text = readasm(path)
    # print(symtab)
    i = 0
    while i in range(len(text)):
        print(text[i])
        i = exec(text[i], i)


execute("asm_files/4.s")

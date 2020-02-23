def extractstring(dicto, address):
    len = int(dicto[address])
    string = ""
    for i in range(len):
        string = string + str(dicto[address + i])

    return string


def syscall(instruction, *args):
    pass

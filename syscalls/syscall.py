def extractstring(dicto, address):
    """Takes a string from a dictionary (memory unit). The length of the string must be in the location of address"""
    len = int(dicto[address])
    string = ""
    for i in range(len):
        string = string + str(dicto[address + i + 1])

    return string


def syscall(instruction, regdict, *args):
    """Executes a system call. Corresponding dictionary of registers is passed, with the addresses of the arguments."""

    if instruction == 1:
        return print("Printing integer value {}".format(regdict[args[0]]))
    else:
        return print("This path hasn't been programmed yet.")

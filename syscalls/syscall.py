def extractstring(dicto, address):
    """Takes a string from a dictionary (memory unit). The length of the string must be in the location of address"""
    len = int(dicto[address])
    string = ""
    for i in range(len):
        string = string + str(dicto[address + i + 1])

    return string


def syscall(instruction, regdict, *args):
    """Executes a system call. Corresponding dictionary of registers is passed, with the addresses of the arguments."""

    global static
    if instruction == 1:
        return print("Printing integer value {}".format(regdict[args[0]]))
    elif instruction == 4:
        string = extractstring(static, args[0])
        print("Printing string {}".format(string))
    elif instruction == 10:
        print("Exiting.")
    else:
        return print("This path hasn't been programmed yet.")

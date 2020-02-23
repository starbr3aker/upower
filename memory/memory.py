def makemap(listofvars):
    """Make a map from a list of variable names. Temp solution for memory"""
    map = {i: 0 for i in listofvars}
    return map


def insert(map, varname, value):
    """Insert into the memory map. Temp solution for memory"""
    map[varname] = value
    return None


def fetch(map, varname):
    """Fetch from the memory map. Temp solution for memory"""
    return map[varname]


def initialise():
    """Main memory implementation with dictionary. Isn't faithful recreation of memory because of RAM constraints."""
    A = 0x0000_0000_0000_0000
    B = 0x0000_0000_0040_0000

    pc = B
    # textend = 2 * B
    # staticend = 3 * B
    sp = 4 * B

    reserved = {i: 0 for i in range(A, B, 4)}
    print("reserved memory initialised")
    text = {i: 0 for i in range(B, 2 * B, 4)}
    print("text memory initialised")
    static = {i: 0 for i in range(2 * B, 3 * B, 4)}
    print("static memory initialised")
    dynamic = {i: 0 for i in range(3 * B, 4 * B, 4)}
    print("dynamic memory initialised")

    return (pc, sp, reserved, text, static, dynamic)

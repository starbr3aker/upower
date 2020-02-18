def process(str):
    """Process string, removes comments and trailing spaces"""
    str = str.split("#", 1)[0].strip()
    return str


def readasm(path):
    """Return lists of data and text statements."""
    with open(str(path), "r") as asm_file:
        file = asm_file.readlines()
        pos1 = file.index(".data\n")
        pos2 = file.index(".text\n")

        data = list(filter(lambda x: x, [process(i) for i in file[pos1 + 1 : pos2]]))
        text = list(filter(lambda x: x, [process(i) for i in file[pos2 + 1 :]]))
        # print(data)
        # print(text)
        return (data, text)

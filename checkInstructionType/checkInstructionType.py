def mnemonic(str):
    """ Returns the mnemonic of the ASM instruction """
    return str.split()[0]


def checkType(str):
    """Returns type of instruction based on mnemonic"""

    lookup = {}
    lookup.update(
        dict.fromkeys(
            ["and", "extsw", "nand", "or", "xor", "sld", "srd", "srad", "cmp"], 1
        )
    )
    lookup.update(dict.fromkeys(["add", "subf"], 2))
    lookup.update(dict.fromkeys(["sradi"], 3))
    lookup.update(
        dict.fromkeys(
            [
                "addi",
                "addis",
                "andi",
                "ori",
                "xori",
                "lwz",
                "stw",
                "stwu",
                "lhz",
                "lha",
                "sth",
                "lbz",
                "stb",
                "cmpi",
            ],
            4,
        )
    )
    lookup.update(dict.fromkeys(["ld", "std"], 5))
    lookup.update(dict.fromkeys(["rlwinm"], 6))
    lookup.update(dict.fromkeys(["bc", "bca"], 7))
    lookup.update(dict.fromkeys(["b", "bl"], 8))
    lookup.update(dict.fromkeys(["sc"], 9))

    return lookup.get(mnemonic(str), "INSTR_NOT_FOUND")

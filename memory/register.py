def makemap(listofvars):
    map = {i: 0 for i in listofvars}
    return map


def insert(map, varname, value):
    map[varname] = value
    return None


def fetch(map, varname):
    return map[varname]

SymTab = {}

class Instruction:
    def __init__(self, mnemnomic, output, input, address):
        self.mnemnomic = mnemnomic
        self.output = output
        self.input = input
        self.address = address

    def readAddres(self)
        return self.address

Instruction_Set = []

def addToSymTab(lable, data, type, address):
    if(type): #If its a lable
        SymTab[lable] = address
        print(lable," : ",address)
    else:
        data = data.split(" ",1)
        data = data[1]
        print(lable, " : ", data)
        SymTab[lable] = data

def RedSymTab(lable): # Returns the memory or the
    return SymTab[lable]


def parseLine():
    for i in (data):
        line = data[i]
        if line[0] != '#' : #Ignore Comments
            if ":" in line: #Chk for Lable
                lable = line.split(":",1)
                lable[1] = lable[1].strip()
                lable[0] = lable[0].strip()
                type = not lable[1];
                addToSymTab(lable[0], lable[1], type, i)

    for i in range(len(text)):
        line = text[i]
        if line[0] != '#' : #Ignore Comments
            if ":" in line: #Chk for Lable
                lable = line.split(":",1)
                lable[1] = lable[1].strip()
                lable[0] = lable[0].strip()
                type = not lable[1];
                addToSymTab(lable[0], lable[1], type, i)
            else: #Instructions
                line = line.replace(","," ")
                line = line.split(" ")
                line = [i for i in line if i]
                #print(line)
                mnemnomic = line[0]
                output = line[1]
                inp = []
                for i in range (2, len(line)):
                    inp.append(line[i])

                Instruction_Set.append(Instruction(mnemnomic, output, input, i))

print(SymTab)
print(mnemnomic, inp, output)

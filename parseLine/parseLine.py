
class Instruction:
    def __init__(self, instruction):
        self.in

def addToSymTab(lable, data, type, add):

def chkLabel(line):

def parseLine():
    for i in (data):

    for i in range(len(text)):
        line = text[i]
        if line[0] != '#' : #Ignore Comments
            if ":" in line: #Chk for Lable
                lable = line.split(":",1)
                lable[1] = lable[1].strip()
                type = not lable[1];
                addToSymTab(lable[0], lable[1], type, i)
            else: #Instructions
                line = line.replace(","," ")
                line = line.split(" ")
                line = [i for i in line if i]
                #print(line)
                mnemnomic = line[0]
                output = line[1]
                for i in range (2, len(line)-2):
                    output[i-2] = line[i]

    print(mnemn, input, output);

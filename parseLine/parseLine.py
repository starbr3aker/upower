
def addToSymTab(lable, data, type, address):

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
                inp = []
                for i in range (2, len(line)-2):
                    inp.append(line[i])

    print(mnemn, inp, output);

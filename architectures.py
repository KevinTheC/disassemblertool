import os
import io
from pathlib import Path
import re
import args
#check if OPCODE matches
def _matchOPCode(rule,binary):
    bits = rule[(rule.split(":")[0].rfind('#')+1):rule.rfind(':')]
    bits = re.split(r'[()]', rule.split("#")[0])
    bits = list(filter(bool,bits))
    offsetBytes = int(re.split(r'[#:]', rule)[1])//8
    binaryString = binary.read(offsetBytes)
    print(binaryString)
    binary.seek(-1*offsetBytes,io.SEEK_CUR)
    for i in range(len(bits)//2):
        j = i*2
        if (binaryString[int(bits[j]):int(bits[j])+len(bits[j+1])]!=bits[j+1]):
            return False
    return True
def _readInstructions():
    curdir = os.getcwd()
    enddir = os.path.join(curdir,"standards")
    if os.path.exists(enddir) and os.path.isdir(enddir):
        return os.listdir(enddir)
    print("Directory \"standards\" in working directory does not exist or is empty.")
    exit()
class Architecture:
    _options = _readInstructions()
    def __init__(self, architecture):
        if not (architecture in Architecture._options):
            raise NotImplementedError
        self.architecture = architecture
    def __parseBinary(self,inBin,outputfile):
        rules = open(os.path.join(os.getcwd(),"standards",self.architecture),"r").readlines()
        rules = list(filter(lambda x: x,rules))
        flag = True
        while (inBin.readable()):
            if not flag:
                args.Args.onFail(inBin.read(8),outputfile)
                if (inBin.readable()):
                    inBin.seek(-4,io.SEEK_CUR)
                else:
                    break
            flag = True
            for i in range(len(rules)):
                #try:
                    if not _matchOPCode(rules[i],inBin):
                        flag = False
                    else:
                        Architecture._applyRule(self,rules[i],inBin,outputfile)
                #except Exception as e:
                    True#print(f"Exception occured in testing the ruleset of an Assembly Instruction: {rules[i]}")

    def _applyRule(self,rule,inBin,outputfile):
        offsetBytes = int(re.split(r'[#:]', rule)[1])//8
        binaryString = inBin.read(offsetBytes)
        #now that we have binary string, start applying the conversions
        stringarray = re.split(r'[>;]',(rule.split(":")[1]))
        for i in range(len(stringarray)//2):
            j = i*2
            currstring = binaryString[:int(stringarray[j])]
            binaryString = binaryString[int(stringarray[j]):]
            if (stringarray[j+1]=="register()"):
                outputfile.write(f"${int(currstring,2)}")
            elif (stringarray[j+1]=="decimal()"):
                outputfile.write(f"{int(currstring,2)}")
            elif (stringarray[j+1]=="hex()"):
                outputfile.write(f"0x{hex(int(currstring,2))}")
            elif (stringarray[j+1]=="address()"):
                outputfile.write(f"&{hex(int(currstring,2))}")
            else:
                outputfile.write(stringarray[j+1].strip('\"'))
            outputfile.write(" ")
        outputfile.write("\r\n")
    
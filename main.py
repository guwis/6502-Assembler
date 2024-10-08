import re
START_BYTE = 0x8000
currentByte = START_BYTE
currentLine = 0

labels ={}
defines = {}
inputASM = []
#Templates:

a = re.compile(r'^A$')
abs = re.compile(r'^\$(?P<highByte>\w\w)(?P<lowByte>\w\w)$')
absX = re.compile(r'^\$(?P<highByte>\w\w)(?P<lowByte>\w\w),X$')
absY = re.compile(r'^\$(?P<highByte>\w\w)(?P<lowByte>\w\w),Y$')
imm = re.compile(r'^#\$(?P<Byte>\w\w)$')
ind = re.compile(r'^\(\$(?P<highByte>\w\w)(?P<lowByte>\w\w)\)$')
indX = re.compile(r'^\(\$(?P<Byte>\w\w),X\)$')
indY = re.compile(r'^\(\$(?P<Byte>\w\w)\),Y$')
zpgrel = re.compile(r'^\$(?P<Byte>\w\w)$')#zpg and rel are the same
zpgX = re.compile(r'^\$(?P<Byte>\w\w),X$')
zpgY = re.compile(r'^\$(?P<Byte>\w\w),Y$')
impl = re.compile(r'^\$(?P<Byte>\w\w)$')

templates = [a,abs,absX,absY,imm,ind,indX,indY,zpgrel,zpgX,zpgY,impl]
templateDef = ["a","abs","absX","absY","imm","ind","indX","indY","zpgrel","zpgX","zpgY","impl"]

'''
templateSize1 = ["a","impl"]
templateSize2 = ["imm","indX","indY","zpgrel","zpgX","zpgY"]
templateSize3 = ["abs","absX","absY","ind"]
'''

##A accumulator; abs absolute; absX; absY; immediate #;
opcodes6502 = {
    "ADC":{"imm": "0x69","zpgrel": "0x65","zpgX":"0x75","abs":"0x6D","absX":"0x7D","absY":"79","indX":"0x61","indY":"0x71"},
    "AND":{"imm":"0x29","zpgrel":"0x25","zpgX":"0x35","abs":"0x2D","absX":"0x3D","absY":"0x39","indX":"0x21","indY":"0x31"},
    "ASL":{"a":"0x0A", "zpgrel":"0x06", "zpgX":"0x16", "abs":"0x0E", "absX":"0x1E"},
    "BCC":{"zpgrel":"0x90"},
    "BCS":{"zpgrel":"0xB0"},
    "BEQ":{"zpgrel":"0xF0"},
    "BIT":{"zpgrel":"0x24", "abs":"0x2C"},
    "BMI":{"zpgrel":"0x30"},
    "BNE":{"zpgrel":"0xD0"},
    "BPL":{"zpgrel":"0x10"},
    "BRK":{"impl":"0x00"},
    "BVC":{"zpgrel":"0x50"},
    "BVS":{"zpgrel":"0x70"},
    "CLC":{"impl":"0x18"},
    "CLD":{"impl":"0xD8"},
    "CLI":{"impl":"0x58"},
    "CLV":{"impl":"0xB8"},
    "CMP":{"imm":"0xC9", "zpgrel":"0xC5", "zpgX":"0xD5", "abs":"0xCD", "absX":"0xDD","absY":"0xD9","indX":"0xC1","indY":"0xD1"},
    "CPX":{"imm":"0xE0","zpgrel":"0xE4","abs":"0xEC"},
    "CPY":{"imm":"0xC0","zpgrel":"0xC4","abs":"0xCC"},
    "DEC":{"zpgrel":"0xC6","zpgX":"0xD6","abs":"0xCE","absX":"0xDE"},
    "DEX":{"impl":"0xCA"},
    "DEY":{"impl":"0x88"},
    "EOR":{"imm":"0x49","zpgrel":"0x45","zpgX":"0x55","abs":"0x4D","absX":"0x5D","absY":"0x59","indX":"0x41","indY":"0x51"},
    "INC":{"zpgrel":"0xE6","zpgX":"0xF6","abs":"0xEE","absX":"0xFE"},
    "INX":{"impl":"0xE8"},
    "INY":{"impl":"0xC8"},
    "JMP":{"abs":"0x4C","ind":"0x6C"},
    "JSR":{"abs":"0x20"},
    "LDA":{"imm":"0xA9","zpgrel":"0xA5","zpgX":"0xB5","abs":"0xAD","absX":"0xBD","absY":"0xB9","indX":"0xA1","indY":"0xB1"},
    "LDX":{"imm":"0xA2","zpgrel":"0xA6","zpgY":"0xB6","abs":"0xAE","absY":"0xBE"},
    "LDY":{"imm":"0xA0","zpgrel":"0xA4","zpgX":"0xB4","abs":"0xAC","absX":"0xBC"},
    "LSR":{"a":"0x4A","zpgrel":"0x46","zpgX":"0x56","abs":"0x4E","absX":"0x5E"},
    "NOP":{"impl":"0xEA"},
    "ORA":{"imm":"0x09","zpgrel":"0x05","zpgX":"0x15","abs":"0x0D","absX":"0x1D","absY":"0x19","indX":"0x01","indY":"0x11"},
    "PHA":{"impl":"0x48"},
    "PHP":{"impl":"0x08"},
    "PLA":{"impl":"0x68"},
    "PLP":{"impl":"0x28"},
    "ROL":{"a":"0x2A","zpgrel":"0x26","zpgX":"0x36","abs":"0x2E","absX":"3E"},
    "ROR":{"a":"0x6A","zpgrel":"0x66","zpgX":"0x76","abs":"0x6E","absX":"7E"},
    "RTI":{"impl":"0x40"},
    "RTS":{"impl":"0x60"},
    "SBC":{"imm":"0xE9","zpgrel":"0xE5","zpgX":"0xF5","abs":"0xED","absX":"0xFD","absY":"0xF9","indX":"0xE1","indY":"0xF1"},
    "SEC":{"impl":"0x38"},
    "SED":{"impl":"0xF8"},
    "SEI":{"impl":"0x78"},
    "STA":{"zpgrel":"0x85","zpgX":"0x95","abs":"0x8D","absX":"0x9D","absY":"0x99","indX":"0x81","indY":"0x91"},
    "STX":{"zpgrel":"0x86","zpgY":"0x96","abs":"0x8E"},
    "STY":{"zpgrel":"0x84","zpgX":"0x94","abs":"0x8C"},
    "TAX":{"impl":"0xAA"},
    "TAY":{"impl":"0xA8"},
    "TSX":{"impl":"0xBA"},
    "TXA":{"impl":"0x8A"},
    "TXS":{"impl":"0x9A"},
    "TYA":{"impl":"0x98"}
}
opcodeNames=["ADC","AND","ASL","BCC","BCS","BEQ","BIT","BMI","BNE","BPL","BRK","BVC","BVS","CLC","CLD","CLI","CLV","CMP","CPX","CPY","DEC","DEX","DEY","EOR","INC","INX","INY","JMP","JSR","LDA","LDX","LDY","LSR","NOP","ORA","PHA","PHP","PLP","ROL","ROR","RTI","RTS","SBC","SEC","SED","SEI","STA","STX","STY","TAX","TAY","TSX","TXA","TXS","TYA"]
pseudoNames=["DEFINE","DATA"]
#func
def getOpCode(opcode, addressingmode):
    return int(opcodes6502[opcode][addressingmode],16)

def getAddr(opField,operandField):
    labelSubstrings = re.split(r'#|\(|\)|,', operandField)
    operandField =''
    for sub in labelSubstrings:
        if sub in labels:
            sub = labels[sub]
        if sub != None:
            operandField += sub


    # now matching the address with the type of address
    addr = []
    j = 0
    while j < len(templates):
        match = templates[j].match(operandField)
        if match:
            try:
                addr.append(int(opcodes6502[opField][templateDef[j]], 16))
            except KeyError:
                print(opField + "doesn't have" + templateDef[j])
            if len(match.groupdict()) == 1:
                addr.append(int(match.groupdict()['Byte'], 16))
            if len(match.groupdict()) == 2:
                addr.append(int(match.groupdict()['lowByte'], 16))
                addr.append(int(match.groupdict()['highByte'], 16))
            break
        j += 1
    return addr

with open("input.txt", "r") as input:
    for line in input:
        inputASM.append(line)

with open("../../NES_Emulator/NES_Emulator/output.nes", "wb") as output:
    for line in inputASM:
        #increments current line count for error handling
        currentLine += 1
        #splits each line into its fields
        #4 fields: Label; OP Code; Operand; Comment
        fields = line.split()

        ##remove any thing after the first comment word
        i = 0
        while i < len(fields):
            if '0b' in fields[i]:
                index = fields[i].find("0b")
                fields[i] = fields[i][:index]+'$'+f'{hex(int(fields[i][(2+index):(10+index)], 2))[2:]:0>2}'+fields[i][(10+index):]
            if '/' in fields[i]:
                j = 0
                fieldsTemp = []
                while j < i:
                    fieldsTemp.append(fields[j])
                    j += 1
                fields = fieldsTemp
                break
            i += 1
        #Iterate through each field
        i = 0
        #the number of fields gives us a clue to the structure of the line
        #1 field - 1 opcode instruction impplied
        if len(fields) == 1:
            if fields[0] in opcodeNames:
                output.write(getOpCode(fields[0],"impl").to_bytes(1,"big"))
                currentByte += 1

        elif len(fields) == 2:
            if fields[0] in opcodeNames:
                lineBytes = getAddr(fields[0], fields[1])
                currentByte += len(lineBytes)
                for byte in lineBytes:
                    output.write(int(byte).to_bytes(1, "big"))
            #Right complex stuff - need specific pseduo code stuff!
            elif fields[1] in opcodeNames:
                labels[fields[0]] = '$'+f'{hex(currentByte)[2:]:0>4}'
                output.write(getOpCode(fields[1],"impl").to_bytes(1,"big"))
                #do pseudo stuff
        elif len(fields) == 3:
            if fields[0] in opcodeNames:
                lineBytes = getAddr(fields[0], fields[1])
                currentByte += len(lineBytes)
                for byte in lineBytes:
                    output.write(int(byte).to_bytes(1, "big"))
            if fields[1] in pseudoNames:
                labels[fields[0]] = '#$'+f'{hex(int(fields[2][1:],16))[2:]:0>2}'
                print("PSEUDO CODE!")
            if fields[1] in opcodeNames:
                labels[fields[0]] = '$'+f'{hex(currentByte)[2:]:0>4}'
                lineBytes = getAddr(fields[1], fields[2])
                currentByte += len(lineBytes)
                for byte in lineBytes:
                    output.write(int(byte).to_bytes(1, "big"))
    print("done!")

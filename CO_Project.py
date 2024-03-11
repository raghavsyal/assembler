def binary_conversion(number):
    if number >= 0:
        if number>(2**31)-1:
            print("Number out of Range")
            s='-1'
            return s

        q = number
        s = ""
        while q != 0:
            r = q%2
            s = s + str(r)
            q = q//2
        s = s[::-1]
        filler = 32 - len(s)
        
        s = filler*"0" + s
        return s
    else:
        if abs(number)>(2**31):
            print("Number out of Range")
            s='-1'
            return s
        z = abs(number)
        s = ""
        cnt = 1
        temp = z
        while temp != 0:
            cnt += 1
            temp = temp//2
        q = (2**cnt) - z
        while q != 0:
            r = q%2
            s = s + str(r)
            q = q//2
        s = s[::-1]
        filler = 32 - len(s)
        s = filler*"1" + s
        return s


#finish these functions
def R(rd, rs1, rs2,f3,f7,opc):  
    str1 = str(f7) + str(rs2) + str(rs1) + str(f3) + str(rd) + str(opc)
    return str1

def I(ra, rs1, imm, f3, opc):
    num = str(binary_conversion(int(imm)))   
    if num=='-1':
        return num          
    num = num[::-1]
    num = num[0:12]
    num = num[::-1]
    str1 = num + str(rs1) + str(f3)+ str(ra)+str(opc)
    return str1

def S(rd,rs1,imm,f3,opc):
    num = str(binary_conversion(int(imm)))         #[11:5] [4:0]
    if num=='-1':
        return num
    num = num[::-1]
    num1 = num[5:12]
    num1 = num1[::-1]
    num2 = num[0:5]
    num2 = num2[::-1]
    str1 = num1 + str(rd) + str(rs1)+ str(f3)+str(num2)+str(opc)
    return str1


def B(rs1, rs2, imm, f3, opc):                                   #0000 0000 0000 1100 1000    #imm[12|10 : 5]    #0000110
    num = str(binary_conversion(int(imm)))
    if num=='-1':
        return num
    num = num[::-1]
    num1 = num[5:11] + num[12]
    num1 = num1[::-1]
    num2 = num[1:5] + num[11]
    num2 = num2[::-1]
    str1 = num1 + str(rs2) + str(rs1) + str(f3) + num2 + str(opc)
    return str1

def U(rd, imm, opc):
   num = str(binary_conversion(int(imm)))
   if num=='-1':
        return num
   num = num[::-1]
   num = num[12:]
   str1 = num + str(rd) + str(opc)
   return str1

def J(rd, imm, opc):
    num = str(binary_conversion(int(imm)))
    if num=='-1':
        return num
    num = num[::-1]
    num = num[12:20] + num[11] + num[1:11] + num[20]
    num = num[::-1]
    str1 = num + str(rd) + str(opc)
    return str1

def assembler(instructions,function_opcodes,reg_binary,label_dict):
    cnt = -1
    function_call = {
        'R' : R,
        'I' : I,
        'S' : S,
        'B' : B,
        'U' : U,
        'J' : J
    }
    with open('outputfinal.txt', 'w') as f:
        cnt += 1
        for i in instructions:
            if not i.strip():      #skipping empty line
                continue
            try:
                # Split the instruction into its components
                opcode, rest = i.split(" ",1)
            except ValueError:
                print("Error: Invalid instruction format:", i)
                continue
            
            try:
                type,func_code3,func_code7,op = tuple(function_opcodes.get(opcode))
                if type is None:
                    print("Error: Unknown opcode:", opcode)
                    continue
                elif type == 'R':
                    dest_reg,source_reg1,source_reg2 = rest.split(",")
                    binary_rep = function_call[type](reg_binary[dest_reg],reg_binary[source_reg1],reg_binary[source_reg2],func_code3,func_code7,op)
                elif type == "I":
                    if opcode == "lw":       #different formatting for lw     #lw a5,20(s1)
                        address_reg, rem = rest.split(",")
                        imm,source_reg1 = rem.split("(",1)
                        source_reg1 = source_reg1[:-1]
                    else:
                        address_reg,source_reg1,imm = rest.split(",")
                    binary_rep = function_call[type](reg_binary[address_reg],reg_binary[source_reg1],imm,func_code3,op)
                elif type == "S":                
                    data_reg, rem = rest.split(",")
                    imm,source_reg = rem.split("(",1)
                    source_reg = source_reg[:-1]
                    binary_rep = function_call[type](reg_binary[data_reg],reg_binary[source_reg],imm,func_code3,op)
                elif type == "B":
                    source_reg1,source_reg2,imm = rest.split(",")
                    try:
                        a = int(imm)
                    except:
                        string = (cnt*4) - int(label_dict.get(imm))
                        imm = str(string)
                    finally:
                        binary_rep = function_call[type](reg_binary[source_reg1],reg_binary[source_reg2],imm,func_code3,op)
                elif type == "U":
                    dest_reg,imm = rest.split(",")
                    binary_rep = function_call[type](reg_binary[dest_reg],imm,op)
                elif type == "J":
                    dest_reg,imm = rest.split(",")
                    binary_rep = function_call[type](reg_binary[dest_reg],imm,op)
                else:
                    print('Unknown Type')
                    continue
                if binary_rep=='-1':
                    continue
                
                f.write('{}\n'.format(binary_rep))

            except:                 #for error in assigning value to variables while splitting(chk name of error)
                print("Incorrect format")
                continue
            
instructions = []      #to be taken from text file
with open('input.txt', 'r') as file:
    instructions = file.readlines()  
    for i in  range(len(instructions)-1):
        instructions[i] = instructions[i][:-1]
        instructions[i] = instructions[i].strip()
    label_dict = {}
    pc = -1
    for i in range(len(instructions)):
        pc += 1
        if ':' in instructions[i]:
            label,instruction=instructions[i].split(":",1)
            instructions[i] = instruction.lstrip()
            label_dict[label] = pc*4


opcodes_dict = { 
    'add': ('R','000','0000000','0110011'),
    'sub': ('R','000','0100000','0110011'),
    'slt': ('R','010','0000000','0110011'),
    'sltu': ('R','011','0000000','0110011'),
    'xor': ('R','100','0000000','0110011'),          # R-Type
    'sll': ('R','001','0000000','0110011'),
    'srl': ('R','101','0000000','0110011'),
    'or': ('R','110','0000000','0110011'),
    'and': ('R','111','0000000','0110011'),

    'lw' : ('I','010',None,'0000011'),
    'addi' : ('I','000',None, '0010011'),          # I-Type
    'sltiu' : ('I','011',None, '0010011'),
    'jalr' : ('I','000',None, '1100111'),

    'sw' : ('S','010',None,'0100011'),        # S-Type

    'beq' : ('B','000',None,'1100011'),
    'bne' : ('B','001',None,'1100011'),
    'bge' : ('B','101',None,'1100011'),
    'bgeu' : ('B','111',None,'1100011'),      # B-Type
    'blt' : ('B','100',None,'1100011'),
    'bltu' : ('B','110',None,'1100011'),

    'auipc' : ('U',None,None,'0010111'),     # U-Type
    'lui' : ('U',None,None,'0110111'),

    'jal' :('J',None,None,'1101111')      # J-Type
}

register_dict = { 
    'zero':'00000',  
    'ra':'00001', 
    'sp':'00010',    
    'gp':'00011',
    'tp':'00100',
    't0':'00101',
    't1':'00110',
    't2':'00111',
    's0':'01000',
    's1':'01001',
    'a0':'01010',
    'a1':'01011',
    'a2':'01100',
    'a3':'01101',
    'a4':'01110',
    'a5':'01111',
    'a6':'10000',
    'a7':'10001',
    's2':'10010',
    's3':'10011',
    's4':'10100',
    's5':'10101',
    's6':'10110',
    's7':'10111',
    's8':'11000',
    's9':'11001',
    's10':'11010',
    's11':'11011',
    't3':'11100',
    't4':'11101',
    't5':'11110',
    't6':'11111',
}
    
assembler(instructions,opcodes_dict, register_dict,label_dict)

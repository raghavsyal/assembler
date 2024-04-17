def sext(imm):
    if imm[0] == 0:
        while len(imm)<32 :
            imm = '0' + imm
        return imm
    while len(imm) < 32:
        imm = '1' + imm
    return imm
def decimaltobinary(num):
    num=int(num)
    if num >= 0:
        a = num
        s = ""
        while a != 0:
            b = a%2
            s = s + str(b)
            a = a//2
        s = s[::-1]
        filler = 32 - len(s)
        if filler < 0:
            print("number out of Range")
            s='-1'
            return s
        s = filler*"0" + s
        return s
    else:
        z = abs(num)
        s = ""
        cnt = 1
        temp = z
        while temp != 0:
            cnt += 1
            temp = temp//2
        a = (2**cnt) - z
        while a != 0:
            b = a%2
            s = s + str(b)
            a = a//2
        s = s[::-1]
        filler = 32 - len(s)
        if filler < 0:
            print("Number out of Range")
            s='-1'
            return s
        s = filler*"1" + s
        return s
def signed_conversion(imm):
    if imm[0] == '1':
        flipped_bits = ''.join('1' if bit == '0' else '0' for bit in imm)
        return -(int(flipped_bits, 2) + 1)
    else:
        return int(imm, 2)

def unsigned_conversion(imm):
    return int(imm, 2)

def beq(rs1, rs2, imm, pc):
    rs1 = sext(rs1)
    rs2 = sext(rs2)
    rs1 = signed_conversion(rs1)
    rs2 = signed_conversion(rs1)
    imm = signed_conversion(imm)
    if rs1 == rs2:
        pc += imm
    else:
        pc += 4
    return pc

def bne(rs1, rs2, imm, pc):
    rs1 = sext(rs1)
    rs2 = sext(rs2)
    rs1 = signed_conversion(rs1)
    rs2 = signed_conversion(rs1)
    imm = signed_conversion(imm)
    if rs1 != rs2:
        pc += imm
    else:
        pc += 4
    return imm

def bge(rs1, rs2, imm, pc):
    rs1 = sext(rs1)
    rs2 = sext(rs2)
    rs1 = signed_conversion(rs1)
    rs2 = signed_conversion(rs1)
    imm = signed_conversion(imm)
    if rs1 >= rs2:
        pc += imm
    else:
        pc += 4
    return pc

def blt(rs1, rs2, imm, pc):
    rs1 = sext(rs1)
    rs2 = sext(rs2)
    rs1 = signed_conversion(rs1)
    rs2 = signed_conversion(rs1)
    imm = signed_conversion(imm)
    if rs1 < rs2:
        pc += imm
    else:
        pc += 4
    return pc
def B(i, pc, reg_dic):
    imm = i[0] + i[24] + i[1:7] + i[20:24]
    imm = sext(imm)
    func3 = i[-15:-13]
    rs1 = i[-20:-15]
    rs2 = i[-25:-20]
    if func3 == "000":
        pc = beq(reg_dic[rs1], reg_dic[rs2], imm, pc)
    if func3 == "001":
        pc = bne(reg_dic[rs1], reg_dic[rs2], imm, pc)
    if func3 == "100":
        pc = blt(reg_dic[rs1], reg_dic[rs2], imm, pc)
    if func3 == "101":
        pc = bge(reg_dic[rs1], reg_dic[rs2], imm, pc)
    return pc

def R(i, pc, reg_dict):
    #try to create this
    ''''''

def lw(rd, rs1, imm, pc, reg_dic, mem_dic):
    rs1 = sext(rs1)
    rs1 = signed_conversion(rs1)
    imm = signed_conversion(imm)               #check for rs1 + imm overflow
    reg_dic[rd] = mem_dic[rs1+imm]             #if binary value not 32 bits, you need to sign extend
    return pc + 4
def addi(rd, rs1, imm, pc):
    rs1 = sext(rs1)
    rs1 = signed_conversion(rs1)
    imm = signed_conversion(imm)
    reg_dic[rd] = decimaltobinary(rs1 + imm)   #check for rs1 + imm overflow
    return pc + 4

def jalr(rd, x6, imm, pc):
    reg_dic[rd] = pc + 4
    x6 = sext(x6)
    x6 = signed_conversion(x6)
    imm = signed_conversion(imm)
    pc += decimaltobinary(x6 + imm)            #check for rs1 + imm overflow
    pc = pc[:-1] + "0"
    return pc 

def I(i, pc, reg_dict, mem_dic):
    imm = i[:12]
    imm = sext(imm)
    rd = i[-11:-6]
    rs1 = i[-19:-14] 
    func3 = i[-14:-11]
    opcode = i[-6:]
    if (func3 == "010") and (opcode == "0000011"):
        pc = lw(rd, reg_dic[rs1], imm, pc, reg_dic, mem_dic)
    if func3 == "000" and (opcode == "0010011"):
        pc = addi(rd, reg_dic[rs1], imm, pc)
    if func3 == "000" and (opcode == "1100111"):
        pc = jalr(rd, reg_dic[rs1], imm, pc)



reg_dic = {'x0': "0"*16, 'x1': "0"*16, 'x2': "0"*16, 'x3': "0"*16, 'x4': "0"*16, 'x5': "0"*16, 'x6': "0"*16, 'x7': "0"*16,'x8': "0"*16, 
           'x9': "0"*16, 'x10': "0"*16, 'x11': "0"*16, 'x12': "0"*16, 'x13': "0"*16, 'x14': "0"*16, 'x15': "0"*16,'x16': "0"*16, 
           'x17': "0"*16, 'x18': "0"*16, 'x19': "0"*16, 'x20': "0"*16, 'x21': "0"*16, 'x22': "0"*16, 'x23': "0"*16,'x24': "0"*16, 
           'x25': "0"*16, 'x26': "0"*16, 'x27': "0"*16, 'x28': "0"*16, 'x29': "0"*16, 'x30': "0"*16, 'x31': "0"*16}

program_memory = {}
stack_memory = {}
data_memory = {}

# Program Memory
for i in range(256):
    address = f"{i:04X}"  
    program_memory[address] = '0' * 8  

# Stack Memory
for i in range(32):
    #stack_address = 0x100 - (i * 4)     
    address = f'0x{int(256 + i * 4):04X}'  
    stack_memory[address] = '0' * 8  

last_address = '0x017F'
stack_memory[last_address] = '0' * 8

# Data Memory
for i in range(32):
    #data_address = 0x1000 + (i * 4)   
    address = f'0x{int(0x00100000 + i * 4):08X}'  
    data_memory[address] = '0' * 8
    
# Set the last address manually to '0' * 8
last_address = '0x0010007F'
data_memory[last_address] = '0' * 8
    
print(program_memory)
print(stack_memory)
print(data_memory)

mem_dict = {
    **program_memory,
    **stack_memory,
    **data_memory
}

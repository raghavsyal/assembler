
def sext(imm):
    if imm[0] == 0:
        while len(imm)<32 :
            imm = '0' + imm
        return imm
    while len(imm) < 32:
        imm = '1' + imm
    return imm

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

def R(i, pc, reg_dict):
    #try to create this

reg_dic = {}

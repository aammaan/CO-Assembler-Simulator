# ##
# Utsav Garg - 2021108
# Ashutosh Gera - 2021026
# Aman Sharma - 2021010
# Group - A40
# ##

# Clarification 3: In case of overflow, set overflow flag and take the register value as regval= regval mod 2^16.
# In case of underflow, set the overflow flag and regval = 0

# Building a simulator for the given ISA
# Code is executed until hlt instruction is reached

def whole2bin(str_number):
    st = ''
    while int(str_number) > 0:
        remainder = int(str_number) % 2
        st += str(remainder)
        str_number = int(str_number)//2    
    return st[::-1] 

def dec2bin_float(str_number):
    str_number = '0.'+str_number
    str_out = ''
    float_num = float(str_number)
    loop_error_detector = 0
    while(float_num!=0 and loop_error_detector < 8):
        float_num*=2
        str_out += str(int(float_num))
        float_num = float_num - int(float_num)
        loop_error_detector+=1
    if (loop_error_detector == 8):
        print("ERROR")
    return str_out

def ieee_conv(n):
    whole_num, dec_num = n.split(".")
    float_str = (whole2bin(whole_num) + '.' + dec2bin_float(dec_num))
    print(float_str)
    float_num = float(float_str)
    float_len = len(float_str)
    if (float_len>8):
        "ERROR"
    exp_counter = 0
    while(float_num>2):
        float_num/=10
        exp_counter+=1
    final_str = str(float_num)[0:float_len]
    exp_str = n_bits_float(whole2bin(exp_counter),3)
    mantissa_str = n_bits_opp(final_str[2:float_len],5)
    ieee_final = exp_str + mantissa_str
    if len(ieee_final)>8:
        print("ERROR")
    return ieee_final

def n_bits_float(bin,n):
    if len(bin)<n:
        while len(bin) != n:
            bin = '0' + bin    
    return bin 

def n_bits_opp(bin,n):
    if len(bin)<n:
        while len(bin) != n:
            bin = bin + '0' 
    return bin 


op_dict = {
    'add' : '10000',
    'sub' : '10001',
    'mov1' : '10010',
    'mov2' : '10011',
    'ld' : '10100',
    'st' : '10101',
    'mul' : '10110',
    'div' : '10111',
    'rs' : '11000',
    'ls' : '11001',
    'xor' : '11010',
    'or' : '11011',
    'and' : '11100',
    'not' : '11101',
    'cmp' : '11110',
    'jmp' : '11111',
    'jlt' : '01100',
    'jgt' : '01101',
    'je' : '01111',
    'hlt' : '01010'
}

op_float_dict = {
    'addf' : '00000',
    'subf' : '00001',
    'movf' : '00010'
}
                                                                    
typeA_list = ['10000', '10001', '10110', '11010', '11011', '11100']
typeB_list = ['10010','11000','11001']
typeC_list = ['10011','10111','11101','11110']
typeD_list = ['10100','10101']
typeE_list = ['01111','01101','01100','11111']
typeF_list = ['01010']
typeAfloat_list = ['00000', '00001']
typeBfloat_list = ['00010']

reg_rev = {'000' : 'R0', '001' : 'R1', '010' : 'R2', '011': 'R3', '100': 'R4', '101':'R5', '110':'R6', '111':'FLAGS'}

reg_values={
    'R0' : 0,
    'R1' : 0,
    'R2' : 0,
    'R3' : 0,
    'R4' : 0,
    'R5' : 0,
    'R6' : 0,
    'FLAGS' : 0
}
#INITIALIZE ALL REGISTER VALUES TO ZERO

def ieee_to_float(bin):
    exp = bin[0:3]
    mantissa = bin[3:]
    ans = 0
    decimal_digit_shift = bin2dec(exp)
    before_decimal_part = '1' + mantissa[:decimal_digit_shift]
    ans += float(bin2dec(before_decimal_part))
    i = 1
    for j in mantissa[decimal_digit_shift:]:
        ans += float(int(j) * (1/(2**i)))
        i += 1
    return ans       

def dec2bin(str_number):
    st = ''
    while int(str_number) > 0:
        remainder = int(str_number) % 2
        st += str(remainder)
        str_number = int(str_number)//2    
    return st[::-1] 

def n_bits(bin,n):
    if len(bin)<n:
        while len(bin) != n:
            bin = '0' + bin    
    return bin 

def bin2dec(str_bin):
    str_bin = str_bin[::-1]
    dec = 0
    for i in range(len(str_bin)):
        dec += int(str_bin[i]) * (2**i)
    return dec

def typeAfloat(op,r1,r2,r3):
    r1 = reg_rev[r1]
    r2 = reg_rev[r2]
    r3 = reg_rev[r3]
    
    if op == op_float_dict['addf']:
        reg_values[r3] = reg_values[r1] + reg_values[r2]
        if reg_values[r3] > 252:
            reg_values['FLAGS'] = 8
            reg_values[r3] = bin2dec(dec2bin('0000000011111111'))
    
    elif op == op_float_dict['subf']:
        reg_values[r3] = reg_values[r1] - reg_values[r2]
        if reg_values[r3] > 252:
            reg_values['FLAGS'] = 8
            reg_values[r3] = bin2dec(dec2bin('0000000011111111'))
        if reg_values[r3] < 0:
            reg_values['FLAGS'] = 8
            reg_values[r3] = bin2dec(dec2bin('0000000011111111'))
  
def typeBfloat(op,r1,imm_val):
    r1 = reg_rev[r1]
    imm_val = ieee_to_float(imm_val)
    if op == op_float_dict['movf']:
        if imm_val > 252 or imm_val < 0:
            reg_values['FLAGS'] = 8
            reg_values[r1] = bin2dec(dec2bin('0000000011111111'))
        else:                
            reg_values[r1] = imm_val
                       
    

def typeA(op,r1,r2,r3):
    r1 = reg_rev[r1]
    r2 = reg_rev[r2]
    r3 = reg_rev[r3]
    
    if op == op_dict["add"]:
        reg_values[r3] = reg_values[r2] + reg_values[r1]
        if reg_values[r3] > ((2**16) - 1):
            reg_values['FLAGS'] = 2**3
            reg_values[r3] = reg_values[r3] % (2**16)
    
    elif op == op_dict["sub"]:
        reg_values[r3] = reg_values[r1] - reg_values[r2]
        if reg_values[r3] < 0:
            reg_values['FLAGS'] = 2**3
            reg_values[r3] = 0
        elif reg_values[r3] > ((2**16) - 1):
            reg_values['FLAGS'] = 2**3
            reg_values[r3] = reg_values[r3] % (2**16)
    
    elif op == op_dict["mul"]:
        reg_values[r3] = reg_values[r2] * reg_values[r1]
        if reg_values[r3] > ((2**16) - 1):
            reg_values['FLAGS'] = 2**3
            reg_values[r3] = reg_values[r3] % (2**16)
        elif reg_values[r3] < 0:
            reg_values['FLAGS'] = 2**3
            reg_values[r3] = 0
    
    elif op == op_dict['xor']:
        reg_values[r3] = reg_values[r1] ^ reg_values[r2]
    
    elif op == op_dict['or']:
        reg_values[r3] = reg_values[r1] | reg_values[r2]                            
    
    elif op == op_dict['and']:
        reg_values[r3] = reg_values[r1] & reg_values[r2]                            
    
def typeB(op,r1,imm_val):
    r1 = reg_rev[r1]
    imm_val = bin2dec(imm_val)
    if op == op_dict['mov1']:
        reg_values[r1] = imm_val
    
    elif op == op_dict['rs']:
        reg_values[r1] = reg_values[r1] >> imm_val
    
    elif op == op_dict['ls']:
        reg_values[r1] = reg_values[r1] << imm_val                                                     

def typeC(op,r1,r2):
    r1 = reg_rev[r1]
    r2 = reg_rev[r2]
    
    if op == op_dict['mov2']:
        reg_values[r2] = reg_values[r1]
    
    elif op == op_dict['div']:
        reg_values['R0'] = reg_values[r1] // reg_values[r2]
        reg_values['R1'] = reg_values[r1] % reg_values[r2]
        
    elif op == op_dict['not']:
        tmp1 = dec2bin(reg_values[r1])
        tmp1 = n_bits(tmp1, 16)
        tmp2 = ''
        for i in tmp1:
            if i == '0':
                tmp2 += '1'
            elif i == '1':
                tmp2 += '0'
        reg_values[r2] = bin2dec(tmp2)
    
    elif op == op_dict['cmp']:
        if reg_values[r1] > reg_values[r2]:
            reg_values['FLAGS'] = 2**1
        elif reg_values[r1] == reg_values[r2]:
            reg_values['FLAGS'] = 2**0                         
        elif reg_values[r1] < reg_values[r2]:
            reg_values['FLAGS'] = 2**2
    
def typeD(op,r1,mem_add):
    r1 = reg_rev[r1]
    
    if op == op_dict['ld']:
        reg_values[r1] = variables[bin2dec(mem_add)]
        if reg_values[r1] > ((2**16) - 1):
            reg_values[r1] = reg_values[r1] % (2**16)
    
    elif op == op_dict['st']:
        if reg_values[r1] > ((2**16) - 1):
            variables[bin2dec(mem_add)] = reg_values[r1] % (2**16)
        else:
            variables[bin2dec(mem_add)] = reg_values[r1]   

def typeE(op,mem_add):
    global prog_counter, c
    mem_add = bin2dec(mem_add)
    
    if op == op_dict['jmp']:
        reg_values['FLAGS'] = 0       
        printIns()
        c = mem_add
        prog_counter = mem_add
    
    elif op == op_dict['jlt'] and reg_values['FLAGS'] == 4:
        reg_values['FLAGS'] = 0       
        printIns()
        c = mem_add
        prog_counter = mem_add
    
    elif op == op_dict['jgt'] and reg_values['FLAGS'] == 2:
        reg_values['FLAGS'] = 0       
        printIns()
        c = mem_add 
        prog_counter = mem_add
    
    elif op == op_dict['je'] and reg_values['FLAGS'] == 1:
        reg_values['FLAGS'] = 0       
        printIns()
        c = mem_add
        prog_counter = mem_add
    
    else:
        reg_values['FLAGS'] = 0       
        printIns()
        c += 1
        prog_counter += 1

# def typeF(op):
#     pass                               

def printIns():
    a = n_bits(dec2bin(prog_counter),8)
    b = n_bits(dec2bin(reg_values['R0']),16)
    c = n_bits(dec2bin(reg_values['R1']),16)
    d = n_bits(dec2bin(reg_values['R2']),16)
    e = n_bits(dec2bin(reg_values['R3']),16)
    f = n_bits(dec2bin(reg_values['R4']),16)
    g = n_bits(dec2bin(reg_values['R5']),16)
    h = n_bits(dec2bin(reg_values['R6']),16)
    i = n_bits(dec2bin(reg_values['FLAGS']),16)
    
    print (a,b,c,d,e,f,g,h,i,sep = " ",end = "\n")

def dumpMem(instruction):
    print (*instruction.values(), sep = '\n')
    printed = len(instruction)
    
    if len(variables) != 0:
        for i in range(printed, printed + len(variables)):
            tmp = n_bits(dec2bin(variables[i]),16)
            print (tmp, end = '\n')
            printed += 1
    
    for i in range(printed,256):
        print ('0'*16)                
            
def main():
    tmp = 0
    instruction = {} #dict to store input binary file
    global prog_counter
    prog_counter = 0
    
    while True:
        try:
            l = input().strip()
            if l != '':
                instruction[tmp] = l
                tmp += 1
        
        except EOFError:
            break        

    #print (instruction)       
    global variables
    variables = {} #dict to store mem address & values of variables
    i = 0   
    for i in range(len(instruction)):
        if instruction[i][0:5] == op_dict['ld'] or instruction[i][0:5] == op_dict['st']:
            variables[bin2dec(instruction[i][8:])] = 0
    
    # x = '010010'
    # x = n_bits(x,8)
    # print(x)
    halted = False
    global c
    c = 0 #instruction count
    while (not halted):
        op = instruction[c][0:5]
        if op in typeF_list:
            reg_values['FLAGS'] = 0
            printIns()
            halted = True
        
        elif op in typeA_list:
            oldFlag = reg_values['FLAGS']
            typeA(op,instruction[c][7:10],instruction[c][10:13], instruction[c][13:16])
            if oldFlag == reg_values['FLAGS']:
                reg_values['FLAGS'] = 0
            printIns()
            c += 1
            prog_counter += 1
        
        elif op in typeB_list:
            oldFlag = reg_values['FLAGS']
            typeB(op,instruction[c][5:8],instruction[c][8:])
            if oldFlag == reg_values['FLAGS']:
                reg_values['FLAGS'] = 0
            printIns()
            c += 1
            prog_counter += 1
        
        elif op in typeC_list:
            oldFlag = reg_values['FLAGS']
            typeC(op,instruction[c][10:13],instruction[c][13:16])
            if oldFlag == reg_values['FLAGS']:
                reg_values['FLAGS'] = 0
            printIns()
            c += 1
            prog_counter += 1
        
        elif op in typeD_list:
            oldFlag = reg_values['FLAGS']
            typeD(op,instruction[c][5:8],instruction[c][8:])
            if oldFlag == reg_values['FLAGS']:
                reg_values['FLAGS'] = 0
            printIns()
            c += 1
            prog_counter += 1
        
        elif op in typeE_list:
            oldFlag = reg_values['FLAGS']
            typeE(op, instruction[c][8:])
            if oldFlag == reg_values['FLAGS']:
                reg_values['FLAGS'] = 0
            #printIns()
            # i += 1
            # prog_counter += 1  
        elif op in typeAfloat_list:
            oldFlag = reg_values['FLAGS']
            typeAfloat(op,instruction[c][7:10],instruction[c][10:13], instruction[c][13:16])
            if oldFlag == reg_values['FLAGS']:
                reg_values['FLAGS'] = 0
            a = n_bits(dec2bin(prog_counter),8)
            b = n_bits(ieee_conv(str(reg_values['R0'])),16)
            c = n_bits(ieee_conv(str(reg_values['R1'])),16)
            d = n_bits(ieee_conv(str(reg_values['R2'])),16)
            e = n_bits(ieee_conv(str(reg_values['R3'])),16)
            f = n_bits(ieee_conv(str(reg_values['R4'])),16)
            g = n_bits(ieee_conv(str(reg_values['R5'])),16)
            h = n_bits(ieee_conv(str(reg_values['R6'])),16)
            i = n_bits(ieee_conv(str(reg_values['FLAGS'])),16)   
             
            print (a,b,c,d,e,f,g,h,i,sep = " ",end = "\n")
            c += 1
            prog_counter += 1
        
        elif op in typeBfloat_list:
            oldFlag = reg_values['FLAGS']
            typeB(op,instruction[c][5:8],instruction[c][8:])
            if oldFlag == reg_values['FLAGS']:
                reg_values['FLAGS'] = 0
            
            a = n_bits(dec2bin(prog_counter),8)
            b = n_bits(ieee_conv(str(reg_values['R0'])),16)
            c = n_bits(ieee_conv(str(reg_values['R1'])),16)
            d = n_bits(ieee_conv(str(reg_values['R2'])),16)
            e = n_bits(ieee_conv(str(reg_values['R3'])),16)
            f = n_bits(ieee_conv(str(reg_values['R4'])),16)
            g = n_bits(ieee_conv(str(reg_values['R5'])),16)
            h = n_bits(ieee_conv(str(reg_values['R6'])),16)
            i = n_bits(ieee_conv(str(reg_values['FLAGS'])),16)   
             
            print (a,b,c,d,e,f,g,h,i,sep = " ",end = "\n")
            c += 1
            prog_counter += 1     
                
                         
   
    dumpMem(instruction)
               
                
            
if __name__ == '__main__':
    main()   
            

import math


def pincount(space,address,word):
    bit=0
    if(space[-1]=='B' and space[-2]=='M'):
        bit=8388608
    elif(space[-1]=='b') and space[-2]=='M':
        bit=1048576
    elif(space[-1]=='b') and space[-2]=='K':
        bit=1024
    elif(space[-1]=='B') and space[-2]=='K':
        bit=8192
    elif(space[-1]=='b') and space[-2]=='G':
        bit=1073741824
    elif(space[-1]=='B') and space[-2]=='G':
        bit=8589934592
    elif(space[-1]=='b') and space[-2]==' ':
        bit=1
    elif(space[-1]=='B') and space[-2]==' ':
        bit=8

    ar=int(space[0:-3])

    mul=0
    if(address==1):
        mul=1
    elif(address==2):
        mul=4
    elif(address==3):
        mul=8
    elif(address==4):
        mul=word
    
    a=math.ceil(math.log2(ar*bit/mul))

    return a

print('\033[1m'+'\033[4m'+'\033[36m'+'''


-------------------- ''''\033[93m'+'WELCOME'+'\033[36m'+'''----------------------

'''+'\033[0m')

query=int(input('''Choose the type of query(1-2): 
1. Question First
2. Question Second  \n'''))

if(query==1):

    space=input("Enter the instruction (eg-16 MB) \n")

    address=int(input('''Choose the type of address(1-4):
    1. Bit Address Memory
    2. Nibble Addressable Memory
    3. Byte Addressable Memory
    4. Word Addressable Memory \n'''))

    word=1
    if(address==4):
        word=int(input("Enter the memory size of CPU in bits (eg-32) :  \n"))
    

    p=pincount(space,address,word)

    inst=int(input("Enter the length of Instruction in bits (eg-32) : \n"))

    reg=int(input("Enter the length of Register in bits (eg-7) : \n"))
    
    opcode=inst-reg-p
    opcode=math.ceil(opcode)
    filler=inst-opcode-2*reg


    if(opcode<0):
        print('\033[91m' + "NEGATIVE VALUE OF OPCODE (",str(opcode)  ,") " + '\033[0m')
    else:
        print("Number of bits needed by opcode is ",'\033[95m'+ str(opcode) +'\033[0m')

    if(filler<0):
        print('\033[91m' + "NEGATIVE VALUE OF FILLER BIT (",str(math.ceil(filler)) ,") " + '\033[0m')
    else:
        print("Number of filler bits in Instruction type 2 is ",'\033[95m'+ str(math.ceil(filler)) +'\033[0m')

    if(p<0):
        print('\033[91m' + "NEGATIVE VALUE OF BITS NEEDED TO REPRESENT AN ADDRESS (", str(math.ceil(p)),") " + '\033[0m')
    else:
        print("Number of Bits needed to represent an address",'\033[95m'+ str(math.ceil(p)) +'\033[0m')

    print("Number Maximum number of Instruction ",'\033[95m'+ str(math.ceil(2**opcode)) +'\033[0m')
    print("Number Maximum number of Register ",'\033[95m'+ str(math.ceil(2**reg)) +'\033[0m ',"\n \n")



elif(query==2):
    type=int(input('''Choose the type(1-2): 
    1. Type A
    2. Type B \n'''))
    if(type==1):
        cpu=input("Enter the memory space (eg-16 MB) : \n")
        memo=int(input('''Choose the type of address(1-4):
        1. Bit Address Memory
        2. Nibble Addressable Memory
        3. Byte Addressable Memory
        4. Word Addressable Memory \n'''))
        ss=int(input('''Enter the bit of Computer (eg-32) : \n'''))
        
        enhance=int(input('''Choose the type of address you want to enhance with (1-4):
        1. Bit Address Memory
        2. Nibble Addressable Memory
        3. Byte Addressable Memory
        4. Word Addressable Memory \n'''))
        print('\033[95m'+str(pincount(cpu,enhance,ss)-pincount(cpu,memo,ss))+'\033[0m')
    
    elif(type==2):
        ss=int(input('''Enter the bit of Computer (eg-32) \n'''))
        pin=int(input("Enter the number of address pins (eg-34): \n"))
        mem=int(input('''Choose the type of address(1-4):
        1. Bit Address Memory
        2. Nibble Addressable Memory
        3. Byte Addressable Memory
        4. Word Addressable Memory \n'''))

        mul=0
        if(mem==1):
            mul=1
        elif(mem==2):
            mul=4
        elif(mem==3):
            mul=8
        elif(mem==4):
            mul=ss

        ans=(2**(pin))*mul
        print('\033[95m' + str(ans/(2**33)),"GB or",str(ans),"bits" + '\033[0m')
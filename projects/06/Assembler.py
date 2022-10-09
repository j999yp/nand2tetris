import pathlib as p
import re

src_path=p.Path(input("Input .asm file path:\n"))
with open(p.Path.cwd().joinpath(src_path),"r") as src:
    src=src.readlines()

class env:
    comp={
        "0"  : "101010",
        "1"  : "111111",
        "-1" : "111010",
        "D"  : "001100",
        "A"  : "110000",
        "!D" : "001101",
        "!A" : "110001",
        "-D" : "001111",
        "-A" : "110011",
        "D+1": "011111",
        "A+1": "110111",
        "D-1": "001110",
        "A-1": "110010",
        "D+A": "000010",
        "D-A": "010011",
        "A-D": "000111",
        "D&A": "000000",
        "D|A": "010101"
    }
    dest={
        "null": "000",
        "M"   : "001",
        "D"   : "010",
        "MD"  : "011",
        "A"   : "100",
        "AM"  : "101",
        "AD"  : "110",
        "AMD" : "111"
    }
    jump={
        "null": "000",
        "JGT" : "001",
        "JEQ" : "010",
        "JGE" : "011",
        "JLT" : "100",
        "JNE" : "101",
        "JLE" : "110",
        "JMP" : "111"
    }
    symbol={
        "SP":0,
        "LCL":1,
        "ARG":2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN":16384,
        "KBD":24576
    }
    def __init__(self):
        for i in range(16):
            self.symbol["R"+str(i)]=i
        self.variable_pointer=16
        self.instruction_pointer=0

envs=env()

def if_A_instruction(row):
    return True if '@' in row else False
def if_label(row):
    return True if '(' in row else False






# remove comments and spaces
for i in range(len(src)):
    src[i]=re.sub(r'(//.*)|(\s*)','',src[i])
# remove blank lines
src=[i for i in src if i]
# find all labels
for i in range(len(src)):
    if(if_label(src[i])):
        label=src[i].replace('(','').replace(')','')
        src[i]=''
        if(label not in envs.symbol):
            envs.symbol[label]=envs.instruction_pointer
    else:
        envs.instruction_pointer+=1
src=[i for i in src if i]
# main work
res=[]
for row in src:
    if(if_A_instruction(row)):
        val=row[1:]
        try:
            res.append(bin(int(val)).replace('0b','').rjust(16,'0'))
        except:
            if(val in envs.symbol):
                res.append(bin(envs.symbol[val]).replace('0b','').rjust(16,'0'))
            else:
                envs.symbol[val]=envs.variable_pointer
                envs.variable_pointer+=1
                res.append(bin(envs.symbol[val]).replace('0b','').rjust(16,'0'))
    else:
        if('=' in row):
            row=row.replace('=',' ')
        else:
            row='null '+row
        if(';' in row):
            row=row.replace(';',' ')
        else:
            row=row+' null'
        dest=row.split(' ')[0]
        comp=row.split(' ')[1]
        jump=row.split(' ')[2]
        if('M' in comp):
            M_flag='1'
            comp=comp.replace('M','A')
        else:
            M_flag='0'
        res.append('111'+M_flag+envs.comp[comp]+envs.dest[dest]+envs.jump[jump])

with open(p.Path.cwd().joinpath(src_path.with_suffix('.hack')),'w') as f:
    for row in res:
        f.write(row+'\n')
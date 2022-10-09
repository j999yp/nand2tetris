from ensurepip import bootstrap
from pathlib import Path as p
import re

#0-15 regs SP LCL ARG THIS THAT
#16-255 static
#256-2047 stack
#2048-16383 heap
#16384-24575 I/O

src=p.cwd().joinpath(p(input("input file or directory:\n")))
if(src.is_file()):
    out=src.with_suffix('.asm')
    src=[src]
else:
    out=src.joinpath(src.stem+".asm")
    src=list(src.glob("*.vm"))

class segments:
    regs={
        "local":"LCL",
        "argument":"ARG",
        "this":"THIS",
        "that":"THAT",
        "temp":5,
        "pointer":3
    }

    def translate(self,base,offset,type):
        res=[]
        if(type=="push"):
            res+=["A=D","D=M","@SP","A=M","M=D","@SP","M=M+1"]
        elif(type=="pop"):
            res+=["@TMP","M=D","@SP","AM=M-1","D=M","@TMP","A=M","M=D"]

        if(base=="static"):
            res=["@"+filename+"."+offset,"D=A"]+res
        elif(base in ["pointer","temp"]):
            addr=self.regs[base]+int(offset)
            res=["@"+str(addr),"D=A"]+res
        elif(base not in self.regs): # push an addr onto stack
            res=["@"+base+offset,"D=A"]+res[2:]
        else:
            res=["@"+offset,"D=A","@"+self.regs[base],"D=D+M"]+res
        return res
segment=segments()

class arithmetic:
    cnt=0
    def __init__(self):
        self.arithmetic={
        "add": ["@SP","AM=M-1","D=M","A=A-1","M=D+M"],
        "sub": ["@SP","AM=M-1","D=M","A=A-1","M=M-D"],
        "neg": ["@SP","A=M-1","M=-M"],
        "eq" : ["@SP","AM=M-1","D=M","A=A-1","D=M-D","M=0","@jmp"+str(self.cnt),"D;JNE","@SP","A=M-1","M=-1","(jmp"+str(self.cnt)+")"],
        "gt" : ["@SP","AM=M-1","D=M","A=A-1","D=M-D","M=0","@jmp"+str(self.cnt),"D;JLE","@SP","A=M-1","M=-1","(jmp"+str(self.cnt)+")"],
        "lt" : ["@SP","AM=M-1","D=M","A=A-1","D=M-D","M=0","@jmp"+str(self.cnt),"D;JGE","@SP","A=M-1","M=-1","(jmp"+str(self.cnt)+")"],
        "and": ["@SP","AM=M-1","D=M","A=A-1","M=D&M"],
        "or" : ["@SP","AM=M-1","D=M","A=A-1","M=D|M"],
        "not": ["@SP","A=M-1","M=!M"]
        }
    def translate(self,func):
        res=self.arithmetic[func]
        if(func in ["eq","gt","lt"]):
            self.cnt+=1
            self.__init__()
        return res
arithmetics=arithmetic()

def translate(row) -> str:
    if(type(row)==str):
        row=row.split()
    if(row[0]=="push"):
        seg=row[1]
        if(seg=='constant'):
            res=['@'+row[2],"D=A","@SP","A=M","M=D","@SP","M=M+1"]
        else:
            offset=row[2]
            res=segment.translate(seg,offset,"push")
    elif(row[0]=="pop"):
        seg=row[1]
        offset=row[2]
        res=segment.translate(seg,offset,"pop")
    elif(row[0]=="label"):
        return ["("+row[1]+")"]
    elif(row[0]=="goto"):
        return ["@"+row[1],"0;JMP"]
    elif(row[0]=="if-goto"):
        res=["@SP","AM=M-1","D=M","M=0","@"+row[1],"D;JNE"]
    elif(row[0]=="function"):
        res=["("+row[1]+")"]
        for _ in range(int(row[2])):
            res+=["@SP","A=M","M=0","@SP","M=M+1"]
    elif(row[0]=="call"):
        global ret_cnt
        res=translate("push "+"ret-addr "+str(ret_cnt))
        res+=["@LCL","D=M","@SP","A=M","M=D","@SP","M=M+1"]
        res+=["@ARG","D=M","@SP","A=M","M=D","@SP","M=M+1"]
        res+=["@THIS","D=M","@SP","A=M","M=D","@SP","M=M+1"]
        res+=["@THAT","D=M","@SP","A=M","M=D","@SP","M=M+1"]
        res+=["@SP","D=M","@LCL","M=D","@"+row[2],"D=D-A","@5","D=D-A","@ARG","M=D"]
        res+=translate("goto "+row[1])
        res+=["(ret-addr"+str(ret_cnt)+")"]
        ret_cnt+=1
    elif(row[0]=="return"):
        res=["@LCL","D=M","@FRAME","M=D"]
        res+=["@5","A=D-A","D=M","@TMP","M=D"] # RET
        res+=["@SP","AM=M-1","D=M","@ARG","A=M","M=D"]
        res+=["@ARG","D=M+1","@SP","M=D"] #? test
        res+=["@FRAME","D=M","@1","A=D-A","D=M","@THAT","M=D"]
        res+=["@FRAME","D=M","@2","A=D-A","D=M","@THIS","M=D"]
        res+=["@FRAME","D=M","@3","A=D-A","D=M","@ARG","M=D"]
        res+=["@FRAME","D=M","@4","A=D-A","D=M","@LCL","M=D"]
        res+=["@TMP","A=M","0;JMP"]

    else: # arithmetics
        res=arithmetics.translate(row[0])
    return res

def main(src,filepath):
    # remove comments and spaces
    for i in range(len(src)):
        src[i]=re.sub(r'(//.*)|(\n*)','',src[i])
    # remove blank lines
    src=[i for i in src if i]
    # instruction type
    res=[]
    for row in src:
        res+=translate(row)
    return res

ret_cnt=0
res=[]
bootstrap=["@256","D=A","@SP","M=D"]+\
    ["@1","D=A","@LCL","M=D"]+\
	["@2","D=A","@ARG","M=D"]+\
	["@3","D=A","@THIS","M=D"]+\
	["@4","D=A","@THAT","M=D"]+\
    translate("call Sys.init 0")
res+=bootstrap
for file in src:
    with open(file,'r') as f:
        src=f.readlines()
        filename=file.stem
        res+=main(src,file)
res+=["(exit)","@exit","0;JMP"]

with open(out,'w') as f:
        for row in res:
            f.write(row+'\n')
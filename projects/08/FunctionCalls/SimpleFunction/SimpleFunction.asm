(SimpleFunction.test)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@0
D=A
@LCL
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@LCL
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
M=0
A=A-1
M=D+M
@SP
A=M-1
M=!M
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
M=0
A=A-1
M=D+M
@1
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
M=0
A=A-1
M=M-D
@LCL
D=M
@FRAME
M=D
@FRAME
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
@0
D=A
@ARG
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
M=0
@R13
A=M
M=D
@ARG
D=M+1
@SP
M=D
@FRAME
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@FRAME
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@FRAME
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@FRAME
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP
(exit)
@exit
0;JMP

@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
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
D=D-M
M=0
@jmp0
D;JNE
@SP
A=M-1
M=-1
(jmp0)
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@16
D=A
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
D=D-M
M=0
@jmp1
D;JNE
@SP
A=M-1
M=-1
(jmp1)
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
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
D=D-M
M=0
@jmp2
D;JNE
@SP
A=M-1
M=-1
(jmp2)
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
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
D=D-M
M=0
@jmp3
D;JLE
@SP
A=M-1
M=-1
(jmp3)
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@892
D=A
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
D=D-M
M=0
@jmp4
D;JLE
@SP
A=M-1
M=-1
(jmp4)
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
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
D=D-M
M=0
@jmp5
D;JLE
@SP
A=M-1
M=-1
(jmp5)
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
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
D=D-M
M=0
@jmp6
D;JGE
@SP
A=M-1
M=-1
(jmp6)
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
D=A
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
D=D-M
M=0
@jmp7
D;JGE
@SP
A=M-1
M=-1
(jmp7)
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
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
D=D-M
M=0
@jmp8
D;JGE
@SP
A=M-1
M=-1
(jmp8)
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
@53
D=A
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
@112
D=A
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
@SP
A=M-1
M=-M
@SP
AM=M-1
D=M
M=0
A=A-1
M=D&M
@82
D=A
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
M=D|M
@SP
A=M-1
M=!M
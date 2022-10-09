// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(READ_KEYBOARD)
@24576
D=M
@R2
M=D
@FILL
D;JEQ
@R2
M=-1


(FILL)
@16384
D=A
@R1
M=D //base addr
(FILL_LOOP)
@R2
D=M //color
@R1
A=M
M=D //write color
@R1
MD=M+1 //next word

@24576
D=D-A
@READ_KEYBOARD
D;JEQ
@FILL_LOOP
0;JMP
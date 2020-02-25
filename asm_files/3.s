.data
str: .asciiz "Hello World!"

.text
.globl main
main:
addi 2, 0, 4
ld 3, 0(str)
addi 0, 4, 0
sc LEV
addi 0, 0, 31      #reset

addi 0, 10, 0     #syscall to exit
sc LEV

.end


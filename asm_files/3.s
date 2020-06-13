.data
str: .asciiz "Hello World!"

.text
.globl main
main:
addi 2, 4, 0
la 3, 0(str)
addi 0, 0, 4
sc LEV
addi 0, 31, 0      #reset

addi 0, 0, 10    #syscall to exit
sc LEV

.end


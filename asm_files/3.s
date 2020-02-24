.data
str: .asciiz "Hello World!"

.text
.globl main
main:
addi 2, 0, 4
lwz 4, 0(str)
sc LEV

lwz 2, 0(10)
sc LEV

.end


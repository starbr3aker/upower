.data
str: .asciiz "Hello World!"

.text
.globl main
main:
addi $v0, $zero,4
la $a0,str
syscall

li $v0,10
syscall

.end


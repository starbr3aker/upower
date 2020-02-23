.data
x: .word 5
y: .word 10
sum: .word 0
label: .asciiz "Hllo"

.text
.globl main

main:
la $t0,x
la $t1,y
lw $s0,0($t0)
lw $s1,0($t1)
add $s2,$s1,$s0
la $t2,sum
sw $s2,0($t2)
li $v0,10
syscall
.end

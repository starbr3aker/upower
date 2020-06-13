.data
x: .word 5
y: .word 10
sum: .word 0

.text
.globl main

main:
la 8, 0(x)    #$t0
la 9, 0(y)    #$t1 
ld 16, 0(8)   #$s0
ld 17, 0(9)   #$s1
add 18, 17, 16  #$s2, $s1, $s0
la 19, 0(sum)
addi 10, 19, 0  #$t2
std 18, 0(10)  #$s2, $t2
addi 0, 0, 10     #syscall to exit
sc LEV
.end

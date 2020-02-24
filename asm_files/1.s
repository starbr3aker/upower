.data
x: .word 5
y: .word 10
sum: .word 0

.text
.globl main

main:
lwz 8,0(x)    #$t0
lwz 9,0(y)    #$t1 
lwz 16,0(8) #$s0
lwz 17,0(9) #$s1
add 18,17,16  #$s2, $s1, $s0
addi 10,sum   #$t2
stw 18,0(10)  #$s2, $t2
addi 2,10   #$v0
sc LEV
.end

.data
	A: .word 10
	B: .word 20

.text
.globl main

main:
    lui $t0, 4096   # to reserve space for later 
    lw $t1, A	# t1=A
    lw $t2, B	# t2=B
    sw $t1, 0($t0)	
    sw $t2, 0($gp)
    add $t3, $t1 $t2	# t3 = t1 + t2
    sw $t3, 396($t0) 	# 396 as each word stores 4 bytes

# To display the result
	li $v0, 1
	add $a0, $zero, $t3
	syscall

    li $v0,10
    syscall


.end

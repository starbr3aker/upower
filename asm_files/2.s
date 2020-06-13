.data
	A: .word 10
	B: .word 20

.text
.globl main

main:
    
    la 9, 0(A)  # t1=address of A
    la 10, 0(B)	# t2=address of B
    ld 9, 0(9)
    ld 10, 0(10)
    add 11, 9, 10	# t3 = t1 + t2
    std 11, 396(8) 	# 396 as each word stores 4 bytes

# To display the result
	addi 3, 11, 0
	addi 0, 0, 1    #syscall to print int
	sc LEV

    addi 0, 31, 0     #syscall instruction reset
    addi 0, 0, 10     #syscall to exit
    sc LEV


.end

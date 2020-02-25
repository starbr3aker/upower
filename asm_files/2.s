.data
	A: .word 10
	B: .word 20

.text
.globl main

main:
    addi 8, 4096, 0   # to reserve space for later 
    ld 9, 0(A)  # t1=address of A
    ld 10, 0(B)	# t2=address of B
    ld 9, 0(9)
    ld 10, 0(10)
    add 11, 9, 10	# t3 = t1 + t2
    std 11, 396(8) 	# 396 as each word stores 4 bytes

# To display the result
	ld 2, 1
	add 4, 0, 11
	sc LEV

    ld 2,10
    sc LEV


.end

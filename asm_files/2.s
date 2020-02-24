.data
	A: .word 10
	B: .word 20

.text
.globl main

main:
    lwz 8, 0(4096)   # to reserve space for later 
    lwz 9, 0(9)	# t1=A
    lwz 10, 0(10)	# t2=B
    stw 9, 0(8)	
    stw 10, 0(28)
    add 11, 9, 10	# t3 = t1 + t2
    stw 11, 396(8) 	# 396 as each word stores 4 bytes

# To display the result
	lwz 2, 1
	add 4, 0, 11
	sc LEV

    lwz 2,10
    sc LEV


.end

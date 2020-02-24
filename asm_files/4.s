.data
array: .word 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
#array = [1,2,3,4,5,6,7,8,9,10]

.text

main:
    
    addi 16, 0, 0           #i=0
    addi 17, 0, 0           #sum=0
    addi 10, 0, 10          #number of elements
    la 11, array             #loading the address of the array into the register

loop:

    cmp 7, 1, 16, 10
    bca 30, end
    ld 12, 0(11)             #$t4 countains the value to be added
    add 17, 17, 12           #$s1 contains the sum of the integers
    add 16, 16, 1            #$s0 contains the counter
    add 11, 11, 4            #$t3 is the address of the array
    ba loop

end:
    addi 2, 0, 1    
	add 4, 17, 0
	sc LEV



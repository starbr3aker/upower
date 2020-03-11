.data
array: .word 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

.text

main:
    
    addi 17, 0, 0           #sum=0
    addi 10, 31, 10          #number of elements
    la 11, 0(array)             #loading the address of the array into the register

loop:

    cmp 7, 1, 16, 10
    bca 30, comp
    ld 12, 0(11)             #$t4 countains the value to be added
    add 17, 17, 12           #$s1 contains the sum of the integers
    addi 16, 16, 1           #$s0 contains the counter
    addi 11,11, 1        #$t3 is the address of the array
    b loop

comp:
    addi 0, 0, 1           #0 is the instruction register, and now has value 1       
    addi 3, 17, 0          #register 3 is the value that syscall operates on. It is now the value in r17
    sc LEV                   #Calling syscall

    addi 0, 31, 0           #Putting r0 = 0

    addi 0, 0, 10           #taking r0 = 10
    sc LEV					#Exit syscall
	.end



.data
	A: .word 10

.text
.globl main
main:
add r1, r2, r3
ld r2, 0(A)
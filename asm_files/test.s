.data
	A: .word 10
	B: .word 20

.text
.globl main
main:
add r1, r2, r3
ld r2, 0(lab)
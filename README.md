# Micropower ISA implementation

Videos are uploaded on:

https://drive.google.com/drive/folders/1x6ZXkRyPD3YazumilLAJqLHjfP6HGpEI

## WORKING:

Read a line from the asm file.

Process the section of the asm file. 

For the .data section, do:

1. Generate a map/dictionary of each label and a corresponding variable.
	
2. Allocate memory for the variable according to memory layout.
	
		
For the .text section, do:

1. Interpret each command, find its format and encode it. Store the encoding as binary 64 bit number. 
	
2. Append number to list of instructions.
	
3. For everytime the address of a label is called, fetch and store from map.
	

STYLE GUIDE: https://www.python.org/dev/peps/pep-0008/

## Syscall:

https://www.kernel.org/doc/html/latest/powerpc/syscall64-abi.html

http://students.cs.tamu.edu/tanzir/csce350/reference/syscalls.html

register 3 is parameter/address

register 0 is the input/type of syscall

register 31 is treated as zero register.

## Submitted by:

1. Feyaz Baker - 181co119

2. Shrvan Warke - 181co151

3. Nihar KG Rai - 181co235

4. Vignesh Srinivasan - 181co258


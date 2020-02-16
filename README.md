# Micropower ISA implementation

WORKING:

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



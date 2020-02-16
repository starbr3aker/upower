# Micropower ISA implementation

WORKING:
Read a line from the asm file.
Process the section of the asm file. 
For the .data section, do:
	Generate a map/dictionary of each label and a corresponding variable.
	Allocate memory for the variable according to memory layout.
	
		
For the .text section, do:
	Interpret each command, find its format and encode it. Store the encoding as binary 64 bit number. 
	Append number to list of instructions.
	For everytime the address of a label is called, fetch and store from map.
	

STYLE GUIDE: https://www.python.org/dev/peps/pep-0008/



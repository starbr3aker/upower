# Micropower ISA implementation

### Instruction to make packages

1. Make a folder with the same name as package.

2. Inside the folder, create a .py file with same name, along with a `__init__.py` file and a `desc.txt` for the description.

3. Write the function inside the .py file, and import it into the `__init__.py` file. 

4. Do `git add .` and then `pre-commit run` to check formatting by PEP8 standards.

5. Correct the errors, if any, and repeat step 4 till no errors are found.

6. Generate commit.

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



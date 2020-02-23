from readasm import readasm  # noqa: F401
import checkInstructionType  # noqa: F401

pc = 0
textend = 0
staticend = 0
sp = 0
reserved = {}
text = {}
static = {}
dynamic = {}
reg = {}


def initialise():
    """Main memory implementation with dictionary. Isn't faithful recreation of memory because of RAM constraints."""
    A = 0x0000_0000_0000_0000
    B = 0x0000_0000_0040_0000

    global pc
    pc = B
    global textend
    textend = 2 * B
    global staticend
    staticend = 3 * B
    global sp
    sp = 4 * B

    global reserved
    reserved = {i: 0 for i in range(A, B)}
    print("reserved memory initialised")
    global text
    text = {i: 0 for i in range(B, 2 * B)}
    print("text memory initialised")
    global static
    static = {i: 0 for i in range(2 * B, 3 * B)}
    print("static memory initialised")
    global dynamic
    dynamic = {i: 0 for i in range(3 * B, 4 * B)}
    print("dynamic memory initialised")

    global reg
    reg = {i: 0 for i in range(32)}
    print("32 registers ready")


initialise()

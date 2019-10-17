"""CPU functionality."""
import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001 
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.branch_table = {
            LDI: self.LDI,
            PRN: self.PRN,
            HLT: self.HLT,
            MUL: self.alu, 
            PUSH: self.PUSH,
            POP: self.POP,
        }

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        # Implement function to load an .ls8 file 
        # Pass in filename as argument

        try:
            with open(filename) as f:
                for line in f:
                    # ignore anything after a #
                    comment_split = line.split("#")
                    # Convert any numbers from binary strings to integers
                    # strip removes whitespaces
                    num = comment_split[0].strip()
                    if num != '':
                        val = int(num, 2)
             
                        self.ram[address] = val
                        address += 1

        except FileNotFoundError:
            # print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            print(f"{filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def HLT(self):
        sys.exit(1)

    def PRN(self, operand_a):
        val = self.reg[operand_a]
        print(val)

    def LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def PUSH(self, operand_a):
        reg = self.ram[operand_a]
        val = self.reg[reg]
        # Decrement the SP
        self.reg[self.sp] -= 1
        # Copy the value in the given register to the address pointed to by SP
        self.ram[self.reg[self.sp]] = val
        

    def POP(self, operand_a):
        reg = self.ram[operand_a]
        val = self.ram[self.reg[self.sp]]
        # Copy the value in the given register to the address pointed to by SP
        self.reg[reg] = val
        # Increment SP 
        self.reg[self.sp] += 1
        

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            IR = self.ram[self.pc]
            
            operand_a = self.ram_read(self.pc + 1)

            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                self.branch_table[HLT]()

            elif IR == LDI:
                self.branch_table[LDI](operand_a, operand_b)
                self.pc += 3
            
            elif IR == PRN:
                self.branch_table[PRN](operand_a)
                self.pc += 2

            elif IR == MUL:
                # self.alu("MUL", operand_a, operand_b)
                self.branch_table[MUL]("MUL", operand_a, operand_b)
                self.pc += 3

            elif IR == PUSH:
                self.branch_table[PUSH](operand_a)
                self.pc += 2

            elif IR == POP:
                self.branch_table[POP](operand_a)
                self.pc += 2

            else:
                print('Error: cannot recognize instruction provided')

        self.trace()

    # MAR == address to write to
    def ram_read(self, MAR):
        return self.ram[MAR]
    # MDR == data to write 
    def raw_write(self, MAR, MDR):
        self.ram[MAR] = MDR



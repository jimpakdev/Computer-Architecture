"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        # Implement function to load an .ls8 file 
        # Pass in filename as argument
        if len(sys.argv) != 2:
            print("usage: file.py <filename>", file=sys.stderr)
            sys.exit(1)

        try:
            with open(filename) as f:
                for line in f:
                    # ignore anything after a #
                    comment_split = line.split("#")
                    # Convert any numbers from binary strings to integers
                    num = comment_split[0].strip()

                    val = int(num, 2)
             
                    self.ram[address] = val
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001 
        MUL = 0b10100010

        running = True

        while running:
            IR = self.ram[self.pc]
            
            operand_a = self.ram_read(self.pc + 1)

            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                running = False

            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif IR == MUL:
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3

            else:
                print('Error: cannot recognize instruction provided')

        self.trace()

    # MAR == address to write to
    def ram_read(self, MAR):
        return self.ram[MAR]
    # MDR == data to write 
    def raw_write(self, MAR, MDR):
        self.ram[MAR] = MDR


"""CPU functionality."""
import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001 
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.flag = 0b00000000
        self.branch_table = {
            LDI: self.LDI,
            PRN: self.PRN,
            HLT: self.HLT,
            ADD: self.alu,
            MUL: self.alu, 
            PUSH: self.PUSH,
            POP: self.POP,
            CALL: self.CALL,
            RET: self.RET,
            CMP: self.alu,
            JMP: self.JMP,
            JEQ: self.JEQ,
            JNE: self.JNE,
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

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        #  `FL` bits: `00000LGE`
        # * `L` Less-than: during a `CMP`, set to 1 if registerA is less than registerB,
        #   zero otherwise.
        # * `G` Greater-than: during a `CMP`, set to 1 if registerA is greater than
        #   registerB, zero otherwise.
        # * `E` Equal: during a `CMP`, set to 1 if registerA is equal to registerB, zero
        #   otherwise.
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001

            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100

            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010

            # print("CMP / FLAG STATUS:", self.flag)

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
        # print('LDI')

    def PUSH(self, operand_a):
        reg = operand_a
        val = self.reg[reg]
        # Decrement the SP
        self.reg[self.sp] -= 1
        # Copy the value in the given register to the address pointed to by SP
        self.ram[self.reg[self.sp]] = val
        
    def POP(self, operand_a):
        reg = operand_a
        val = self.ram[self.reg[self.sp]]
        # Copy the value in the given register to the address pointed to by SP
        self.reg[reg] = val
        # Increment SP 
        self.reg[self.sp] += 1

    def CALL(self):
        # Push the return address on the stack 
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        # The PC is set to the address stored in the given register
        reg = self.ram[self.pc + 1]
        # Jump to that location in RAM and execute first instruction
        self.pc = self.reg[reg]

    def RET(self):
        # Return from subroutine 
        # Pop the value from the top of the stack and store it in the PC
        self.pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def JMP(self, operand_a): 
        # Set the `PC` to the address stored in the given register.
        self.pc = self.reg[operand_a]

    def JEQ(self, operand_a):
        # If `E` flag is clear (false, 0), jump to the address stored in the given
        # register.
        if self.flag == 0b00000001:
            self.JMP(operand_a)
        else: 
            self.pc += 2
        # print('JEQ')

    def JNE(self, operand_a):
        # If `E` flag is clear (false, 0), jump to the address stored in the given
        # register.
        if self.flag != 0b00000001:
            self.JMP(operand_a)
        else:
            self.pc += 2
        # print('JNE')

    # MAR == address to write to
    def ram_read(self, MAR):
        return self.ram[MAR]
    # MDR == data to write 
    def raw_write(self, MAR, MDR):
        self.ram[MAR] = MDR

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

            elif IR == ADD: 
                self.branch_table[ADD]("ADD", operand_a, operand_b)
                self.pc += 3

            elif IR == MUL:
                self.branch_table[MUL]("MUL", operand_a, operand_b)
                self.pc += 3

            elif IR == PUSH:
                self.branch_table[PUSH](operand_a)
                self.pc += 2

            elif IR == POP:
                self.branch_table[POP](operand_a)
                self.pc += 2

            elif IR == CALL:
                self.branch_table[CALL]()

            elif IR == RET:
                self.branch_table[RET]()

            elif IR == CMP:
                self.branch_table[CMP]("CMP", operand_a, operand_b)
                self.pc += 3

            elif IR == JMP:
                self.branch_table[JMP](operand_a)
                
            elif IR == JEQ:
                self.branch_table[JEQ](operand_a)
                
            elif IR == JNE:
                self.branch_table[JNE](operand_a)
                
            else:
                print('Error: cannot recognize instruction provided')

        self.trace()





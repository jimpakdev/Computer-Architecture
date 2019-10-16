import sys

PRINT_BEEJ     = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4  # SAVE VALUE INTO REGISTER
PRINT_REGISTER = 5
ADD            = 6


memory = [
    PRINT_BEEJ,
    SAVE,  # SAVE 65 into R2
    65,
    2,
    SAVE,  # Save 20 into R3
    20,
    3,
    ADD,   # Add R2 + R3 = 65 + 20, store in R2
    2,
    3,
    PRINT_REGISTER,
    2,
    HALT,
  ]


pc = 0
running = True

# Create 8 registers
register = [0] * 8

def load_memory(filename):
    try:
        address = 0

    with open(sys.argv[1]) as f:
        for line in f:
            # Prcoess comments:
            # Ignore anything after a # symbol
            comment_split = line.split("#")
            # Convert any numbers from binary strings to integers
            num = comment_split[0]
            try: 
                x = int(num, 2)
            except ValueError:
                continue
            # Print in binary and decimal
            print(f"{x:08b}: {x:d}")

while running:
    # Do stuff
    command = memory[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1

    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2

    elif command == HALT:
        running = False
        pc += 1

    elif command == SAVE:
        num = memory[pc+1]  # Get the num from 1st arg
        reg = memory[pc+2]  # Get the register index from 2nd arg
        register[reg] = num # Store the num in the right register
        pc += 3

    elif command == PRINT_REGISTER:
        reg = memory[pc+1]   # Get the register index from 1st arg
        print(register[reg]) # Print contents of that register
        pc += 2

    elif command == ADD:
        reg_a = memory[pc+1]   # Get the 1st register index from 1st arg
        reg_b = memory[pc+2]   # Get the 2nd register index from 2nd arg
        register[reg_a] += register[reg_b] # Add registers, store in reg_a
        pc += 3

    elif command == PUSH:
        reg = memory[pc + 1]
        val = memory[register[SP]]

    else:
        print(f"Unknown instruction: {command}")
        sys.exit(1)
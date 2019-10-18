#!/usr/bin/env python3

# Day 1: Get print8.ls8 running
#  Inventory what is here
#  Implement the CPU constructor
#  Add RAM functions ram_read() and ram_write()
#  Implement the core of run()
#  Implement the HLT instruction handler
#  Add the LDI instruction
#  Add the PRN instruction

# Day 2: Add the ability to load files dynamically, get mult.ls8 running
#  Un-hardcode the machine code
#  Implement the load() function to load an .ls8 file given the filename passed in as an argument
#  Implement a Multiply instruction (run mult8.ls8)

# Day 3: Stack
#  Implement the System Stack and be able to run the stack.ls8 program

# Day 4: Get call.ls8 running
#  Implement the CALL and RET instructions
#  Implement Subroutine Calls and be able to run the call.ls8 program

"""Main."""

import sys
from cpu import *

# other way
# import os

cpu = CPU()

# we need to make sure it exists
if len(sys.argv) != 2:
    print("usage: file.py <filename>", file=sys.stderr)
    sys.exit(1)

# path = os.path.dirname(os.path.abspath(__file__))

# cpu.load(f'{path}/examples/print8.ls8')   
cpu.load(sys.argv[1])   
cpu.run()
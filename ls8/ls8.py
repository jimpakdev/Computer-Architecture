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

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()
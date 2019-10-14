#!/usr/bin/env python3

# Day 1: Get print8.ls8 running
#  Inventory what is here
#  Implement the CPU constructor
#  Add RAM functions ram_read() and ram_write()
#  Implement the core of run()
#  Implement the HLT instruction handler
#  Add the LDI instruction
#  Add the PRN instruction

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()
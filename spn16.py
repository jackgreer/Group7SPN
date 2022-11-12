# Filename: spn.py
# Author: MATH 4175 Group 7 (Andrew Tran, Anthony Tran, Jack Greer, Jason Pak, Michael Peters)
# Date: 6 Nov 2022 (Date Last Modified: 6 Nov 2022, Jack Greer)
# Description: This file contains a Python algorithm that performs a linear attack
# on the "Baby SPN" and partially finds the key.
from tabulate import tabulate

# This dict contains the corresponding XOR values for the numbers 0b000 through 0b111
# Could be a list
parity_dict = {0b0000: 0, 0b0001: 1, 0b0010: 1, 0b0011: 0,\
               0b0100: 1, 0b0101: 0, 0b0110: 0, 0b0111: 1,\
                0b1000: 1, 0b1001: 0, 0b1010: 0, 0b1011: 1,\
                0b1100: 0, 0b1101: 1, 0b1110: 1, 0b1111: 0}

# There's gotta be a better way to do this data structure ngl
# Doing a dict for clarity, consider a regular list
pi_s = {0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,\
        0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,\
        0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,\
        0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7}

pi_s_inv = {0x0: 0xE, 0x1: 0x3, 0x2: 0x4, 0x3: 0x8,\
            0x4: 0x1, 0x5: 0xC, 0x6: 0xA, 0x7: 0xF,\
            0x8: 0x7, 0x9: 0xD, 0xA: 0x9, 0xB: 0x6,\
            0xC: 0xB, 0xD: 0x2, 0xE: 0x0, 0xF: 0x5}

# Note the permutation network is involutary, so it's its own inverse
# Also NOTE THIS IS ZERO-INDEXED, WHILE THE CLASS EXAMPLES/FIGURE IN THE PROJECT SPEC
# IS ONE-INDEXED!!!
pi_p = [0, 3, 4, 1, 2, 5]

# One-indexed dictionary version
# pi_p = {1: 1, 2: 4, 3: 5, 4: 2, 5: 3, 6: 6}

# Instantiate table with minimum normalized values (maximum number of matches is 8,
# so default to 0 - 4)
normalized_linear_approx_table = [[-8 for x in range(16)] for y in range(16)]

# For each input_sum in range (0, 7)
#   For each output_sum in range (0, 7)
#       For each input_code in range (0, 7)
#           output_code = pi_s(input_code)
#           masked_input = input_code & input_sum
#           masked_output = output_code & output_sum
#           if(parity_dict[masked_input] == parity_dict[]):
#               normalized_linear_approx_table[input_sum][output_sum] += 1

for input_sum in range(16):
    for output_sum in range(16):
        for input_code in range(16):
            output_code = pi_s[input_code]
            # TODO: Consider renaming these variables, this might not make intuitive sense
            masked_input = input_code & input_sum
            masked_output = output_code & output_sum
            if(parity_dict[masked_input] == parity_dict[masked_output]):
                # TODO: make sure that the rows and columns aren't reversed here
                normalized_linear_approx_table[input_sum][output_sum] += 1

# TODO: print the table out, with headers marking rows and columns
print(tabulate(normalized_linear_approx_table,\
                headers=[x for x in range(16)],\
                    tablefmt="fancy_grid", showindex="always"))
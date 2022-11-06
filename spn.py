# Filename: spn.py
# Author: MATH 4175 Group 7 (Andrew Tran, Anthony Tran, Jack Greer, Jason Pak, Michael Peters)
# Date: 6 Nov 2022 (Date Last Modified: 6 Nov 2022, Jack Greer)
# Description: This file contains a Python algorithm that performs a linear attack
# on the "Baby SPN" and partially finds the key.

# This dict contains the corresponding XOR values for the numbers 0b000 through 0b111
# Could be a list
parity_dict = {0b000: 0, 0b001: 1, 0b010: 1, 0b011: 0,\
               0b100: 1, 0b101: 0, 0b110: 0, 0b111: 1}

# There's gotta be a better way to do this data structure ngl
# Doing a dict for clarity, consider a regular list
pi_s = {0b000: 0b110, 0b001: 0b101, 0b010: 0b001, 0b011: 0b000,\
        0b100: 0b011, 0b101: 0b010, 0b110: 0b111, 0b111: 0b100}

pi_s_inv = {0b000: 0b011, 0b001: 0b010, 0b010: 0b101, 0b011: 0b100,\
            0b100: 0b111, 0b101: 0b001, 0b110: 0b000, 0b111: 0b110}

# Note the permutation network is involutary, so it's its own inverse
# Also NOTE THIS IS ZERO-INDEXED, WHILE THE CLASS EXAMPLES/FIGURE IN THE PROJECT SPEC
# IS ONE-INDEXED!!!
pi_p = [0, 3, 4, 1, 2, 5]

# One-indexed dictionary version
# pi_p = {1: 1, 2: 4, 3: 5, 4: 2, 5: 3, 6: 6}

# Instantiate table with minimum normalized values (maximum number of matches is 8,
# so default to 0 - 4)
normalized_linear_approx_table = [[-4 for x in range(7)] for y in range(7)]

# For each input_sum in range (0, 7)
#   For each output_sum in range (0, 7)
#       For each input_code in range (0, 7)
#           output_code = pi_s(input_code)
#           masked_input = input_code & input_sum
#           masked_output = output_code & output_sum
#           if(parity_dict[masked_input] == parity_dict[]):
#               normalized_linear_approx_table[input_sum][output_sum] += 1

for input_sum in range(7):
    for output_sum in range(7):
        for input_code in range(7):
            output_code = pi_s[input_code]
            # TODO: Consider renaming these variables, this might not make intuitive sense
            masked_input = input_code & input_sum
            masked_output = output_code & output_sum
            if(parity_dict[masked_input] == parity_dict[masked_output]):
                # TODO: make sure that the rows and columns aren't reversed here
                normalized_linear_approx_table[input_sum][output_sum] += 1

# TODO: print the table out, with headers marking rows and columns
print(normalized_linear_approx_table)
# Filename: spn.py
# Author: MATH 4175 Group 7 (Andrew Tran, Anthony Tran, Jack Greer, Jason Pak, Michael Peters)
# Date: 6 Nov 2022 (Date Last Modified: 13 Nov 2022)
# Description: This file contains a Python algorithm that performs a linear attack
# on the "Baby SPN" and partially finds the fourth-round key K_4. 
# We are not given enough plaintext/ciphertext pairs to determine the full key; only the first

# For formatting and printing a table
from tabulate import tabulate

# This dict contains the corresponding XOR values for the numbers 0b000 through 0b111
parity_dict = {0b000: 0, 0b001: 1, 0b010: 1, 0b011: 0,\
               0b100: 1, 0b101: 0, 0b110: 0, 0b111: 1}

# This dict represents the S-box
pi_s = {0b000: 0b110, 0b001: 0b101, 0b010: 0b001, 0b011: 0b000,\
        0b100: 0b011, 0b101: 0b010, 0b110: 0b111, 0b111: 0b100}
# This dict represents the inverse of the S-box
pi_s_inv = {0b000: 0b011, 0b001: 0b010, 0b010: 0b101, 0b011: 0b100,\
            0b100: 0b111, 0b101: 0b001, 0b110: 0b000, 0b111: 0b110}

# This dict is used for converting decimal numbers to binary strings
bin_num_to_string = {0: "000", 1: "001", 2: "010", 3: "011",\
                    4: "100", 5: "101", 6: "110", 7: "111"}
# This dict is used for converting binary strings to decimal numbers
string_to_bin_num = {"000": 0, "001": 1, "010": 2, "011": 3,\
                    "100": 4, "101": 5, "110": 6, "111": 7}

# List of plaintext and ciphertext pairs for problem 4
plain_lin_attack_list = ["100111", "000111", "001100", "011000", "001000", "011010"]
cipher_lin_attack_list = ["100100", "110010", "111001", "011101", "001101", "101001"]

# Instantiate table with minimum normalized values (maximum number of matches is 8,
# so default to 0 - 4)
normalized_linear_approx_table = [[-4 for x in range(8)] for y in range(8)]

# Iterating through each input and output sum pair in the table
for input_sum in range(8):
    for output_sum in range(8):
        for input_code in range(8):
            # Grab output from S-box
            output_code = pi_s[input_code]
            
            # Mask the input and output codes
            masked_input = input_code & input_sum
            masked_output = output_code & output_sum
            
            # Increment value in table if masked input and masked output agree
            if(parity_dict[masked_input] == parity_dict[masked_output]):
                normalized_linear_approx_table[input_sum][output_sum] += 1

print("This is the normalized linear approximation table for this SPN (input sums along y-axis, output sums along x-axis):")
# Print the table out with headers marking rows and columns
print(tabulate(normalized_linear_approx_table,\
                headers=[x for x in range(8)],\
                    tablefmt="fancy_grid", showindex="always"))

# We know the input and output sum we want is input sum = 6 (on both S11 and S12),
# and output sum = 4 (on both S11 and S12)
# This will trace through to input sum 6 and output sum 4 on s-box S21, and then
# we're done

# I have this on paper right now, but the bias is determined as follows:
# 3 active s-boxes, each of which has bias -1/2 ((N_L(6, 4) - 4)/8)
# Then the total bias is 2^(3 - 1) * (-1/2)^3 = -4 / 8 = -1 / 2

# Launch attack: For K^4_1, K^4_2, K^4_3 in range (0b000, 0b111):
# Set count = 0
# for (plain, cipher) in plain_to_cipher_lin_attack_dict:
#   find h_1 through partial decryption
#       j_1 j_2 j_3 = c_1 XOR K^4_1, c_2 XOR K^4_2, c_3 XOR K^4_3
#       h_1 h_2 h_3 = pi_s_inv(j_1 j_2 j_3)
#       compute sum = p_1 XOR p_2 XOR p_4 XOR p_5 XOR h_1
#       if sum = 0: count += 1

# MOST guesses for K^4_1, K^4_2, K^4_3 will have a count of |plaintext-ciphertext pairs| / 2
# in our case, we have 3 pairs, so most guesses will have a count of 3
# the correct guess will have a count of (6 / 2)(1 +- bias(trail)) = 3(1 -+ 1/2) = 3/2, 9/2
# We will find the correct guess(es) by finding the MAXIMUM difference from 3, as
# detailed in slide deck 4.3
count = [0 for x in range(8)]
for k_guess in range(8):
    for pair_index in range(6):
        plaintext = plain_lin_attack_list[pair_index]
        ciphertext = cipher_lin_attack_list[pair_index]

        plain_first_half = plaintext[:3]
        plain_second_half = plaintext[3:]

        cipher_first_half = ciphertext[:3]
        cipher_second_half = ciphertext[3:]

        j = k_guess ^ string_to_bin_num[cipher_first_half]
        
        h = pi_s_inv[j]
        # Grab the first bit of H
        h_1 = (h & 4) >> 2
        
        #  compute sum = p_1 XOR p_2 XOR p_4 XOR p_5 XOR h_1
        sum = parity_dict[string_to_bin_num[plain_first_half] & 0b110] ^ \
                parity_dict[string_to_bin_num[plain_second_half] & 0b110] ^ \
                h_1
        
        if(sum == 0):
            count[k_guess] += 1

max_value = -1
max_value_list = []
max_key_value = -1
max_key_value_list = []

t = len(plain_lin_attack_list)
count_normalized = [0 for x in range(8)]

for k_guess in range(8):
    count_normalized[k_guess] = int(abs(count[k_guess] - (t / 2)))

    if(count_normalized[k_guess] >= max_value):
        max_value = count_normalized[k_guess]
        max_value_list.append(max_value)
        max_key = k_guess
        max_key_value_list.append(k_guess)

if(len(max_key_value_list) > 1):
    print("We have a Tie Between the Following Values: ", end="")
    for key in max_key_value_list:
        print(key, end=" ")
else:
    print("Max Key: " + str(max_key_value))
print()

sneed_table = [["K-guess:", 0, 1, 2, 3, 4, 5, 6, 7], \
    ["Count:", count[0], count[1], count[2], count[3], count[4], count[5], count[6], count[7]], \
    ["|Count - T/2|:", count_normalized[0], count_normalized[1], count_normalized[2], count_normalized[3], count_normalized[4], count_normalized[5], count_normalized[6], count_normalized[7]]]
print(tabulate(sneed_table, tablefmt = "fancy_grid"))

print("As you can see, guessing K = 0b000 and K = 0b010 both have a normalized count of 3")
print("Thus, we cannot determine whether the bit K^4_2 is equal to 0 or 1")

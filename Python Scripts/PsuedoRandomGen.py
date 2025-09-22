import random

# Step 1: Function to encode string to binary
def string_to_binary(input_string):
    return ''.join(format(ord(char), '08b') for char in input_string)

# Step 2: Function to count number of 0s and 1s
def count_zeros_ones(binary_string):
    zeros = binary_string.count('0')
    ones = binary_string.count('1')
    return zeros, ones

# Step 3: Function to generate OTP key using SystemRandom
def generate_otp_key(n):
    rand = random.SystemRandom()                                    # <-- NECCESSARY CODE FOR MARKS 
    return ''.join(rand.choice(["0", "1"]) for _ in range(n))

# Step 4: Function to XOR two binary sequences
def xor_binary(bin1, bin2):
    return ''.join(str(int(b1) ^ int(b2)) for b1, b2 in zip(bin1, bin2))

# Step 5: Function to convert binary back to string
def binary_to_string(binary_string):
    return ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))

# Step 6: Get user input for security parameter n
while True:
    try:
        n = int(input("Enter the security parameter n (length of binary sequence for encryption): "))
        break
    except ValueError:
        print("Invalid input. Please enter an integer.")

# Step 7: Get user input and validate length
while True:
    user_input = input("Enter a string to encode (must fit within n bits): ")
    binary_message = string_to_binary(user_input)

    if len(binary_message) <= n:
        break
    else:
        print(f"String too long. The binary sequence is {len(binary_message)} bits but must be ≤ {n} bits.")

# Step 8: Print binary sequence
print(f"\nBinary sequence: {binary_message}")

# Step 9: Count and print 0s and 1s in binary sequence
zeros, ones = count_zeros_ones(binary_message)
print(f"Number of 0s: {zeros}, Number of 1s: {ones}")

# Step 10: Generate and print OTP key
otp_key = generate_otp_key(len(binary_message))
print(f"Generated OTP Key: {otp_key}")

# Step 11: Encrypt message using OTP
encrypted_message = xor_binary(binary_message, otp_key)
print(f"Encrypted Binary: {encrypted_message}")

# Step 12: Count and print 0s and 1s in encrypted sequence
enc_zeros, enc_ones = count_zeros_ones(encrypted_message)
print(f"Number of 0s in Encrypted: {enc_zeros}, Number of 1s in Encrypted: {enc_ones}")

# Step 13: Decrypt the message
decrypted_message = xor_binary(encrypted_message, otp_key)
print(f"Decrypted Binary: {decrypted_message}")

# Step 14: Count and print 0s and 1s in decrypted sequence
dec_zeros, dec_ones = count_zeros_ones(decrypted_message)
print(f"Number of 0s in Decrypted: {dec_zeros}, Number of 1s in Decrypted: {dec_ones}")

# Step 15: Convert binary back and print original message
decoded_string = binary_to_string(decrypted_message)
print(f"Decrypted String: {decoded_string}")
# with open("C:/Users/Cmall/python/test.txt", "r") as input_file:
#     # Read the binary string from the input file
#     binary_string = input_file.read().strip()

# # Convert the binary string to bytes
# binary_data = bytes([int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8)])

# # Write the binary data to the output file
# with open("C:/Users/Cmall/python/out.txt", "wb") as output_file:
#     output_file.write(binary_data)
print(bin(100)[2:])


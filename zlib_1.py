# import base64
# import zlib
# import os

# def compress_and_split(input_file, chunk_size):
#     # Read the content of the file
#     with open(input_file, 'rb') as f:
#         data = f.read()

#     # Compress the data
#     compressed_data = zlib.compress(data)

#     # Split the compressed data into chunks
#     chunks = [compressed_data[i:i+chunk_size] for i in range(0, len(compressed_data), chunk_size)]

#     return chunks

# def encode_chunks_to_base64(chunks):
#     # Encode each chunk to Base64
#     encoded_chunks = [base64.b64encode(chunk).decode('utf-8') for chunk in chunks]

#     return encoded_chunks

# if __name__ == "__main__":
#     input_file = "OOP.pdf"  # Replace with your actual file name
#     #chunk_size = 1024  # Set your desired chunk size
#     chunk_size = 2048 
#     # Check if the file exists
#     if not os.path.isfile(input_file):
#         print(f"Error: File '{input_file}' not found.")
#     else:
#         # Compress and split the file
#         chunks = compress_and_split(input_file, chunk_size)

#         # Encode chunks to Base64
#         encoded_chunks = encode_chunks_to_base64(chunks)

#         # Print or save the encoded chunks with each chunk on a new line
#         with open("2.txt", "w") as output_file:
#             for i, chunk in enumerate(encoded_chunks):
#                 output_file.write(f"{chunk}\n")


import base64
import zlib
import os

def decode_base64_to_bytes(encoded_chunks):
    # Decode each Base64 chunk to bytes
    decoded_chunks = [base64.b64decode(chunk) for chunk in encoded_chunks]

    return decoded_chunks

def decompress_and_reconstruct(decoded_chunks):
    # Concatenate the decoded chunks
    compressed_data = b''.join(decoded_chunks)

    # Decompress the data
    original_data = zlib.decompress(compressed_data)

    return original_data

def save_original_file(original_data, output_file):
    # Write the decompressed data to the output file
    with open(output_file, 'wb') as f:
        f.write(original_data)

if __name__ == "__main__":
    input_file = "OOP.pdf"  # Replace with your actual file name
    chunk_size = 2048 
    output_file = "reconstructed_OOP.pdf"  # Replace with your desired output file name

    # Check if the file exists
    if not os.path.isfile("f.txt"):
        print(f"Error: File '2.txt' not found.")
    else:
        # Read the encoded chunks from the file
        with open("f.txt", "r") as input_file:
            encoded_chunks = [line.strip() for line in input_file]

        # Decode Base64 to bytes
        decoded_chunks = decode_base64_to_bytes(encoded_chunks)

        # Decompress and reconstruct the original data
        original_data = decompress_and_reconstruct(decoded_chunks)

        # Save the original data to a new file
        save_original_file(original_data, output_file)

        print(f"Original file has been reconstructed and saved to '{output_file}'.")

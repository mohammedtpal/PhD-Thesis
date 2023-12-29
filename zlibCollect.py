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
    #input_file = "OOP.rar"  # Replace with your actual file name
    chunk_size = 2048 
    output_file = "reconstructed_OOP.zip"  # Replace with your desired output file name

    # Check if the file exists
    if not os.path.isfile("GoOutPutBase64.txt"):
        print(f"Error: File 'GoOutPutBase64.txt' not found.")
    else:
        # Read the encoded chunks from the file
        with open("GoOutPutBase64.txt", "r") as input_file:
            encoded_chunks = [line.strip() for line in input_file]

        # Decode Base64 to bytes
        decoded_chunks = decode_base64_to_bytes(encoded_chunks)

        # Decompress and reconstruct the original data
        original_data = decompress_and_reconstruct(decoded_chunks)

        # Save the original data to a new file
        save_original_file(original_data, output_file)

        print(f"Original file has been reconstructed and saved to '{output_file}'.")

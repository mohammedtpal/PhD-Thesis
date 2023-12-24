import base64
import gzip
import os

def compress_and_split(input_file, chunk_size):
    # Read the content of the file
    with open(input_file, 'rb') as f:
        data = f.read()

    # Compress the data using gzip
    compressed_data = gzip.compress(data)

    # Split the compressed data into chunks
    chunks = [compressed_data[i:i+chunk_size] for i in range(0, len(compressed_data), chunk_size)]

    return chunks

def encode_chunks_to_base64(chunks):
    # Encode each chunk to Base64
    encoded_chunks = [base64.b64encode(chunk).decode('utf-8') for chunk in chunks]

    return encoded_chunks

if __name__ == "__main__":
    input_file = "OOP.pdf"  # Replace with your actual file name
    chunk_size = 1024  # Set your desired chunk size

    # Check if the file exists
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
    else:
        # Compress and split the file
        chunks = compress_and_split(input_file, chunk_size)

        # Encode chunks to Base64
        encoded_chunks = encode_chunks_to_base64(chunks)

        # Print or save the encoded chunks with each chunk on a new line
        with open("2.txt", "w") as output_file:
            for i, chunk in enumerate(encoded_chunks):
                output_file.write(f"Chunk {i+1}:\n{chunk}\n")

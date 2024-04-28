import base64
import zstandard as zstd
import os
import time

def compress_and_split(input_file, chunk_size):
    # Read the content of the file
    with open(input_file, 'rb') as f:
        data = f.read()

    # Compress the data using Zstandard
    cctx = zstd.ZstdCompressor(level=22)
    compressed_data = cctx.compress(data)
    original_size_bytes = len(data)

    # Calculate the size of the compressed data
    compressed_size_bytes = len(compressed_data)

    print(f"Size of original data: {original_size_bytes} bytes")
    print(f"Size of compressed data: {compressed_size_bytes} bytes")

    # Split the compressed data into chunks
    start_time_chunk = time.time()
    chunks = [compressed_data[i:i+chunk_size] for i in range(0, len(compressed_data), chunk_size)]
    end_time_chunk = time.time()
    total_time_chunk = end_time_chunk - start_time_chunk

    total_size_bytes = sum(len(chunk) for chunk in chunks)

    print(f"Total size of all chunks: {total_size_bytes} bytes")
    print(f"Total number of chunks: {len(chunks)}")
    print(f"Time consumed to chunk the file: {total_time_chunk:.4f} seconds")
    return chunks

def encode_chunks_to_base64(chunks):
    start_time_encode = time.time()
    # Encode each chunk to Base64
    encoded_chunks = [base64.b64encode(chunk).decode('utf-8') for chunk in chunks]
    end_time_encode = time.time()
    total_time_encode = end_time_encode - start_time_encode

    total_size_bytes = sum(len(encoded_chunk.encode('utf-8')) for encoded_chunk in encoded_chunks)
    print(f"Total size of encoded_chunks: {total_size_bytes} bytes")
    print(f"Time consumed to encode chunks to Base64: {total_time_encode:.4f} seconds")
    return encoded_chunks

if __name__ == "__main__":
    input_file = "OOP.pdf"  # Replace with your actual file name
    chunk_size = 4*1024  # Set your desired chunk size

    # Check if the file exists
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
    else:
        # Compress and split the file
        chunks = compress_and_split(input_file, chunk_size)

        # Encode chunks to Base64
        encoded_chunks = encode_chunks_to_base64(chunks)

        # Print or save the encoded chunks with each chunk on a new line
        with open("3.txt", "w") as output_file:
            for i, chunk in enumerate(encoded_chunks):
                output_file.write(f"{chunk}\n")

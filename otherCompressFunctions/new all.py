import os
import time
import lz4.frame
import gzip
import bz2
import lzma
import zlib
import base64

# Define compression functions

def rle_compress(data):
    # Your Run-Length Encoding (RLE) compression logic here
    compressed_data = ...  # Perform RLE compression
    return compressed_data

def shannon_fano_compress(data):
    # Your Shannon-Fano compression logic here
    compressed_data = ...  # Perform Shannon-Fano compression
    return compressed_data

def compress_and_measure(file_path, compression_function, extension):
    start_time = time.time()

    # Read the content of the file
    with open(file_path, 'rb') as f:
        data = f.read()

    # Compress the data using the provided compression function
    compressed_data = compression_function(data)

    # Write the compressed data to a new file
    compressed_file_path = file_path + extension
    with open(compressed_file_path, 'wb') as f:
        f.write(compressed_data)

    # Measure the size of the compressed file
    compressed_size = os.path.getsize(compressed_file_path)

    # Clean up: remove the compressed file
    os.remove(compressed_file_path)

    elapsed_time = time.time() - start_time

    return compressed_size, elapsed_time

if __name__ == "__main__":
    file_path = "your_file.pdf"  # Replace with the path to your file

    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
    else:
        print(f"Original file size: {os.path.getsize(file_path)} bytes")

        # Define compression functions
        compression_functions = [
            ('LZ4', lz4.frame.compress),
            ('gzip', gzip.compress),
            ('bzip2', bz2.compress),
            ('xz', lzma.compress),
            ('Zstandard', zlib.compress),
            ('Base64', lambda data: base64.b64encode(data)),
            ('Run-Length Encoding (RLE)', rle_compress),
            ('Shannon-Fano coding', shannon_fano_compress)
            # Add more compression functions here if needed
        ]

        # Measure and print the size of the compressed file for each compression function
        for compression_name, compression_function in compression_functions:
            compressed_size, elapsed_time = compress_and_measure(file_path, compression_function, extension='.' + compression_name.lower())
            print(f"{compression_name} compressed size: {compressed_size} bytes, Time: {elapsed_time:.4f} seconds")

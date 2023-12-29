import zlib

def compress_and_chunk(input_file, output_file, chunk_size):
    # Read the content of the file
    with open(input_file, 'rb') as f:
        data = f.read()

    # Compress the data using zlib
    compressed_data = zlib.compress(data)

    # Split the compressed data into chunks
    chunks = [compressed_data[i:i+chunk_size] for i in range(0, len(compressed_data), chunk_size)]

    # Write each chunk directly to the output file as binary
    with open(output_file, 'wb') as output_file:
        for chunk in chunks:
            output_file.write(chunk)

if __name__ == "__main__":
    input_file = "OOP.pdf"  # Replace with your actual file name
    output_file = "output.bin"    # Replace with your desired output file name
    chunk_size = 1024              # Set your desired chunk size

    # Compress, chunk, and save the file
    compress_and_chunk(input_file, output_file, chunk_size)

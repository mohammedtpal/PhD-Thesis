import base64
import zstandard as zstd
import os
import hashlib

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
    chunks = [compressed_data[i:i+chunk_size] for i in range(0, len(compressed_data), chunk_size)]
    total_size_bytes = sum(len(chunk) for chunk in chunks)

    print(f"Total size of all chunks: {total_size_bytes} bytes")
    return chunks

def encode_chunks_to_base64(chunks):
    # Encode each chunk to Base64
    encoded_chunks = [base64.b64encode(chunk).decode('utf-8') for chunk in chunks]
    total_size_bytes = sum(len(encoded_chunk.encode('utf-8')) for encoded_chunk in encoded_chunks)
    print(f"Total size of encoded_chunks: {total_size_bytes} bytes")
    return encoded_chunks

def hash_file_name(file_name):
    hasher = hashlib.sha256()
    hasher.update(file_name.encode('utf-8'))
    return hasher.hexdigest()

if __name__ == "__main__":
    fileName="4"
    SavePathChunks="/home/muhammed/go/src/github.com/mohammedt.pal@gmail.com/fabric-samples/asset-transfer-basic/application-gateway-typescript/256KB-Chunk"
    SavePathMeat="/home/muhammed/go/src/github.com/mohammedt.pal@gmail.com/fabric-samples/asset-transfer-basic/application-gateway-typescript/FilesMetaData"
    input_file = f"TestFiles/{fileName}.pdf"  # Replace with your actual file name
    chunk_size = 256*1024  # Set your desired chunk size

    # Check if the file exists
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
    else:
        # Compress and split the file
        chunks = compress_and_split(input_file, chunk_size)

        # Encode chunks to Base64
        encoded_chunks = encode_chunks_to_base64(chunks)

        # Print or save the encoded chunks with each chunk on a new line
        with open(f"{SavePathChunks}/{fileName}.txt", "w") as output_file:
            for i, chunk in enumerate(encoded_chunks):
                output_file.write(f"{chunk}\n")
                chuksCount=i

        print(f"Number of chunks: {chuksCount+1}")
        hashed_file_name = hash_file_name(input_file)
        print("Hashed file name:", hashed_file_name)
        with open(f"{SavePathMeat}/{fileName}.txt", "w") as output_file:
            output_file.write(f"{hashed_file_name}\n")
            output_file.write(str(chuksCount+1))
import base64
import zlib
import os
import zstandard as zstd
import time


def decode_base64_to_bytes(encoded_chunks):
    # Decode each Base64 chunk to bytes
    start_time_decode = time.time()
    decoded_chunks = [base64.b64decode(chunk) for chunk in encoded_chunks]
    end_time_decode = time.time()
    total_time_decode = end_time_decode - start_time_decode
    print(f"Time consumed to decode the chunks: {total_time_decode:.4f} seconds")

    return decoded_chunks

def decompress_and_reconstruct(decoded_chunks):
    # Concatenate the decoded chunks
    compressed_data = b''.join(decoded_chunks)

    # Decompress the data
    # original_data = zlib.decompress(compressed_data)
    start_time_decompress = time.time()

    decompressor = zstd.ZstdDecompressor()
    original_data = decompressor.decompress(compressed_data)
    end_time_decompress = time.time()
    total_time_decompress = end_time_decompress - start_time_decompress
    print(f"Time consumed to decompress the chunks: {total_time_decompress:.4f} seconds")
    return original_data

def save_original_file(original_data, output_file):
    # Write the decompressed data to the output file
    start_time = time.time()
    with open(output_file, 'wb') as f:
        f.write(original_data)
    end_time = time.time()
    total_time_save_original_file = end_time - start_time
    print(f"Time consumed to save original file: {total_time_save_original_file:.4f} seconds")

if __name__ == "__main__":
    #input_file = "OOP.rar"  # Replace with your actual file name
    chunk_size = 4*1024 
    output_file = "reconstructed_File.pdf"  # Replace with your desired output file name

    # Check if the file exists
    #if not os.path.isfile("/home/muhammed/go/src/github.com/mohammedt.pal@gmail.com/fabric-samples/asset-transfer-basic/application-gateway-typescript/result.txt"):
    if not os.path.isfile("/home/moh/go/src/github.com/mohammedt.pal@gmail.com/fabric-samples/asset-transfer-basic/application-gateway-typescript/result.txt"):

        print(f"Error: File not found.")
    else:
        # Read the encoded chunks from the file
        #with open("/home/muhammed/go/src/github.com/mohammedt.pal@gmail.com/fabric-samples/asset-transfer-basic/application-gateway-typescript/result.txt", "r") as input_file:
        with open("/home/moh/go/src/github.com/mohammedt.pal@gmail.com/fabric-samples/asset-transfer-basic/application-gateway-typescript/result.txt", "r") as input_file:
            encoded_chunks = [line.strip() for line in input_file]

        # Decode Base64 to bytes
        decoded_chunks = decode_base64_to_bytes(encoded_chunks)

        # Decompress and reconstruct the original data
        original_data = decompress_and_reconstruct(decoded_chunks)

        # Save the original data to a new file
        save_original_file(original_data, output_file)
        print(f"Size of original data: {len(original_data)} bytes")
        #print(f"Original file has been reconstructed and saved to '{output_file}'.")

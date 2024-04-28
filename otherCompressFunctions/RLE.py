import os
import time
from collections import Counter

class ShannonFanoNode:
    def __init__(self, symbol=None, probability=0, code=""):
        self.symbol = symbol
        self.probability = probability
        self.code = code
        self.left = None
        self.right = None

def shannon_fano_tree(symbols):
    if len(symbols) == 1:
        return ShannonFanoNode(symbol=symbols[0][0], probability=symbols[0][1])

    total_prob = sum(prob for _, prob in symbols)
    symbols = sorted(symbols, key=lambda x: x[1], reverse=True)

    cumulative_prob = 0
    split_index = None
    for i, (_, prob) in enumerate(symbols):
        cumulative_prob += prob
        if cumulative_prob >= total_prob / 2:
            split_index = i
            break

    if split_index is None:
        # If all symbols have the same probability, split at the middle
        split_index = len(symbols) // 2

    left_symbols = symbols[:split_index+1]
    right_symbols = symbols[split_index+1:]

    node = ShannonFanoNode()
    node.left = shannon_fano_tree(left_symbols)
    node.right = shannon_fano_tree(right_symbols)

    return node

def assign_codes(node, code=""):
    if node is None:
        return
    node.code = code
    print(f"Symbol: {node.symbol}, Code: {node.code}")  # Debug print
    assign_codes(node.left, code + "0")
    assign_codes(node.right, code + "1")


def shannon_fano_compress(data):
    freq_counter = Counter(data)
    symbols = freq_counter.most_common()
    tree_root = shannon_fano_tree(symbols)
    assign_codes(tree_root)

    encoded_data = ""
    for symbol in data:
        code = next((node.code for node in [tree_root] if node.symbol == symbol), "")  # Assign default code if symbol is not found
        encoded_data += code

    # Debug: Print symbols and their corresponding codes
    print("Symbols and codes:")
    for symbol, code in [(node.symbol, node.code) for node in [tree_root]]:
        print(f"Symbol: {symbol}, Code: {code}")

    return encoded_data.encode('utf-8')




def compress_and_measure(file_path):
    start_time = time.time()

    # Read the content of the file
    with open(file_path, 'rb') as f:
        data = f.read()

    # Compress the data using Shannon-Fano coding
    compressed_data = shannon_fano_compress(data)

    # Write the compressed data to a new file
    compressed_file_path = file_path + '.sf'
    with open(compressed_file_path, 'wb') as f:
        f.write(compressed_data)

    # Measure the size of the compressed file
    compressed_size = os.path.getsize(compressed_file_path)

    # Clean up: remove the compressed file
    os.remove(compressed_file_path)

    elapsed_time = time.time() - start_time

    return compressed_size, elapsed_time

if __name__ == "__main__":
    file_path = "OOP.pdf"  # Replace with the path to your file

    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
    else:
        print(f"Original file size: {os.path.getsize(file_path)} bytes")

        # Compress the file using Shannon-Fano coding and measure compression time
        compressed_size, elapsed_time = compress_and_measure(file_path)
        
        print(f"Compressed file size: {compressed_size} bytes")
        print(f"Elapsed time: {elapsed_time:.4f} seconds")

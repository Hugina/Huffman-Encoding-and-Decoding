class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

def read_traversal(file, bytes_per_data):
    # skip the newline that separates the data from the traversals
    while True:
        char = file.read(1)
        if char == b'\n':  # If it's a newline, move past it
            break

    # Read how long the traversal list is
    traversal_length = int.from_bytes(file.read(bytes_per_data), 'big')
    traversal = []  # A list to hold the traversal data
    for _ in range(traversal_length): # Read the traversal data
        prefix = file.read(1)  
        if prefix == b'\xFF':  
            data = int.from_bytes(file.read(1), 'big')
        else:  
            data = file.read(1).decode()  # Change bytes to text
        traversal.append(data)  # Add to our list
    return traversal

def read_compressed_file(file):
    # size of chunks of data
    bytes_per_data = 5  
    length_byte_array = file.read(bytes_per_data) # Read metadata size
    
    # Change the metadata from bytes to a number
    length = int.from_bytes(length_byte_array, 'big')

    # read the compressed info including a byte for padding
    compressed_data_with_padding = file.read(length)
                    
    padding = compressed_data_with_padding[len(compressed_data_with_padding) - 1]

    # get only the part that has the compressed data
    compressed_data = compressed_data_with_padding[:len(compressed_data_with_padding) - 1]
                    
    # Change the compressed data into a binary string 
    bit_string = ''.join(format(byte, '08b') for byte in compressed_data)
                    
    if padding > 0:  
        bit_string = bit_string[: len(bit_string) - padding]

    #  read the  traversals 
    inorder_traversal = read_traversal(file, bytes_per_data)
    preorder_traversal = read_traversal(file, bytes_per_data)
    return bit_string, inorder_traversal, preorder_traversal

def build_tree(preorder, inorder):
    if not preorder or not inorder:
        return None

    #  as we learned from data structers course, the first element in the preorder list is the root
    root_data = preorder[0]
    root = Node(root_data)
    root_index_inorder = inorder.index(root_data)
    # Split the inorder into two parts around the main node
    left_subtree_inorder = inorder[:root_index_inorder]
    right_subtree_inorder = inorder[root_index_inorder + 1:]
    left_subtree_size = len(left_subtree_inorder)
    left_subtree_preorder = preorder[1:1 + left_subtree_size]
    right_subtree_preorder = preorder[1 + left_subtree_size:]

   
    root.left = build_tree(left_subtree_preorder, left_subtree_inorder)
    root.right = build_tree(right_subtree_preorder, right_subtree_inorder)

    return root

def decode_huffman(bit_string, root):
    decoded_data = ''
    current_node = root  # Start at the top of the tree
    for bit in bit_string:  
        # Depending on the bit, move left or right
        if bit == '0':
            current_node = current_node.left
        else:  # bit == 1
            current_node = current_node.right

        # If we hit a leaf node, it's a character for sure
        if current_node.left is None and current_node.right is None:
            decoded_data += current_node.data  # Add the character to our string
            current_node = root  # Go back to the top to start decoding the next bit

    return decoded_data

def main():
    # Open the file to read from it
    file =  open('Alice_in_wonderlands_compressed.txt', 'rb')
    bit_string, inorder_traversal, preorder_traversal = read_compressed_file(file)
    root = build_tree(preorder_traversal, inorder_traversal)  # Make the tree
    decoded_data = decode_huffman(bit_string, root)  # Decode the string
    
    # Save the decoded string in a new file
    decompressed_file =  open('Alice_in_wonderlands_decompressed.txt', 'w')
    decompressed_file.write(decoded_data)
    decompressed_file.close()
    
    # Check if the original and decompressed files are the same
    original_file = open('Alice_in_wonderlands.txt', 'r')
    original_data = original_file.read()
    original_file.close()
    if (original_data == decoded_data):
        print("The original file and the decompressed file are the same!")
        print("Submitted by: Dolev Kaiser 208603357 and Nadav Hugi 208572677")

if __name__ == "__main__":
    main()

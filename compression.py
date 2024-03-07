class HuffNode:
    def __init__(self, char, frequency):
        self.char = char
        self.freq = frequency
        self.right = None
        self.left = None


def CreateHuffTree(txt):# Create the huffman tree from the given text
    listNodes = []
    frequencyStruct = {}
    valueNode = 0
    for i in txt:  # Count the frequency of each character in the text
        if i in frequencyStruct:
            frequencyStruct[i] = frequencyStruct[i] + 1
        else:
            frequencyStruct[i] = 1
    for char, freq in frequencyStruct.items(): # Create a list of nodes with the frequency of each character
        listNodes.append(HuffNode(char, freq))
    while len(listNodes) > 1:  # Create the huffman tree
        listNodes = sorted(listNodes, key=lambda i: i.freq)
        left = listNodes.pop(0)
        right = listNodes.pop(0)
        tempParentNode = HuffNode(valueNode, left.freq + right.freq) 
        valueNode = valueNode + 1
        tempParentNode.left = left
        tempParentNode.right = right
        listNodes.append(tempParentNode)
    return listNodes[0]


def CreateHuffTreeCodes(node, codes, iterCode):  # Create the huffman codes for each character
    if node is None:
        return
    if node.left is None and node.right is None:
        codes[node.char] = iterCode
        return
    CreateHuffTreeCodes(node.left, codes, iterCode + "0")
    CreateHuffTreeCodes(node.right, codes, iterCode + "1")
    return codes


def CompressedText(txt, codes):
    compressedTxt = ""
    for i in txt:
        compressedTxt = compressedTxt + codes[i]
    return compressedTxt


def inorder(node, traversal=[]): # create the inorder traversal 
    if node:
        inorder(node.left, traversal)
        traversal.append(node.char)
        inorder(node.right, traversal)


def preorder(node, traversal=[]): # create the preorder traversal
    if node:
        traversal.append(node.char)
        preorder(node.left, traversal)
        preorder(node.right, traversal)


def write_traversal(file, traversal_data, bytes_per_data): # write the traversal to the file
    file.write(len(traversal_data).to_bytes(bytes_per_data, 'big'))
    for i in traversal_data:
        prefix = b'\xFF' if isinstance(i, int) else b'\x00'
        data = i.to_bytes(1, 'big') if isinstance(i, int) else i.encode()
        file.write(prefix + data)


def compress_and_write_data(huffTreeCodes, inorder_traversal, preorder_traversal, CompressedTextFilePath): # compress the data and write it to the file
    byte_array = bytearray([int(huffTreeCodes[i:i + 8].ljust(8, '0'), 2) for i in range(0, len(huffTreeCodes), 8)] + [
        8 - len(huffTreeCodes) % 8])
    bytes_per_data = 5
    file = open(CompressedTextFilePath, 'wb')
    file.write(len(byte_array).to_bytes(bytes_per_data, 'big'))
    file.write(byte_array)
    file.write(b'\n')
    write_traversal(file, inorder_traversal, bytes_per_data)
    file.write(b'\n')
    write_traversal(file, preorder_traversal, bytes_per_data)


def main():
    txt_File_Path = "/Users/nadavhugi/python/Algorithm-Design/Alice_in_wonderlands.txt"
    CompressedTextFilePath = "/Users/nadavhugi/python/Algorithm-Design/Alice_in_wonderlands_compressed.txt"
    txt_file = open(txt_File_Path, 'r')
    txt_File_Content = txt_file.read()
    huffTreeRoot = CreateHuffTree(txt_File_Content)
    huffTreeCodes = CreateHuffTreeCodes(huffTreeRoot, {}, "")
    compressedTextBits = CompressedText(txt_File_Content, huffTreeCodes)
    inorder_traversal = []
    preorder_traversal = []
    inorder(huffTreeRoot, inorder_traversal)
    preorder(huffTreeRoot, preorder_traversal)
    compress_and_write_data(compressedTextBits, inorder_traversal, preorder_traversal, CompressedTextFilePath)


if __name__ == "__main__":
    main()
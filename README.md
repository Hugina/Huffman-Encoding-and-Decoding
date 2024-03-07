Huffman Coding Compression and Decompression

Overview

This project focuses on implementing Huffman coding for file compression and decompression using Python. Huffman coding is an efficient method of encoding characters based on their frequency of occurrence in the text, allowing for significant reductions in file size. This implementation includes two main scripts: one for compression and another for decompression.

Objective

To develop Python scripts that efficiently compress and decompress text files using Huffman coding, ensuring data integrity and minimizing file size.

Features

Compression: Converts a text file into a compressed format using Huffman coding, outputting the compressed data and the Huffman tree necessary for decompression.
Decompression: Rebuilds the Huffman tree from the compressed file and accurately decompresses the data back to its original form.
Implementation Details

Languages & Libraries: Implemented in Python, leveraging common libraries such as Numpy, Scipy, and Pandas for data manipulation and operations.
Huffman Tree Serialization: Includes a novel approach for encoding and decoding the Huffman tree within the compressed file using preorder and inorder traversals, ensuring the tree can be reconstructed during decompression.
Binary Encoding Challenges: Addresses the challenge of converting Huffman coded binary sequences to text format and back, taking care of special cases like non-printable characters.

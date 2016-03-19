'''
Matasano Crypto Pals
Challenge 5
Jonathan Eskeldson

Takes a filename and key via command line arguments, and prints the encryption
of the file with repeating-key XOR with the provided key.
'''

import sys
from common import *

SAMPLE_FILENAME = "05_txt"
SAMPLE_KEY = "ICE"

def main():
        if len(sys.argv) < 3:
                f = open(SAMPLE_FILENAME, "r")
                key = SAMPLE_KEY
        else:
                f = open(argv[1])
                key = argv[2]

        pt = ""
        for line in f:
                pt += line.rstrip() + "\n"

        # use whole pt except for last extra "\n"
        print repeat_xor_cipher(key, pt[:-1]).encode("hex")

if __name__ == "__main__":
        main()

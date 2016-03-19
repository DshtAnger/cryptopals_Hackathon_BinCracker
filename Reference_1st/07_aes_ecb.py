'''
Matasano Crypto Pals
Challenge 7
Jonathan Eskeldson

Takes a filename and a key via command line arguments.  Decrypts the file
using AES-128 with the provided key, and prints it to console.
'''

# uses pycrypto for AES
from Crypto.Cipher import AES
import sys

import common

SAMPLE_KEY = "YELLOW SUBMARINE"
SAMPLE_FILENAME = "07_txt"

def main():
        if len(sys.argv) < 3:
                key = SAMPLE_KEY
                filename = SAMPLE_FILENAME
        else:
                key = sys.argv[1]
                filename = sys.argv[2]
        f = open(filename, "r")
        ciphertext = ""
        for line in f:
                ciphertext += common.b64decode(line.rstrip())

        plaintext = ""
        for i in range(0, len(ciphertext), 16):
                plaintext += common.aes_decrypt_block(ciphertext[i:i+16], key)

        print plaintext
        
if __name__ == '__main__':
        main()

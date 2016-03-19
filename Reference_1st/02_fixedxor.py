'''
Matasano Crypto Pals
Challenge 2
Jonathan Eskeldson
Takes two equal-length buffers via command line and produces their XOR sum
'''

import sys
from common import *

SAMPLE_BUFFER1 = "1c0111001f010100061a024b53535009181c"
SAMPLE_BUFFER2 = "686974207468652062756c6c277320657965"

def main():
        if len(sys.argv) < 3:
                buf1 = SAMPLE_BUFFER1.decode("hex")
                buf2 = SAMPLE_BUFFER2.decode("hex")
        else:
                buf1 = sys.argv[1].decode("hex")
                buf2 = sys.argv[2].decode("hex")

        buf_res = ""
        for i in range(len(buf1)):
                buf_res += chr(ord(buf1[i]) ^ ord(buf2[i]))

        print xor_strings(buf1, buf2).encode("hex")

if __name__ == "__main__":
        main()

'''
Matasano Crypto Pals
Challenge 8
Jonathan Eskeldson

Takes a filename via command line.  Finds a line encrypted with ECB mode.
'''

import sys
from common import *

SAMPLE_FILENAME = "08_txt"

def main():
        if len(sys.argv) < 2:
                f = open(SAMPLE_FILENAME, "r")
        else:
                f = open(argv[1], "r")

        for line in f:
                data = line.rstrip().decode("hex")
                blocks = dict()

                assert len(data) % 16 == 0
                for i in range(0, len(data), 16):
                        cur_block = data[i:i+16]
                        if cur_block in blocks:
                                blocks[cur_block] = blocks[cur_block] + 1
                        else:
                                blocks[cur_block] = 1

                if max(blocks.values()) > 1:
                        print "Found following candidate for ECB-encrypted text:"
                        print line.rstrip()

        
if __name__ == "__main__":
        main()

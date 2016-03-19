'''
Matasano Crypto Pals
Challenge 4
Jonathan Eskeldson

Takes a filename via commandline, and searches for a line that's been encrypted
by XORing the plaintext with a single byte
'''

import sys
from common import *

SAMPLE_FILENAME = "04_txt"

def main():
        if len(sys.argv) < 2:
                f = open(SAMPLE_FILENAME, "r")
        else:
                f = open(sys.argv[1], "r")

        best_dist = 100

        for line in f:
                data = line.rstrip().decode("hex")
                tmp_key, tmp_pt, tmp_dist = break_single_xor(data)
                if tmp_dist < best_dist:
                        best_key = tmp_key
                        best_pt = tmp_pt
                        best_dist = tmp_dist

        print "recovered key: " + str(best_key)
        print "recovered plaintext: " + str(best_pt)
        print "best distance: " + str(best_dist)

if __name__ == '__main__':
        main()

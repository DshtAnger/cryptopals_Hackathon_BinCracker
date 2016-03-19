'''
Matasano Crypto Pals
Challenge 3
Jonathan Eskeldson

Takes a hex-encoded string from command line that's been encrypted by XORing a
single character against the string.  Recovers the key and decrypts the
message.
'''

import sys
from common import *

SAMPLE_CT = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def main ():
        if len(sys.argv) < 2:
                ct = SAMPLE_CT.decode("hex")
        else:
                ct = sys.argv[1].decode("hex")

        key, pt, dist = break_single_xor (ct)
        print "recovered key: " + str(key)
        print "recovered message: " + pt
        print "total distance from english profile: " + str(dist)

if __name__ == '__main__':
        main()

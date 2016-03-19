'''
Matasano Crypto Pals
Challenge 1
Jonathan Eskeldson

Takes a hex-encoded string via command line, converts it to a base64
encoded string, and back again. 
'''

import sys
import base64
import binascii
from common import *
import common

SAMPLE_STRING = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

def b64encode(s):
        table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        assert len(table) == 64

        ret = ""
        for i in range(0, len(s), 3):
                if i + 2 < len(s):
                        chunk = (ord(s[i]) << 16) | (ord(s[i+1]) << 8) | (ord(s[i+2]))
                        ret += table[chunk >> 18] + table[(chunk >> 12) & 0x3f] + table[(chunk >> 6) & 0x3f] + table[chunk & 0x3f]
                elif i + 1 < len(s):
                        chunk = (ord(s[i]) << 16) | (ord(s[i+1]) << 8)
                        ret += table[chunk >> 18] + table[(chunk >> 12) & 0x3f] + table[(chunk >> 6) & 0x3f] + "="
                else:
                        chunk = (ord(s[i]) << 16)
                        ret += table[chunk >> 18] + table[(chunk >> 12) & 0x3f] + "=="

        return ret

def b64decode(s):
        table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        assert len(table) == 64
        assert len(s) % 4 == 0

        ret = ""
        for i in range(0, len(s) - 4, 4):
                chunk = (table.index(s[i]) << 18) | (table.index(s[i+1]) << 12) | (table.index(s[i+2]) << 6) | table.index(s[i+3])
                ret += chr(chunk >> 16) + chr((chunk >> 8) & 0xff) + chr(chunk & 0xff)

        if s[-2:] == "==":
                chunk = (table.index(s[-4]) << 18) | (table.index(s[-3]) << 12)
                ret += chr(chunk >> 16)
        elif s[-1] == "=":
                chunk = (table.index(s[-4]) << 18) | (table.index(s[-3]) << 12) | (table.index(s[-2]) << 6)
                ret += chr(chunk >> 16) + chr((chunk >> 8) & 0xff)
        else:
                chunk = (table.index(s[-4]) << 18) | (table.index(s[-3]) << 12) | (table.index(s[-2]) << 6) | table.index(s[-1])
                ret += chr(chunk >> 16) + chr((chunk >> 8) & 0xff) + chr(chunk & 0xff)

        return ret

def main():
        if len(sys.argv) < 2:
                s = SAMPLE_STRING
        else:
                s = sys.argv[1]

        assert s == base64_to_hex(hex_to_base64(s))

        # print "hex encoded string: " + s
        # print "base64 encoding: " + hex_to_base64(s)
        # print "hex encoding of base64 encoding: " + base64_to_hex(hex_to_base64(s))

        for _ in range(100):
                t = common.randbytes(random.randint(1, 40))
                if t != b64decode(b64encode(t)):
                        print binascii.hexlify(t)
                        print b64encode(t)
                        print binascii.hexlify(b64decode(b64encode(t)))
                        print "-----"



        # print SAMPLE_STRING.decode("hex")
        # print b64encode(SAMPLE_STRING.decode("hex"))

if __name__ == "__main__":
        main()

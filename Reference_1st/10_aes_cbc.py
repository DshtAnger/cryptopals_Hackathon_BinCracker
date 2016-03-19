import sys

import common

import random
import binascii

SAMPLE_KEY = "YELLOW SUBMARINE"
SAMPLE_FILENAME = "10_txt"


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

        print common.aes_cbc_decrypt(ciphertext, key, "\x00" * 16)
        
        
        if False:
                for _ in range(1000):
                        key = common.randbytes(16)
                        pt = common.randbytes(random.randint(1, 64))
                        iv = common.randbytes(16)

                        AFTER = binascii.hexlify(common.aes_cbc_decrypt(common.aes_cbc_encrypt(pt, key, iv), key, iv))

                        PT = binascii.hexlify(common.pkcs7_pad(pt, len(pt) + (16 - (len(pt) % 16))))

                        print PT == AFTER

                
if __name__ == '__main__':
        main()

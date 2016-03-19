import random
import binascii

import common

def encryption_oracle(pt):
        key = common.randbytes(16)
        pt = common.randbytes(random.randint(5, 10)) + pt + common.randbytes(random.randint(5, 10))

        if random.randint(0, 1) == 1:
                print "actually doing ECB"
                ret = common.aes_ecb_encrypt(pt, key)
        else:
                print "actually doing CBC"
                ret = common.aes_cbc_encrypt(pt, key, common.randbytes(16))

        return ret

def main():
        for _ in range(100):
                trial = encryption_oracle("A" * 43)
                if trial[16:32] == trial[32:48]:
                        print "trial reports ECB"
                else:
                        print "trial reports CBC"
                print "--------"
        

if __name__ == '__main__':
        main()

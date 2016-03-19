import binascii

import common

TARGET_PT = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

key = ""

def setup_oracle():
        global key
        key = common.randbytes(16)

def encryption_oracle(pt):
        global key
        return common.aes_ecb_encrypt(pt + common.b64decode(TARGET_PT), key)

def main():
        setup_oracle()

        trial_string = "A"
        prev_length = len(encryption_oracle("A"))

        new_length = prev_length
        while (new_length == prev_length):
                trial_string += "A"
                new_length = len(encryption_oracle(trial_string))

        blocksize = new_length - prev_length
        print blocksize

        # confirm ecb
        test_ecb = encryption_oracle("A" * 2*blocksize)
        if test_ecb[0:16] == test_ecb[16:32]:
                print "using ecb: true!"
        else:
                print "using ecb: false!"
                exit(1)

        # n used for readability; n = len(bytes_recovered)
        bytes_recovered = ""
        n = 0
        blocknum = (n+1) / blocksize

        print prev_length
        for _ in range(prev_length):
                slide = "A" * (blocksize - ((n + 1) % blocksize))
                target = encryption_oracle(slide)[blocksize * blocknum : blocksize * (blocknum + 1)]
                print slide + bytes_recovered + "  (%d %d)" % (n, blocknum)
                # print binascii.hexlify(target)

                candidates = [0] * 0x100
                for t in range(0, 0x100):
                        candidates[t] = encryption_oracle(slide + bytes_recovered + chr(t))[blocksize * blocknum : blocksize * (blocknum + 1)]

                # print map(binascii.hexlify, candidates)
                if candidates.count(target) >= 2:
                        print "unlucky!"
                        exit(1)

                bytes_recovered += chr(candidates.index(target))
                n = n + 1
                blocknum = (n+1) / blocksize

        # technically this crashes before we reach here
        # once we reach the padding, the padding changes between the "target" and
        # "slide+recovered+chr(t)", so we won't have any matches

        print bytes_recovered

if __name__ == '__main__':
        main()

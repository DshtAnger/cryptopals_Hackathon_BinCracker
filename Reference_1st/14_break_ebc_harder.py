import binascii
import random

import common

TARGET_PT = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

key = ""

def setup_oracle():
        global key
        key = common.randbytes(16)

def encryption_oracle(pt):
        global key
        return common.aes_ecb_encrypt(common.randbytes(random.randint(2, 50)) + pt + common.b64decode(TARGET_PT), key)

def get_blocksize():
        size_list = []
        for _ in range(100):
                size_list.append(len(encryption_oracle("A")))

        size_list.sort()
        if size_list[0] == size_list[-1]:

                trial_string = "A"
                prev_length = len(encryption_oracle("A"))

                new_length = prev_length
                while (new_length == prev_length):
                        trial_string += "A"
                        new_length = len(encryption_oracle(trial_string))

                blocksize = new_length - prev_length

        else:
                for i in range(1, len(size_list)):
                        if size_list[i] != size_list[i-1]:
                                blocksize = size_list[i] - size_list[i-1]
                                break

        return blocksize

def grab_controllable_block(buf, blocksize, offset):
        blocknum = 1
        while buf[blocknum*blocksize:(blocknum+1)*blocksize] != buf[(blocknum-1)*blocksize:blocknum*blocksize]:
                blocknum = blocknum + 1

        while buf[blocknum*blocksize:(blocknum+1)*blocksize] == buf[(blocknum-1)*blocksize:blocknum*blocksize]:
                blocknum = blocknum + 1

        return buf[(blocknum + offset)*blocksize:(blocknum+1 + offset)*blocksize]


def main():
        setup_oracle()

        blocksize = get_blocksize()
        print "blocksize = %s" % (blocksize)
        
        # confirm ecb
        test_ecb = encryption_oracle("A" * 3*blocksize)
        found = False
        for i in range(0, len(test_ecb) - blocksize, blocksize):
                if test_ecb[i:i+blocksize] == test_ecb[i+blocksize:i+2*blocksize]:
                        found = True
                        break

        if not found:
                print "not using ecb, aborting"
                exit(1)

        # n used for readability; n = len(bytes_recovered)
        bytes_recovered = ""
        n = 0
        blocknum = n / blocksize

        # pick 999; it'll just start generating nonsense eventually
        for _ in range(999):
                encrypted_slides = []
                slide = "A" * (3 * blocksize) + "A" * (blocksize - ((n + 1) % blocksize))
                while len(encrypted_slides) != blocksize:
                        t = grab_controllable_block(encryption_oracle(slide), blocksize, blocknum) 
                        if t not in encrypted_slides and t != "":
                                encrypted_slides.append(t)


                candidates = []
                for t in range(0, 0x100):
                        possibilities = []
                        num_oracles = 0
                        while len(possibilities) != blocksize:
                                buf = grab_controllable_block(encryption_oracle(slide + bytes_recovered + chr(t)), blocksize, blocknum)
                                num_oracles = num_oracles + 1
                                if buf not in possibilities and buf != "":
                                        possibilities.append(buf)

                        candidates.append(possibilities)


                matches = []
                for t in range(0, 0x100):
                        for candidate in candidates[t]:
                                if candidate in encrypted_slides:
                                        matches.append(t)

                if n == 0:
                        newbyte = chr(matches[0])
                        for match in matches:
                                if match != 0x41:
                                        newbyte = chr(match)
                                        break
                else:
                        counts = dict()
                        for match in matches:
                                if match in counts:
                                        counts[match] = counts[match] + 1
                                else:
                                        counts[match] = 1
                        
                        for t in counts:
                                if counts[t] == (n % blocksize) + 1:
                                        newbyte = chr(t)


                bytes_recovered += newbyte
                print bytes_recovered
                n = n + 1
                blocknum = n / blocksize

        # technically this crashes before we reach here
        # once we reach the padding, the padding changes between the "target" and
        # "slide+recovered+chr(t)", so we won't have any matches

        print bytes_recovered

if __name__ == '__main__':
        main()

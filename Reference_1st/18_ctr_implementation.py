import random
import common
import binascii
import struct

target = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="

def aes_ctr_encrypt(pt, key, nonce):
        ctr = 0
        ct = ""
        for i in range(0, len(pt), 16):
                # little endian ctr string
                keystream_input = struct.pack("<QQ", nonce, ctr)
                keystream = common.aes_encrypt_block(keystream_input, key)
                ct += common.xor_strings(keystream[:len(pt[i:i+16])], pt[i:i+16])
                ctr = (ctr + 1) % (2 ** 64)

        return ct
                

def aes_ctr_decrypt(ct, key, nonce):
        return aes_ctr_encrypt(ct, key, nonce)

def main():
        ct = aes_ctr_encrypt("HELLO" * 50, "YELLOW SUBMARINE", 0)
        pt = aes_ctr_decrypt(ct, "YELLOW SUBMARINE", 0)
        print aes_ctr_decrypt(common.b64decode(target), "YELLOW SUBMARINE", 0)

        for _ in range(100):
                # print "boop"
                key = common.randbytes(16)
                nonce = random.randint(0, 2**64 - 1)
                pt = common.randbytes(random.randint(3, 1000))
                ct = aes_ctr_encrypt(pt, key, nonce)
                if pt != aes_ctr_decrypt(ct, key, nonce):
                        print "mismatch: pt = %s, ct = %s, key = %s, nonce = %d" % (binascii.hexlify(pt), binascii.hexlify(ct), binascii.hexlify(key), nonce)
                        break


if __name__ == '__main__':
        main()

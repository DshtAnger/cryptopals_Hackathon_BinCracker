import common
import binascii
import random

key = ""

choices = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc="
                ,"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic="
                ,"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw=="
                ,"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg=="
                ,"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl"
                ,"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA=="
                ,"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw=="
                ,"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8="
                ,"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g="
                ,"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
        ]

def setup_oracle():
        global key
        key = common.randbytes(16)

def get_target():
        global key
        IV = common.randbytes(16)
        text = common.b64decode(random.choice(choices))

        ct = common.aes_cbc_encrypt(text, key, IV)
        return ct, IV

def decryption_oracle(ct, IV):
        global key

        try:
                pt = common.aes_cbc_decrypt(ct, key, IV)
                unpadpt = common.unpad(common.aes_cbc_decrypt(ct, key, IV), 16)
        except common.InvalidPaddingError as e:
                return False

        # print hex(ord(pt[-1]))
        return True

def solve_block(curblock, prevblock):
        intermediate = [""] * 16
        bytes_recovered = ""
        nextpad = ""
        for i in range(15, -1, -1):
                # print i
                # print bytes_recovered
                # print nextpad
                slide = "A" * i 
                candidates = []
                for t in range(0x100):
                        if decryption_oracle(curblock, slide + chr(t) + nextpad):
                                candidates.append(chr(t))
                if len(candidates) != 1:
                        print "unlucky!"
                        # print candidates
                        exit(1)
                else:
                        match = candidates[0]
                        intermediate[i] = chr(ord(match) ^ (16 - i))
                        bytes_recovered = chr(ord(match) ^ ord(prevblock[i]) ^ (16 - i)) + bytes_recovered
                        nextpad = common.xor_strings((chr(16 - i + 1) * (16 - i)), intermediate[i:])

        return bytes_recovered


def main():
        setup_oracle()
        ct, IV = get_target()

        testiv = "A" * 15
        candidates = []
        intermediate = [""] * 16
        for i in range(0x100):
                if decryption_oracle(ct[0:16], testiv + chr(i)):
                        candidates.append(chr(i))

        if len(candidates) > 1:
                print "unlucky!"
                print candidates
                exit(1)
        else:
                # print hex(ord(candidates[0]))
                # print hex(ord(ct[15]))
                pt = chr(ord(chr(ord(candidates[0]) ^ ord(IV[15]) ^ 1)))
                # print hex(ord(chr(ord(candidates[0]) ^ ord(IV[15]) ^ 1)))
                intermediate[15] = chr(ord(candidates[0]) ^ 1)

        
        bytes_recovered = ""
        bytes_recovered += solve_block(ct[0:16], IV)
        for i in range(16, len(ct), 16):
                bytes_recovered += solve_block(ct[i:i+16], ct[i-16:i])
        # bytes_recovered += solve_block(ct[16:32], ct[0:16])
        # bytes_recovered += solve_block(ct[32:48], ct[16:32])
        print bytes_recovered

        # print decryption_oracle(ct, IV)

if __name__ == '__main__':
        main()

import common
import binascii

key = ""
IV = ""

def setup_oracle():
        global key
        global IV

        key = common.randbytes(16)
        IV = common.randbytes(16)

def encryption_oracle(pt):
        global key
        global IV

        sanitized = pt.replace(";", "%%3b").replace("=", "%%3d")

        return common.aes_cbc_encrypt("comment1=cooking%%20MCs;userdata=%s;comment2=%%20like%%20a%%20pound%%20of%%20bacon" % sanitized, key, IV)

def decryption_oracle(ct):
        global key
        global IV

        try:
                t = common.aes_cbc_decrypt(ct, key, IV).index(";admin=true;")
        except:
                return False

        return True

def main():
        setup_oracle()
        ct = encryption_oracle("A" * 32)
        cut = ct[16:32]
        paste = common.xor_strings(common.xor_strings("BBBB;admin=true;", "A" * 16), cut)
        print decryption_oracle(ct[0:16] + paste + ct[32:])

if __name__ == '__main__':
        main()

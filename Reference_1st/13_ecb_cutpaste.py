import binascii

import common

key = ""

class Profile:
        def __init__(self, email=None, uid=None, role=None):
                self.email = email
                self.uid = uid
                self.role = role

        def decode(self, encoded):
                params = encoded.split("&")
                self.email = params[0].split("=")[1]
                self.uid = int(params[1].split("=")[1])
                self.role = params[2].split("=")[1]

        def encode(self):
                return "email=%s&uid=%d&role=%s" % (self.email, self.uid, self.role)

        def dump(self):
                return "{\n\temail: '%s'\n\tuid: %d\n\trole: '%s'\n}" % (self.email, self.uid, self.role)

def profile_for(email_address):
        addr = ""
        for s in email_address.split("&"):
                for t in s.split("="):
                        addr += t

        return Profile(addr, 10, "user")

def setup_oracle():
        global key
        key = common.randbytes(16)

def encryption_oracle(email_address):
        global key
        
        return common.aes_ecb_encrypt(profile_for(email_address).encode(), key)

def decryption_oracle(ct):
        global key
        encoding = common.aes_ecb_decrypt(ct, key)
        P = Profile()
        P.decode(encoding)

        return P.dump()

def main():
        setup_oracle()

        paste_block = encryption_oracle("A" * (16 - len("email=")) + "admin" + '\x0b' * 11)[16:32]
        solution = encryption_oracle("A" * 10 + "B" * 3)

        print decryption_oracle(solution[0:32] + paste_block)

if __name__ == '__main__':
        main()

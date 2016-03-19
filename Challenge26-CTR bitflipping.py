#coding:utf-8
from code import *

key = randbytes(16)
IV = 0

def encryption_oracle(arbitrary_inputPT):
        sanitized = arbitrary_inputPT.replace(";","%%3b").replace("=", "%%3d")
        return aes_ctr_encrypt("comment1=cooking%%20MCs;userdata=%s;comment2=%%20like%%20a%%20pound%%20of%%20bacon"%sanitized, key, IV)

def decryption_oracle(ciphertext):

        try:
                plaintext = aes_ctr_decrypt(ciphertext, key, IV).index(";admin=true;")
        except:
                return False

        return True
                             
if __name__ == '__main__':
    ciphertext = encryption_oracle("A" * 32)
    print ciphertext
    
    
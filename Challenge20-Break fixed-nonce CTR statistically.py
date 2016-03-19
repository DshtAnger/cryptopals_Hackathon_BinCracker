from code import *



def main():        
        minlength = min(map(len, ct_list))
        ctchunks = "".join(map(lambda t: t[0:minlength], ct_list))
        ptchunks = break_repeating_xor_withkeylen(ctchunks, minlength)[0]
        
        for i in range(0, len(ptchunks), minlength):
                print ptchunks[i:i+minlength]



if __name__ == '__main__':
        nonce = 0
        ct_list = []
        key = randbytes(16)
        f = open("20.txt", "r")
        for line in f:
                ct_list.append(aes_ctr_encrypt(b64decode(line.rstrip()), key, nonce))
        #main()

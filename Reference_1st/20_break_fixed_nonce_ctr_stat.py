import common

INPATH = "20.txt"

NONCE = 0
KEY = ""

ct_list = []

def setup():
        global ct_list
        global KEY

        KEY = common.randbytes(16)

        f = open(INPATH, "r")
        for line in f:
                ct_list.append(common.aes_ctr_encrypt(common.b64decode(line.rstrip()), KEY, NONCE))

def main():
        setup()

        minlength = min(map(len, ct_list))
        ctchunks = "".join(map(lambda t: t[0:minlength], ct_list))
        ptchunks = common.break_repeating_xor_withkeylen(ctchunks, minlength)[0]
        for i in range(0, len(ptchunks), minlength):
                print ptchunks[i:i+minlength]

        # we get most of the plaintext; we can't 100% recover *all* of it;
        # this method just gives us enough to work with

if __name__ == '__main__':
        main()

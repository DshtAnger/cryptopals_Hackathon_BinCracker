'''
Matasano Crypto Pals
utility module
Jonathan Eskeldson

Contains stuff that has the potential to be used in multiple challenges.
'''

import base64
import binascii
import operator
import random
import string
import struct

from Crypto.Cipher import AES

class InvalidPaddingError(Exception):
        def __init__(self, msg):
                self.msg = msg
        def __str__(self):
                return repr(self.msg)

# character frequencies of english characters
english_profile = {
        " " :  0.18288462654132653,
        "e" :  0.10266650371711405,
        "t" :  0.07516998273511516,
        "a" :  0.06532167023346977,
        "o" :  0.06159577254159049,
        "n" :  0.05712011128985469,
        "i" :  0.05668443260048856,
        "s" :  0.05317005343812784,
        "r" :  0.04987908553231180,
        "h" :  0.04978563962655234,
        "l" :  0.03317547959533063,
        "d" :  0.03282923097335889,
        "u" :  0.02275795359120720,
        "c" :  0.02233675963832357,
        "m" :  0.02026567834113036,
        "f" :  0.01983067155219636,
        "w" :  0.01703893766467868,
        "g" :  0.01624904409178952,
        "p" :  0.01504324284647170,
        "y" :  0.01427666624127353,
        "b" :  0.01258880743014620,
        "v" :  0.00796116438442061,
        "k" :  0.00560962722644426,
        "x" :  0.00140920161949961,
        "j" :  0.00097521808184139,
        "q" :  0.00083675498119895,
        "z" :  0.00051284690692656
}

def randbytes(n):
        '''
        returns a string of random bytes

        args:
                n:      number of bytes to return
        returns:
                string of n random bytes
        '''

        ret = ""
        for i in range(n):
                ret += chr(random.randint(0, 0xff))

        return ret

def hamming_distance(s1, s2):
        '''
        given two strings of equal length, computes the number of differing 
        bits between them
        args:
                s1: first string
                s2: second string
        returns:
                number of bits that differ between s1 and s2
        '''

        assert len(s1) == len(s2)
        # xor each bit in s1 and s2, count the number of 1's in the result
        return str(bin(int(s1.encode("hex"), 16) ^ int(s2.encode("hex"), 16))).count("1")



def repeat_xor_cipher(key, pt):
        ''' 
        given a key and a plaintext, uses repeating-key XOR to encrypt the
        plaintext with a key.
        args:
                key: key to repeatedly XOR
                pt: plaintext to be encrypted
        returns:
                ciphertext of pt under repeating-key XOR using "key"
        '''
                
        ct = ""
        key_i = 0
        for c in pt:
                ct += chr(ord(c) ^ ord(key[key_i]))
                key_i = (key_i + 1) % len(key)

        return ct


def score_string (s):
        ''' 
        gives a string a "score" for how close it is to english
        args:
                s: string to score
        returns:
                a floating-point measure of how "close" the string is to 
                english, with lower scores being "closer"
        '''
        distr = dict()
        for c in string.lowercase:
                distr[c] = 0.0
        distr[' '] = 0.0

        for c in s:
                if c not in string.printable: 
                        return 999
                if c in string.letters or c == ' ':
                        distr[c.lower()] = distr[c.lower()] + (1.0 / len(s))

        return earth_movers_distance(english_profile, distr)


def break_single_xor(ct):
        ''' 
        given a ciphertext encrypted by XORing with a single byte, decrypts the
        ciphertext and recovers the key.
        args:
                ct: ciphertext to be decrypted
        returns:
                (key, str, dist), where:
                key is the XORed byte to encrypt
                str is the plaintext message
                dist is the earth_movers_distance to the english profile
        '''

        best_score = score_string(ct)
        best_key = 0
        best_str = ct

        for poss_key in range(1, 256):
                poss_str = ""

                for c in ct:
                        poss_str += chr(ord(c) ^ poss_key)

                poss_score = score_string(poss_str)
                if poss_score < best_score:
                        best_score = poss_score
                        best_key = poss_key
                        best_str = poss_str

        return (best_key, best_str, best_score)


def break_repeating_xor_withkeylen(ct, keylen):
        blocks = [""] * keylen
        for i in range(len(ct)):
                blocks[i % keylen] += ct[i]

        key = ""
        for b in blocks:
                key += chr(break_single_xor(b)[0])
        poss_string = repeat_xor_cipher(key, ct)

        return (poss_string, key)


def break_repeating_xor(ct):
        keysize_distances = dict()
        for poss_keysize in range(2, 50):
                dists = []
                # average edit distance over first 5 blocks
                for i in range(0, 5):
                        dists.append(hamming_distance (ct[2*i*poss_keysize:(2*i+1)*poss_keysize], ct[(2*i+1)*poss_keysize:(2*i+2)*poss_keysize]) / float(poss_keysize))
                keysize_distances[poss_keysize] = sum(dists) / float(len(dists))

        best_candidates = sorted(keysize_distances.iteritems(), key=operator.itemgetter(1))[0:5]

        best_score = 9999
        for candidate in best_candidates:
                poss_string, key = break_repeating_xor_withkeylen(ct, candidate[0])
                poss_score = score_string(poss_string)
                if poss_score < best_score:
                        best_score = poss_score
                        best_string = poss_string
                        best_candidate = candidate
                        best_key = key

        return (best_string, best_key)

_b64table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
def b64encode(s):
        assert len(_b64table) == 64

        ret = ""
        for i in range(0, len(s), 3):
                if i + 2 < len(s):
                        chunk = (ord(s[i]) << 16) | (ord(s[i+1]) << 8) | (ord(s[i+2]))
                        ret += _b64table[chunk >> 18] + _b64table[(chunk >> 12) & 0x3f] + _b64table[(chunk >> 6) & 0x3f] + _b64table[chunk & 0x3f]
                elif i + 1 < len(s):
                        chunk = (ord(s[i]) << 16) | (ord(s[i+1]) << 8)
                        ret += _b64table[chunk >> 18] + _b64table[(chunk >> 12) & 0x3f] + _b64table[(chunk >> 6) & 0x3f] + "="
                else:
                        chunk = (ord(s[i]) << 16)
                        ret += _b64table[chunk >> 18] + _b64table[(chunk >> 12) & 0x3f] + "=="

        return ret

def b64decode(s):
        assert len(_b64table) == 64
        assert len(s) % 4 == 0

        ret = ""
        for i in range(0, len(s) - 4, 4):
                chunk = (_b64table.index(s[i]) << 18) | (_b64table.index(s[i+1]) << 12) | (_b64table.index(s[i+2]) << 6) | _b64table.index(s[i+3])
                ret += chr(chunk >> 16) + chr((chunk >> 8) & 0xff) + chr(chunk & 0xff)

        if s[-2:] == "==":
                chunk = (_b64table.index(s[-4]) << 18) | (_b64table.index(s[-3]) << 12)
                ret += chr(chunk >> 16)
        elif s[-1] == "=":
                chunk = (_b64table.index(s[-4]) << 18) | (_b64table.index(s[-3]) << 12) | (_b64table.index(s[-2]) << 6)
                ret += chr(chunk >> 16) + chr((chunk >> 8) & 0xff)
        else:
                chunk = (_b64table.index(s[-4]) << 18) | (_b64table.index(s[-3]) << 12) | (_b64table.index(s[-2]) << 6) | _b64table.index(s[-1])
                ret += chr(chunk >> 16) + chr((chunk >> 8) & 0xff) + chr(chunk & 0xff)

        return ret

def xor_strings(s1, s2):
        '''
        takes two strings and produces the XOR sum of the bytes making them up
        args:
                s1: first string in sum
                s2: second string in sum
        returns:
                string consisting of the XOR sum of each byte in s1 and s2
        '''

        assert len(s1) == len(s2)
        ret = ""
        for i in range(len(s1)):
                ret += chr(ord(s1[i]) ^ ord(s2[i]))

        return ret

def earth_movers_distance (d1, d2):
        '''
        takes two distributions and computes the (approximate) earth mover's 
        distance between them, assuming that they have the (roughly) the same 
        total weight and that their keys are all the same

        args:
                d1: dictionary of first distribution
                d2: dictionary of second distribution
        returns:
                earth mover's distance between two distributions as a float
        '''

        emd = [0]
        
        i = 1
        for key in d1:
                emd.append(emd[i-1] + d1[key] - d2[key])
                i = i + 1

        return sum(map(abs, emd))

def pkcs7_pad(s, padto):
        '''
        takes a string and pads it to the specified length using PKCS#7, which
        pads using the value of the number of bytes to pad to.

        args:
                s:      string to pad
                padto:  length to pad it to
        returns:
                s padded to padto bytes
        '''

        assert (len(s) <= padto) 
        padlen = padto - len(s)
        return s + chr(padlen)*padlen

def aes_encrypt_block(pt, key):
        '''
        encrypts a 16 byte plaintext with a 16 byte key using AES-128 ECB

        args:
                pt:     plaintext to encrypt
                key:    key to encrypt with
        returns:
                ciphertext resulting from encrypting pt with the specified key
        '''
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.encrypt(pt)

def aes_decrypt_block(ct, key):
        '''
        decrypts a 16 byte ciphertext with a 16 byte key using AES-128 ECB

        args:
                ct:     ciphertext to decrypt
                key:    key to decrypt with
        returns:
                plaintext resulting from decrypting ct with the specified key
        '''

        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.decrypt(ct)

def aes_ecb_encrypt(pt, key):
        ''' 
        encrypts an arbitrary length plaintext with a 16 byte key using AES-128 ECB

        args:
                pt:     plaintext to encrypt
                key:    key to encrypt with
        returns:
                ciphertext resulting from encrypting pt with the specified key
        '''

        padpt = pkcs7_pad(pt, len(pt) + (16 - (len(pt) % 16)))
        ct = ""
        for i in range(0, len(padpt), 16):
                ct += aes_encrypt_block(padpt[i:i+16], key)

        return ct

def aes_ecb_decrypt(ct, key):
        ''' 
        decrypts an arbitrary length ciphertext with a 16 byte key using AES-128 ECB

        args:
                ct:     ciphertext to encrypt
                key:    key to decrypt with
        returns:
                plaintext resulting from decrypting ct with the specified key
        '''

        assert(len(ct) % 16 == 0)

        pt = ""
        for i in range(0, len(ct), 16):
                pt += aes_decrypt_block(ct[i:i+16], key)

        return pt

def aes_cbc_encrypt(pt, key, IV):
        '''
        encrypts a ciphertext with a 16 byte KEY using AES-128 CBC

        args:
                pt:     plaintext to encrypt
                key:    key to encrypt with
                IV:     initialization vector
        returns:
                ciphertext resulting from encrypting pt with specified key and IV
        '''

        assert(len(IV) == 16)
        padpt = pkcs7_pad(pt, len(pt) + (16 - (len(pt) % 16)))
        
        prev_ct = IV
        ct = ""
        for i in range(0, len(padpt), 16):
                cur_ct_block = aes_encrypt_block(xor_strings(padpt[i:i+16], prev_ct), key)
                ct += cur_ct_block
                prev_ct = cur_ct_block

        return ct

def aes_cbc_decrypt(ct, key, IV):
        '''
        decrypts a ciphertext with a 16 byte KEY using AES-128 CBC

        args:
                ct:     ciphertext to decrypt
                key:    key to decrypt with
                IV:     initialization vector
        returns:
                plaintext resulting from decrypting ct with specified key and IV
        '''

        assert(len(IV) == 16)
        assert(len(ct) % 16 == 0)
        pt = ""
        prev_block = aes_decrypt_block(ct[-16:], key)
        for i in range(len(ct) - 16, 0, -16):
                cur_ct_block = ct[i-16:i]
                pt = xor_strings(prev_block, cur_ct_block) + pt
                prev_block = aes_decrypt_block(cur_ct_block, key)

        pt = xor_strings(prev_block, IV) + pt
        return pt

def unpad(padpt, blocksize):
        '''
        depads a plaintext padded with PKCS #7 padding scheme
        raises exception on incorrect padding 

        args:
                padpt:          padded plaintext
                blocksize:      blocksize of cipher used
        returns:
                unpadded version of padded plaintext
        exceptions:
                InvalidPaddingError on incorrect padding
        '''

        pad = padpt[-1]
        if ord(pad) > blocksize or ord(pad) == 0:
                raise InvalidPaddingError("padding character too large")

        for i in range(0, ord(pad)):
                if padpt[-i-1] != pad:
                        raise InvalidPaddingError("padding character mismatch")

        return padpt[:-ord(pad)]


def aes_ctr_encrypt(pt, key, nonce):
        '''
        encrypts a plaintext using AES CTR mode

        args:
                pt:     plaintext
                key:    key to encrypt pt under
                nonce:  nonce to encrypt pt under

        returns:
                ciphertext resulting from encrypting plaintext
        '''
                
        ctr = 0
        ct = ""
        for i in range(0, len(pt), 16):
                # little endian ctr string
                keystream_input = struct.pack("<QQ", nonce, ctr)
                keystream = aes_encrypt_block(keystream_input, key)
                ct += xor_strings(keystream[:len(pt[i:i+16])], pt[i:i+16])
                ctr = (ctr + 1) % (2 ** 64)

        return ct
                

def aes_ctr_decrypt(ct, key, nonce):
        '''
        decrypts a plaintext using AES CTR mode

        due to the nature of CTR mode, this is essentially a wrapper for
        the encryption routine, but named decryption for developer convenience

        args:
                ct:     ciphertext
                key:    key to decrypt ct under
                nonce:  nonce to decrypt ct under

        returns:
                plaintext resulting from decrypting ciphertext
        '''
        return aes_ctr_encrypt(ct, key, nonce)

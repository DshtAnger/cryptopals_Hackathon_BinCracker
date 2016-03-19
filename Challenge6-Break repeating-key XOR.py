from code import *
import sys
import operator
import string

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
def getbin(char):
	'get the bin value of a single character'
	return bin(ord(char)).lstrip('0b')

def HamDist(srting1,string2):
	'compute the Hamming distance between two strings'
	count=0
	for (x,y) in zip(srting1,string2):
		s1 = getbin(x)
		s2 = getbin(y)
		if len(s1) < len(s2):
				s1 = '0'*(len(s2)-len(s1))+s1
		else:
				s2 = '0'*(len(s1)-len(s2))+s2
		
		for (a,b) in zip(s1,s2):
			if a!=b:
				count+=1
	return count


def avg_hamming_dist(raw, block_size):
    blocks = get_chunks(raw, block_size)
    return sum(HamDist(c1, c2) / block_size for c1, c2 in zip(blocks, blocks[1:])) / len(blocks[1:])

def get_chunks(raw, chunk_size):
    return [raw[i:i+chunk_size] for i in range(0, len(raw), chunk_size)]

test1 = 'this is a test'
test2 = 'wokka wokka!!!'

'----------------------------------------------------------------------------'

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

def break_repeating_xor_withkeylen(ct, keylen):
        blocks = [""] * keylen
        for i in range(len(ct)):
                blocks[i % keylen] += ct[i]

        key = ""
        for b in blocks:
                key += chr(break_single_xor(b)[0])
        poss_string = repeat_xor_cipher(key, ct)

        return (poss_string, key)

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
def break_repeating_xor(ct):
        keysize_distances = dict()
        for poss_keysize in range(2, 50):
                dists = []
                # average edit distance over first 5 blocks
                for i in range(0, 5):
                        dists.append(HamDist (ct[2*i*poss_keysize:(2*i+1)*poss_keysize], ct[(2*i+1)*poss_keysize:(2*i+2)*poss_keysize]) / float(poss_keysize))
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
def main():
        if len(sys.argv) < 2:
                f = open (SAMPLE_FILENAME, "r")
        else:
                f = open (sys.argv[1], "r")

        ct = ""
        for line in f:
                ct += line.rstrip()

        ct = b64decode(ct)

        assert HamDist("this is a test", "wokka wokka!!!") == 37

        pt, key = break_repeating_xor(ct)
        print pt
        print key



if __name__ == '__main__':
	SAMPLE_FILENAME = "Challenge6.txt"
	main()


		

	

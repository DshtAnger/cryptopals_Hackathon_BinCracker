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
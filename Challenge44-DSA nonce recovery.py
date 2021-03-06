
p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291

y = 0x2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821

s1 = 1267396447369736888040262262183731677867615804316
r1 = 1105520928110492191417703162650245113664610474875
m1 = 0xa4db3de27e2db3e5ef085ced2bced91b82e0df19

s2 = 559339368782867010304266546527989050544914568162
r2 = 826843595826780327326695197394862356805575316699
m2 = 0x88b9e184393408b133efef59fcef85576d69e249

def egcd(a, b):
    if b == 0:
        return (1, 0)
    else:
        q = a // b
        r = a % b
        (s, t) = egcd(b, r)
        return (t, s - q * t)

# Returns a^-1 mod N
def invmod(a, N):
    
    (x, y) = egcd(a, N)
    return x % N

def recover_dsa_k(hash1, hash2, r1, s1, r2, s2, q=q):
	'''
	       (m1 - m2)
	   k = --------- mod q
	       (s1 - s2)
	'''

	top = (hash1 - hash2) % q
	k = top * invmod((s1 - s2)%q, q)
	return k

def get_dsa_key_from_known_k(r, s, k, msg_hash, q=q):
	'''
	x is private key
	      (s * k) - H(msg)
	  x = ----------------  mod q
	              r
	'''
	top = ((s*k) - msg_hash) % q
	x = top * invmod(r, q)
	return x

if __name__ == "__main__":
    k = recover_dsa_k(m1, m2, r1, s1, r2, s2)
    x1 = get_dsa_key_from_known_k(r1, s1, k, m1)
    x2 = get_dsa_key_from_known_k(r1, s1, k, m1)
    assert(x1 == x2)
    print("x = ", x1)
    print("problem 44 success")
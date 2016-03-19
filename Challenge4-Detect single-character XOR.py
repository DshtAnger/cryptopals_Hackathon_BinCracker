
def FindSingleCharXOR(SpaceNum):
	for char in xrange(10,127):
		result = ''.join([chr(char^ord(byte)) for byte in ciphertext])
		SpaceCount=0
		for each in result:
			if each == ' ':
				SpaceCount+=1
		if SpaceCount>=SpaceNum:
			print "char =",chr(char)
			print "The message is :",result

if __name__ == '__main__':
	f = open('Challenge4.txt','r').readlines()
	for EachMeg in f:
		ciphertext = EachMeg.rstrip('\n').decode('hex')
		FindSingleCharXOR(5)
	

	

#coding:utf-8
from code import *

UnknownPt="Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
key = randbytes(16)

def encryption_oracle(plaintext):
        global key
        return aes_ecb_encrypt(randbytes(random.randint(2, 50))+plaintext+base64.b64decode(UnknownPt),key)

def find_blocksize():
    size_list = []
    for _ in range(100):
        size_list.append(len(encryption_oracle("A")))
    size_list.sort()

    
    if size_list[0] == size_list[-1]:
        trial_string = "A"
        prev_length = len(encryption_oracle("A"))
        new_length = prev_length
        while (new_length == prev_length):
                trial_string += "A"
                new_length = len(encryption_oracle(trial_string))
        blocksize = new_length - prev_length  

    
    else:
        for i in range(1, len(size_list)):
            if size_list[i] != size_list[i-1]:
                blocksize = size_list[i] - size_list[i-1]
                break

    return blocksize

def detect_useECB(blocksize=find_blocksize()):
    test_ecb = encryption_oracle("A" * 3*blocksize)
    found = False

    for i in range(0, len(test_ecb) - blocksize, blocksize):
        if test_ecb[i:i+blocksize] == test_ecb[i+blocksize:i+2*blocksize]:
            print "Using ECB : True!"
            found = True
            break
    if not found:
        print "Using ECB : Flase!"
        
    return found


def find_unknowPT_length():
    times=1
    compare=[]
    result=0
    while True:
        try_length=[]
        for _ in range(1000):
            try_length.append(str(len(encryption_oracle('A'*times))))

        try_length.sort()
        compare.append(try_length[-1])

        if len(compare)>1:
            for i in range(1,len(compare)):
                if compare[i] != compare[i-1]:
                    result = int(compare[i-1]) - 50 - (times-1)
                    break
        times+=1
        if result!=0:
            return result

def get_longest_block(trial):
    times=1
    records=[]
    for _ in range(10000):
        records.append(encryption_oracle(trial*times))
    records_length = map(len, records)
    index=records_length.index(max(records_length))
    longest_block=records[index]

    return longest_block


def break_ecb():
    blocksize = find_blocksize()
    print "blocksize = %d" % (blocksize)
    assert(detect_useECB())
    unknown_pt_length = find_unknowPT_length()
    print "unknown_pt_length : %d"%unknown_pt_length


    bytes_recovered = ""
    for trial_len in xrange(blocksize-1,-1,-1):
        trial = 'A'*14 + "A"*trial_len
        
        longest_block = get_longest_block(trial)
        target = longest_block[blocksize*4:blocksize*5]


        
        for char in xrange(10,126):
            test = get_longest_block(trial+bytes_recovered+chr(char))
            if test[blocksize*4:blocksize*5] == target[blocksize*4:blocksize*5]:
                bytes_recovered+=chr(char)                
                print bytes_recovered 
                break
    print "--------------------------------------------------"






'''
if __name__ == '__main__':
    break_ecb()
'''
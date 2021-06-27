#!/usr/bin/env python
#

from hashlib import sha256
import time


MAX_NONCE = 10_000_000        # You can also use a while loop to run infinitely with no upper limit


def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

def mine(block_number,transaction,previous_hash,prefix_zeros):
    prefix_str='0'*prefix_zeros
    hash_count = 0
    hash_result = None
    for nonce in range(MAX_NONCE):
        text= str(block_number) + transaction + previous_hash + str(nonce)
        hash = SHA256(text)
        hash_count += 1
        # print(hash)
        if hash.startswith(prefix_str):
            print("Bitcoin mined with nonce value : ", nonce)
            hash_result = nonce
            break
    if hash_result is None:
        print("Could not find a hash in the given range of upto", MAX_NONCE)
    else:
        print("Found a hash in the given range of upto", MAX_NONCE,
              " explored %.3f" % (float(hash_count)/float(MAX_NONCE)))
    return hash_result, hash_count


transactions='''
A->B->10
B->c->5
'''

difficulty = 6
t_begin=time.time()
new_hash = mine(684260,
                transactions,
                "000000000000000000006bd3d6ef94d8a01de84e171d3553534783b128f06aad",
                difficulty)
print("Hash value : ",new_hash[0])
time_taken=time.time()- t_begin
print("The mining process took ", "%.3f" % time_taken, "seconds",
      " at a hash rate ", "%.3f M" % ( float(new_hash[1]) / time_taken / 1000_000.0),
      " diffuculty level ", difficulty)

'''
Bitcoin mined with nonce value :  36674
Found a hash in the given range of upto 10000000  explored 0.004
Hash value :  36674
The mining process took  0.214 seconds  at a hash rate  0.172 M  diffuculty level  4

Bitcoin mined with nonce value :  2387325
Found a hash in the given range of upto 10000000  explored 0.239
Hash value :  2387325
The mining process took  10.086 seconds  at a hash rate  0.237 M  diffuculty level  5

'''


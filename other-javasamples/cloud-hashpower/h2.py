#!/usr/bin/env python
#  http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html
#  miner.py

import hashlib, struct
import codecs

# hashed header fields
#       version 02000000
#       previous block hash (reversed) 17975b...0000
#       merkle root (reversed) 8a9729...1787
#       timestamp 358b0553
#       bits 535f0119
#       nonce 48750833
# other fields
#       transaction count 62
#       coinbase transaction
#       transaction
#       ...

ver = 2
prev_block = "000000000000000117c80378b8da0e33559b5997f2ad55e2f7d18ec1975b9717"
mrkl_root = "871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a"
time_ = 0x53058b35  # 2014-02-20 04:57:25
bits = 0x19015f53

# https://en.bitcoin.it/wiki/Difficulty
exp = bits >> 24
mant = bits & 0xffffff
target_hexstr = '%064x' % (mant * (1 << (8 * (exp - 3))))
#target_str = target_hexstr.decode('hex')
target_str = bytes.fromhex(target_hexstr)

nonce = 0
nonce = 856190328 #the result is 856192328
while nonce < 0x100000000:
    #header = (struct.pack("<L", ver) + prev_block.decode('hex')[::-1] +
    #          mrkl_root.decode('hex')[::-1] + struct.pack("<LLL", time_, bits, nonce))
    header = (struct.pack("<L", ver) + bytes.fromhex(prev_block)[::-1] +
              bytes.fromhex(mrkl_root)[::-1] + struct.pack("<LLL", time_, bits, nonce))
    hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
    encode_hex = codecs.getencoder("hex_codec")
    print(nonce, encode_hex(hash[::-1]))    #nonce, hash[::-1].encode('hex')
    if hash[::-1] < target_str:
        print('success')
        break
    nonce += 1


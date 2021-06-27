#!/usr/bin/env python
# http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html
# stratum.py

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("us1.ghash.io", 3333))

sock.send("""{"id": 1, "method": "mining.subscribe", "params": []}\n""")
print(sock.recv(4000))

sock.send("""{"params": ["kens_1", "password"], "id": 2, "method": "mining.authorize"}\n""")
print(sock.recv(4000))


'''  in the third message params: job_id=58af8d8c, prevhash=975b97..., coinb1=010000...,
                                   coinb2=2e52...,
                                   merkle_branch=["ea9d... ,
                                   version=00000002, nbits=19015f53, ntime=53058b41, clean_jobs=false
{"id":1,"result":[ [ ["mining.set_difficulty","b4b6693b72a50c7116db18d6497cac52"],
                     ["mining.notify","ae6812eb4cd7735a302a8a9dd95cf71f"]
                   ],"4bc6af58",4],"error":null}

{"id":null,"params":[16],"method":"mining.set_difficulty"}

{"id":null,"params":["58af8d8c",
                     "975b9717f7d18ec1f2ad55e2559b5997b8da0e3317c803780000000100000000",
                     "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4803636004062f503253482f04428b055308",
                     "2e522cfabe6d6da0bd01f57abe963d25879583eea5ea6f08f83e3327eba9806b14119718cbb1cf04000000000000000000000001fb673495000000001976a91480ad90d403581fa3bf46086a91b2d9d4125db6c188ac00000000",
                     ["ea9da84d55ebf07f47def6b9b35ab30fc18b6e980fc618f262724388f2e9c591",
                      "f8578e6b5900de614aabe563c9622a8f514e11d368caa78890ac2ed615a2300c",
                      "1632f2b53febb0a999784c4feb1655144793c4e662226aff64b71c6837430791",
                      "ad4328979dba3e30f11c2d94445731f461a25842523fcbfa53cd42b585e63fcd",
                      "a904a9a41d1c8f9e860ba2b07ba13187b41aa7246f341489a730c6dc6fb42701",
                      "dd7e026ac1fff0feac6bed6872b6964f5ea00bd8913a956e6b2eb7e22363dc5c",
                      "2c3b18d8edff29c013394c28888c6b50ed8733760a3d4d9082c3f1f5a43afa64"],
                     "00000002","19015f53","53058b41",false],"method":"mining.notify"
{"id":2,"result":true,"error":null}
{"id":null,"params":[16],"method":"mining.set_difficulty"}
'''


#!/bin/bash

# you shouldn't need to change these
PYTHONVER="Python-2.7.3"

set -e 

mkdir lib
mkdir lib/encodings
mkdir lib/json

for fn in  _abcoll.py tempfile.py platform.py linecache.py posixpath.py socket.py  \
           keyword.py traceback.py sysconfig.py UserDict.py bisect.py sre_parse.py \
           subprocess.py codecs.py struct.py types.py pickle.py re.py hashlib.py   \
           random.py string.py warnings.py getopt.py os.py base64.py abc.py \
           textwrap.py collections.py __future__.py genericpath.py stat.py   \
           _weakrefset.py mimetools.py copy_reg.py urlparse.py heapq.py      \
           functools.py sre_compile.py httplib.py rfc822.py sre_constants.py \
           ssl.py urllib.py site.py ; do
  cp $PYTHONVER/Lib/$fn  lib/
done


for fn in  json/encoder.py json/__init__.py json/scanner.py json/decoder.py ; do 
  cp $PYTHONVER/Lib/$fn  lib/json/
done


for fn in  encodings/aliases.py encodings/__init__.py encodings/hex_codec.py  \
           encodings/ascii.py encodings/cp1252.py encodings/cp437.py         \
           encodings/latin_1.py encodings/mbcs.py encodings/utf_8.py  ; do
  cp $PYTHONVER/Lib/$fn  lib/json/
done



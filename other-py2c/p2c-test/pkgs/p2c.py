#!/usr/bin/env python
# p2c.py
#   derived from the blog at 
#   http://blog.biicode.com/bii-internals-compiling-your-python-application-with-cython/

import bii_cfg

import bii_cythonize
cffs = bii_cythonize.bii_cythonize(True, 
	bii_cfg.included_dirs, bii_cfg.biicode_python_path, 
	bii_cfg.src_dir, bii_cfg.ignored_files)
print "cffs", cffs

import bii_optimize
mods = bii_optimize.bii_optimize(cffs, bii_cfg.src_dir)
print "mods", mods

from distutils.extension import Extension
from distutils.core import setup
 
VERSION="1.2.3.4"
setup(
       name="bii",
       version=VERSION,
       script_name='setup.py',
       script_args=['build_ext'],
       packages=['biicode'],
       ext_modules=mods,
       )


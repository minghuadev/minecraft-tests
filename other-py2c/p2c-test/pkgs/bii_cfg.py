#!/usr/bin/env python
# bii_cfg.py

import os

biicode_pkg_path = os.path.abspath("../srcs/srcs/testsrc")
biicode_python_path = os.path.dirname(biicode_pkg_path)

build_dir = os.path.abspath("../release")
src_dir = os.path.abspath(os.path.join(build_dir, 'src'))
if not os.path.exists(src_dir):
   print " make src_dir ", src_dir
   os.makedirs(src_dir)

ignored_files = ['__init__.py']
included_dirs = [os.path.join(biicode_pkg_path, dir_) for dir_ in ['client', 'common']]

print " included_dirs ", included_dirs



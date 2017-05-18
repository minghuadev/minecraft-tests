#!/usr/bin/env python
# bii_cythonize.py

import os

from Cython.Build import cythonize
def bii_cythonize(force_compile, included_dirs, 
		biicode_python_path, src_dir, ignored_files):
   '''
   Creates c files from your source python
   Params:
       force_compile: boolean, if true compiles regardeless 
                      of whether the file has changed or not
   Returns:
       list of c files relative to biicode_pkg_path
   '''
 
   c_files = []
   for dir_ in included_dirs:
       for dirname, dirnames, filenames in os.walk(dir_):
           if 'test' in dirnames:
               dirnames.remove('test')
 
           for filename in filenames:
               file_ = os.path.join(dirname, filename)
               stripped_name = os.path.relpath(file_, biicode_python_path)
               file_name, extension = os.path.splitext(stripped_name)
               target_tmpf, tmp2 = os.path.splitext(file_)
               target_tmpf += '.c'
 
               if extension == '.py':
                   target_file = os.path.join(src_dir, file_name + '.c')
                   if filename not in ignored_files:
                       c_files.append(stripped_name.replace('.py', '.c'))
                       file_dir = os.path.dirname(target_file)
                       if not os.path.exists(file_dir):
                           os.makedirs(file_dir)
 
                       extension = cythonize(file_, ##stripped_name,
                                             force=force_compile, 
                                             build_dir=src_dir)
                       print extension, extension
                       os.rename(target_tmpf, target_file)
   return c_files


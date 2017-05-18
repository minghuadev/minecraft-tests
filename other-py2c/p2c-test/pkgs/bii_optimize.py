#!/usr/bin/env python

import os
import platform
from distutils.extension import Extension
from distutils import sysconfig
 
def bii_optimize(orig_c_files, src_dir):
   abs_path_c_files = [os.path.join(src_dir, c) for c in orig_c_files]
   modules = []
   for c_file in abs_path_c_files:
       relfile = os.path.relpath(c_file, src_dir)
       filename = os.path.splitext(relfile)[0]
       extName = filename.replace(os.path.sep, ".")
       extension = Extension(extName,
                             sources=[c_file],
                             define_macros=[('PYREX_WITHOUT_ASSERTIONS',
                                             None)]  # ignore asserts in code
                             )
       modules.append(extension)
 
   if platform.system() != 'Windows':
       cflags = sysconfig.get_config_var('CFLAGS')
       opt = sysconfig.get_config_var('OPT')
       sysconfig._config_vars['CFLAGS'] = cflags.replace(' -g ', ' ')
       sysconfig._config_vars['OPT'] = opt.replace(' -g ', ' ')
 
   if platform.system() == 'Linux':
       ldshared = sysconfig.get_config_var('LDSHARED')
       sysconfig._config_vars['LDSHARED'] = ldshared.replace(' -g ', ' ')
 
   elif platform.system() == 'Darwin':
       #-mno-fused-madd is a deprecated flag that now causes a hard error
       # but distuitls still keeps it
       # it was used to disable the generation of the fused multiply/add instruction
       for flag, flags_line in sysconfig._config_vars.iteritems():
           if ' -g' in str(flags_line):
               sysconfig._config_vars[flag] = flags_line.replace(' -g', '')
       for key in ['CONFIG_ARGS', 'LIBTOOL', 'PY_CFLAGS', 'CFLAGS']:
           value = sysconfig.get_config_var(key)
           if value:
               sysconfig._config_vars[key] = value.replace('-mno-fused-madd', '')
               sysconfig._config_vars[key] = value.replace('-DENABLE_DTRACE',  '')
   return modules


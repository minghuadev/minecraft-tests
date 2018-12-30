#!/bin/bash
# ccc.bash

set -ex

mb-gcc  -O0 -c -o start.o start.S
mb-gcc  -O0 -c -o test.o  test.c

mb-ld -Tlinker.lds start.o test.o -o foo.elf
mb-objcopy -S -I elf32-big foo.elf -O binary bar.bin

mb-objcopy -O srec foo.elf foo.srec
srec2vram 4 foo.srec 0 8192 > rom.vmem



/*
 * linker.lds
 *  see https://sourceware.org/binutils/docs/ld/Scripts.html
 */

SECTIONS
{
  . = 0x0;
  .text : { *(.text) }
  . = 0x400;
  .data : { *(.data) }
  .bss : { *(.bss) }
}



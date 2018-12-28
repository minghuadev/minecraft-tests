/*
 * start.S
 *   copied partly from github.com/Xilinx/u-boot-xlnx/blob/master/arch/microblaze/cpu/start.S
 */

#define CONFIG_SYS_INIT_SP_OFFSET 0x800

	.text
	.global _start
_start:
	/*
	 * reserve registers:
	 * r10: Stores little/big endian offset for vectors
	 * r2: Stores imm opcode
	 * r3: Stores brai opcode
	 */

	/*mts	rmsr, r0	/* disable cache */

	/*addi	r8, r0, __end
	mts	rslr, r8
	*/

	/* TODO: Redo this code to call board_init_f_*() */
	addi	r1, r0, CONFIG_SYS_INIT_SP_OFFSET
	mts	rshr, r1
	addi	r1, r1, -4	/* Decrement SP to top of memory */

	/* add opcode instruction for 32bit jump - 2 instruction imm & brai */
	addi	r2, r0, 0xb0000000	/* hex b000 opcode imm */
	addi	r3, r0, 0xb8080000	/* hew b808 opcode brai */

	bralid	r15, main
	or	r0, r0, r0
	or	r0, r0, r0

1:	bri	1b
	or	r0, r0, r0
	or	r0, r0, r0



.section .text.init
.global _start
_start:
li sp,0x00008000
la t0, __bss_start
la t1, __bss_end
bge t0, t1, done_bss
bss_loop:
sw zero, 0(t0)
addi t0, t0, 4
blt t0, t1, bss_loop
done_bss:
call main
hang:
j hang
ENTRY(_start)

MEMORY {
    FLASH (rx)  : ORIGIN = 0x00000000, LENGTH = 32K
    RAM   (rwx) : ORIGIN = 0x00000000, LENGTH = 32K
}

SECTIONS {
    .text : { *(.text.init) *(.text) *(.rodata) } > FLASH
    .data : { *(.data) } > RAM
    .bss : {
        __bss_start = .;
        *(.bss)
        __bss_end = .;
    } > RAM
}
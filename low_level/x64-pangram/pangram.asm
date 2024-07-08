section .text
global pangram
pangram:
    xor ecx, ecx ; Set bitset value to '0'
.loop:
    movzx edx, byte [rdi] ; Load 1 byte from string
    cmp edx, 0 ; Compare loaded byte to 0
    je .end ; Jump to the end if byte is '0'
    add rdi, 1 ; Increment string to go to the next byte
    cmp edx, '@' ; Check if this byte is less then ASCII '@' - not a letter
    jl .loop ; If it's not ASCII letter - jump to next
    bts ecx, edx ; Set bit in bitset
    jmp .loop
.end:
    xor eax, eax ; Set result register to '0'
    cmp ecx, 0x07fffffe ; Compare result register with mask
    sete al ; Set lower byte of eax to '1' if bitset is equal to mask
    ret
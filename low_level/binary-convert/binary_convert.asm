section .text
global binary_convert
binary_convert:
    mov eax, 0; Init counter as 0
.loop:
    movzx esi, byte [rdi] ; Load one byte from 1-st argument register
    cmp esi, 0; If ASCII byte ptr is '0' - return
    je .end
    shl eax, 1 ; shift counter left
    and esi, 1 ; Get last bit of fetched byte (because we can have only '30' or '31' in ASCII here)
    or eax, esi ; If it's '1' - put '1' to eax, else - put '0'
    add rdi, 1 ; Move ASCII string ptr
    jmp .loop ; Loop
.end
    ret
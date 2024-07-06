section .text
global sum_to_n

sum_to_n:
    mov rsi, 0 ; init counter register with 0
    mov rax, 0 ; init result register with 0
    call sum ; call function
	ret

sum:
    add rax, rsi ; add value of counter to result register
    inc rsi ; increment counter
    cmp rsi, rdi ; compare if counter is < argument
    jle sum ; make recursive call if counter < argument
    ret ; return from function if counter equal to argument
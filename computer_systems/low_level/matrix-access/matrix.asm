section .text
global index
	; rdi: matrix
	; esi: rows
	; edx: cols
	; ecx: rindex
	; r8d: cindex
index:
    imul ecx, edx       ; Multiply row index by number of columns (w_row * t_cols)
    add ecx, r8d        ; Add column index ((w_row * t_cols) + w_col)
    imul ecx, 4          ; Multiply by 4 (size of int)
    mov eax, [rdi + rcx] ; Load the value at the calculated address
    ret

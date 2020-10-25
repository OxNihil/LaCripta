[bits 16]
[org 0x7c00]

jmp 0:init

init:
	xor bx,bx ; Poner a 0 - variable contador
    	mov di,bx ; seteo a 0 - almacena string
	mov cx,bx ; seteo a 0 
	mov di,STR1 ;Copiamos string
	count_loop:
		mov cx,[di]	
		cmp cx,0x0
		je end		
		inc bx
		jmp count_loop

STR1: db "Hola",0

end: 
	xor ax,ax
	mov ax,bx
	call print
	jmp $


%include "print.asm"

VGA: dd 0xb8000

times 510-($-$$) db 0
dw 0xaa55



[bits 16]
[org 0x7c00]

jmp 0:init

init:
	xor bx,bx ; Ponerlos a 0
    	mov si,bx
	mov cx,bx
	
	mov di,STR1 ;Parametro 1
	mov si,STR2 ;Parametro 2
	mov cx, 4 
	l1: 
		inc di ; mira el final del buffer desrino
		test ds,[di]
		jnz l1
	copy_loop:
		mov al,[si] ; Contenido que apunta STR1
		inc si
		mov [di],al
		inc di
		test al,al ; comparamos si registro
		jz end
		jmp copy_loop


STR1: db "Hola",0
STR2: db "String",0

times 510-($-$$) db 0
dw 0xaaa55

end: 
	jmp $

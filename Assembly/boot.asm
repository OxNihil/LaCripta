;Bootloader 16 bits

[bits 16] ;indica bits con los que trabaja 
[org 0x7c00] ; Direccion Inicial

mov [DISK],dl ; copiamos el contenido del disco inicial - la bios guarda en dl la direccion del primer disco

mov sp,0x9000; establecemos el stack despues de la 9000
mov bp,sp

call load
mov bx, STRING
call bucle
jmp $


bucle: ; print string 
mov ah, 0xe0; negro sobre blanco
mov al, [bx] ;string a pasar [] contenido de
cmp al,0
je end
add bx,0x1
int 0x10

jmp bucle

load:
	xor ax,ax ;xor consigo mismo da 0 	
	mov es, ax ;no deja cargar segmento desde valores inmediatos sino desde un registro
	mov ah,0x2 ;read
	mov al,0x1 ;numero sectores a cargar
	mov cl,0x2 ;a partir de que sector
	mov ch 0x0 
	;cilindro
	mov dl,[DISK] ;disco
	mov dh 0x1 
	;cabezal
	mov bx,0x8000
	int 0x13
	jc error
error:
	mov bx,MSG ;imprime el msg si hay un error
	jmp bucle
end:
    jmp $ ; Salta siempre a posicion actual (halt)

MSG: db "Holaaaaa",0 ;el 0 es el null byte caracter terminador
DISK: dw 0


times 510-($-$$) db 0 ;db define bits (como poner char 1)-> rellenamelo con 0 hasta la pos 510 $(posicion actual)  $$(Posicion primera etiqueta)
		      ;dd define double -> 2 palabras

dw 0xaa55 ;define word
;PRIMER SECTOR 512 BYTES

STRING: db "Estoy en el 2do sector",0

;jmp 0:init el procesador actualiza CS con esto -> CS vale 0

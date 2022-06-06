bits 16 ;Indicamos que se usara un codigo de 16 bits al ensamblar
org 0x7C00 ; Direccion inicial del programa

;Necesario para funcionar en hardware real, poner a cero los segmentos de datos
xor ax, ax ; ax = 0
mov ds, ax ; ds = ax (0)
mov es, ax ; es = ax (0)
jmp setup_game


;;CONSTANTES
VIDEOMEM equ 0B800h ; Color text mode VGA memory location
ROWLEN equ 160 ; 80 character row x 2 bytes cada fila
PLAYERX equ 4  ; Player posicion eje X
CPUX equ 154 ; CPU posicion eje X
SCREENW equ 80 ;Ancho de la pantalla
SCREENH equ 24 ;Alto de la pantalla
PADDLEHEIGHT equ 5 ;Altura de las paletas
KEY_W equ 11h ; Keyboard Scancodes...
KEY_S equ 1Fh
KEY_R equ 13h
KEY_C equ 2Eh
PLAYERBALLSTARTX equ 66 ; Posicion inicial eje X pelota para jugador
CPUBALLSTARTX equ 90 ; Posicion inical eje X pelota para CPU
BALLSTARTY equ 7 ; Posicion inicial eje Y pelota
WINSCORE equ 3 ; Puntos necesarios para ganar


;;VARIABLES
playerY: dw 10 ; Posicion Y del jugador
cpuY: dw 10 ; Posicion Y de la CPU
ballX: dw 66 ; Posicion X de la pelota
ballY: dw 7 ; Posicion Y de la pelota
ballVelX: db -2 ; Velocidad eje X de la pelota
ballVelY: db 1 ; Velocidad eje Y de la pelota
drawColor: db 0F0h ;Color de los elementos
playerScore: db 0 ;Puntuancion Jugador
cpuScore: db 0 ;Puntuacion CPU


setup_game:
    mov si,string ; string = puntero del string
    call setup_video_mode ; Setea AL 03h -> modo texto 80x25 chars, 16 colores VGA
    call hide_cursor ; Oculta el cursor
    call setup_video_memory ; Setea la memoria de video
    call print_string ; Muestra el texto inicial
    call sleeps ;Espera unos segundos
    jmp game_loop ; Carga el juego principal


game_loop:
    ;Limpia la pantalla en negro cada ciclo
    xor ax, ax
    xor di, di
    mov cx, 80*25
    rep stosw
    
    ;Dibuja la linea del medio
    mov ah, [drawColor] ; fondo negro y blanco el primer plano
    mov di, 78 ; Empieza a crear la linea en el medio de una fila de 80 caracteres
    mov cl, 13 ; Bucle para dibujar la linea discontinua
    .draw_line_loop:
        stosw 
        add di, 2*ROWLEN-2 ;Dibujamos cada 2 filas (80 chars * 2 bytes * 2 rows ) - extra offset
        loop .draw_line_loop ;Lo ejecuta CX veces
    
    ;Dibujamos la pala del jugador y del CPU
    imul di, [playerY], ROWLEN ;La posicion Y es, las filas de Y * longitud fila
    imul bx, [cpuY], ROWLEN
    mov cl, PADDLEHEIGHT
    .draw_paddle_loop:
        mov [es:di+PLAYERX], ax
        mov [es:bx+CPUX], ax
        add di, ROWLEN
        add bx, ROWLEN
        loop .draw_paddle_loop
        

    ;Obtenemos el input del usuario
    get_player_input:
        mov ah, 01h ; Lectura de caracteres por te lado
        int 16h ; interrupcion del teclado
        jz move_cpu ;si no hay interrupcion,no checkeamos, pasamos a la cpu
    
        cbw ; Convierte byte a word
        int 16h ;interrupcion del teclado
    
        cmp ah, KEY_W ; si se pulsa W
        je w_pressed
        cmp ah, KEY_S ; si se pulsa S
        je s_pressed
        cmp ah, KEY_C ; si se pulsa C
        je c_pressed 
        cmp ah, KEY_R ; si se pulsa R
        je r_pressed
        jmp move_cpu
    
    ;acciones al pulsar teclas
    w_pressed:
        ;mueve hacia arriba
        dec word [playerY] ; mueve 1 fila mas arriba
        jge move_cpu ; si la posicion del jugador Y es 0, o el valor minimo, salta. 
        inc word [playerY] ;sino incrementamos en una unidad
        jmp move_cpu ;  pasamos a comprobar la cpu
    
    s_pressed:
        cmp word [playerY], SCREENH - PADDLEHEIGHT ;Si el jugador esta ya abajo del todo
        jg move_cpu  
        inc word [playerY] ; si no lo esta, movemos una fila abajo
        jmp move_cpu
        
    c_pressed:
        add byte [drawColor], 10h ; Mueve al siguiente color VGA
        jmp move_cpu
        
    r_pressed:
        int 19h ; Recarga el sector de arranque (Qemu)
    
    move_cpu:
        mov bx, [cpuY]
	cmp bx, [ballY]		; Esta la parte superior de la paleta por encima de la pelota?
	jl move_cpu_down	; si, movemos hacia abajo
	dec word [cpuY]		; No, movemos hacia arriba 
	jge move_ball		; CPU en o por encima de Y mínimo (0), movemos
	inc word [cpuY]		; Si la CPU toca la parte superior del area, retrocede para corregir
	jmp move_ball
	
    move_cpu_down:
        add bx, PADDLEHEIGHT-1  
	cmp bx, [ballY]		; Esta la parte inferior de la paleta de la CPU en o debajo pelota?
	jg move_ball		; si, movemos la pelota
	cmp bx, SCREENH		; No, Está la parte inferior de la paleta CPU en la parte inferior de la pantalla?
	je move_ball		; si, continuamos
	inc word [cpuY]		; No, movemos CPU una fila abajo 
	
    move_ball:
        ;Dibuja la pelota
        imul di, [ballY], ROWLEN
        add di, [ballX]
        mov word [es:di], 2020h ; Green bg, black fg
        
        ;Cambios en la posicion
        mov bl, [ballVelX] 
	add [ballX], bl	 ; Cambios en eje X
	mov bl, [ballVelY]
	add [ballY], bl  ; Cambios en eje Y
	
    check_hit_top:
	cmp word [ballY],0 ;Comparamos si la posicion Y de la pelota esta arriba del todo (0)
	jg check_hit_bottom ;Si no lo esta, revisamos si esta toca abajo 
	neg byte [ballVelY] ;revertimos la direccion de Y
	jmp end_collision_checks

   check_hit_bottom:
	cmp word [ballY],SCREENH ;Comprobamos si la posicion Y de la pelota esta abajo del todo (24)
	jl check_hit_player ; si no lo esta, comprobamos si toca al jugador
	neg byte [ballVelY]  ; revertimos la direccion de Y 
	jmp end_collision_checks
	
    check_hit_player:
        cmp word [ballX], PLAYERX+2 ; Esta la pelota en la misma posicion que la paleta del jugador?		
	jne check_hit_cpu ; No, comprobamos si toca paleta de CPU
	mov bx, [playerY] 
	cmp bx, [ballY]	; ¿Esta la parte superior de la paleta del jugador igual o por encima de la pelota?
	jg check_hit_cpu ; No, comprobamos si toca la paleta de la CPU			
	add bx, PADDLEHEIGHT ; Comprobamos si toca la parte inferior de la paleta del jugador	 		
	cmp bx, [ballY]		
	jl check_hit_cpu ; Comprobamos si toca la paleta de la CPU
	neg byte [ballVelX] ;En otro caso la toca por lo que revertimos la direccion de X	
    
    check_hit_cpu:
        cmp word [ballX], CPUX-2  ; Esta la pelota en la misma posicion que la paleta de la CPU?
	jne check_hit_left ; Si no lo esta, comprobamos si toca la izquierda de la pantalla		
	mov bx, [cpuY]
	cmp bx, [ballY] ; La parte superior de la paleta CPU es <= que la posicion de la pelota?		
	jg check_hit_left ; No, comprobamos si toca la izquierda 		
	add bx, PADDLEHEIGHT
	cmp bx, [ballY]				
	jl check_hit_left ;  Esta la parte inferior de la paleta de la cpu >= que la posicion de la pelota?
	neg byte [ballVelX] ; revertimos la direccion de X
    
    
    check_hit_left:
        cmp word [ballX], 0  ; La pelota pasa la parte izquerda de la pantalla?
	jg check_hit_right ; No, comprobamos si pasa la parte derecha
	inc byte [cpuScore] ; Si, aumentamos puntos CPU
	mov bx, PLAYERBALLSTARTX ; reseteamos la pelota para la siguiente ronda
	jmp reset_ball
   
    check_hit_right:
        cmp word [ballX], ROWLEN ; La pelota pasa la parte derecha de la pantalla?
	jl end_collision_checks ; No, finalizamos las comprobaciones
	inc byte [playerScore] ; Si, aumentamos la puntuacion del jugador
	mov bx, CPUBALLSTARTX ;reseteamos la pelota para la siguiente ronda
    
    reset_ball:
       cmp byte [cpuScore], WINSCORE  ; Comprobamos si ha ganado la cpu
       je lost
       cmp byte [playerScore], WINSCORE ; Comprobamos si ha ganado el usuario
       je won
       ;Movemos la pelota a su posicion inicial
       mov [ballX], bx	
       mov word [ballY], BALLSTARTY
    
    end_collision_checks: 
        ; Demoramos la ejecucion del siguiente ciclo
        call sleep 
        call sleep
jmp game_loop
   


setup_video_mode:
    mov ax, 0003h 
    int 10h

setup_video_memory:
    mov ax,VIDEOMEM
    mov es,ax ; B800:0000

hide_cursor:
   inc ah
   mov ch,25
   int 10h

sleeps:
   mov cl,10
   .sleep_loop:
       call sleep
       jl .sleep_loop
    
sleep: 
  mov ah, 86h 
  mov cx, 0
  mov dx, 33333 ;dx:cx en microsegundos
  int 15h

print_string:
    mov ah,0x0e ; teletype

.print_each_char:
    lodsb ; load next byte of SI
    cmp al, 0; comparamos byte con 0
    je .done ; saltamos a .done si son iguales
    int 10h 
    jmp .print_each_char

.done:
   ret

won:
    mov dword [es:0000], 0F490F57h  ; WI
    mov dword [es:0004], 0F210F4Eh  ; N!
    cli
    hlt
    
lost:
    mov dword [es:0000], 0F4F0F4Ch  ; LO
    mov dword [es:0004], 0F450F53h  ; SE
    cli
    hlt

string: db "Welcome PONG",0 ; Mensaje inicial

times 510-($-$$) db 0 ;rellena el resto del sector con 0 hasta la pos 510-$(posicion actual)-$$(Posicion primera etiqueta)
dw 0xaa55 ;define que es un sector de arranque

;;Mi versión simplificada de la implementación del PONG: https://www.youtube.com/watch?v=mYPzJlqQ3XI&t=2962s

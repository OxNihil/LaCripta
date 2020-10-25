Esta sección solo incluye algunos codigos experimentales sueltos en ensamblador.
Los comparto porque considero que puede ser de utilidad para quien se este iniciando 
a programar en esamblador

How to compile: nasm boot.asm -f bin -o boot.bin
How to test: quemu-system-i386
Debug desde quemu: qemu -s -S 

Conceptos para entender los códigos:

-POST (Power on self test) al arrancar comprueba que el hardware esta disponible
-Bin no permite simbolos de debug mientras que elf si 
-Posicion memoria mágica 0x7C00 -> Primera posición de memoria antes de esa posición hay codigo de la bios
-0x0A55; Numero magico, indica disco arranque, util para hacer una USB o Imagen booteable 

SysCalls

La bios -> Escribe pantala 0x10
	   Lee disco 0x13




alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
##########AUX############

def normalize_text(text):
    result = ""
    text = text.replace(" ", "").upper()
    for c in text:
        if c in alfabeto:
             result+=c
    return result

def get_desp(char):
    return (ord(char.upper())-65)

#########CAESAR#############
"""
El cifrado cesar general es un cifrado de sustitución monoalfabetico
consiste en sustituir una letra por la letra que ocupa X posiciones en el alfabeto

"""
def caesar_cipher(text,desp):
    cipher = ""
    for i in range(len(text)):   #Para cada letra del texto
        char = text[i]
        if (char.islower()):
            cipher += chr((ord(char) + desp - 97) % 26 + 97) #97 primera letra minuscula (a)
        else:
            cipher += chr((ord(char) + desp-65) % 26 + 65)  # Prima letra mayuscula (A) -> EJ caesar 3: (A(65) + 3-65) -> 3 % 26 = 3+65 = 68(D)   
    return cipher

def caesar_decipher(text,desp):
    plain = ""
    for i in range(len(text)):
        char = text[i]
        if (char.islower()):
            plain += chr((ord(char) -97-desp) % 26 + 97)
        else:
            plain += chr((ord(char) -65-desp) % 26 + 65)
    return plain

#########VIGENERE#########
"""
Vigenere se trata de un algoritmo de cifrado simetrico polialfabetico,
consiste en varias series de cifrado caesar general, por ello para implementar vigenere
es necesario tambien implementar caesar. El algoritmo prosigue de la siguiente forma:

Se introduce una clave de longitud menor o igual al texto, si es menor que el texto se repite
ciclicamente hasta ser de la misma longitud.
Vigenere utiliza para cifrar cada letra, el desplazamiento asociado
a la letra de la clave que le corresponde, ej:

m:HOLAATODOS --> HOLAATODOS
c:dos        --> DOSDOSDOSD

El funcionamiento del script es el siguiente:
-1. Se solicita el texto y se normaliza
-2. Para cifrar se recorre todo el texto, obteniendo el desplazamiento asociado a la clave para cada caracter
una vez obtenido el desplazamiento, se realiza un cifrado cesar general con el desplazamiento dado para esa letra
Se va almacenando las letras segun se cifran en un string y al finalizar se retorna el string

La función de descifrado es igual que la función de cifrado
"""
def vigenere_cipher(plain,clave):
    result = ""
    for i in range(0,len(plain)): #Para todo el texto
        desp = get_desp(clave[i % len(clave)]) #Obtenemos el desplazamiento asociado a la clave
        result +=(caesar_cipher(plain[i],desp)) #Ciframos la letra con caesar y la aÃ±adimos al string
    return result

def vigenere_decipher(text,clave):
    result = ""
    for i in range(0,len(text)): #Para todo el texto
        desp = get_desp(clave[i % len(clave)]) #Obtenemos el desplazamiento asociado a la clave
        result +=(caesar_decipher(text[i],desp)) #desciframos la letra con caesar para el desplazamiento dado 
    return result

#########MENU#########################

def menu():
    print("Vigenere")
    print("----------------\n")
    while(True):
        print("[1] Vigenere cipher ")
        print("[2] Vigenere decipher")
        print("[0] Salir")
        print("")
        opt = int(input("[+]> Elige una opcion: "))
        if opt == 0:
            break
        else:
            text = input("[+]> Introduce el texto: ")
            text = normalize_text(str(text))
            if opt == 1:
                clave = input("[+]> Introduce la clave: ")
                print(vigenere_cipher(text,clave))
            elif opt == 2:
                clave = input("[+]> Introduce la clave: ")
                print(vigenere_decipher(text,clave))
        print("\n")
menu()



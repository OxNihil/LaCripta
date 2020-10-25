
"""
La cifra afin se trata de un cifrado de sustitución monoalfabetico basado en la aritmetica modular
La aritmetica modular se construye mediante relacion de congruencia, las congruencias designa dos numeros enteros
a y b tienen el mismo resto al dividirlo por un numero naturarl m denominado modulo.

El script funciona de la siguiente manera:
1- Solicita el texto de entrada y lo normaliza con la función normalize_text para que solo trabaje con texto del alfabeto aceptado
2- La función de cifrado responde  a la formula  Cifrar afin:  C = (a * x + b ) mod m
a: constante decimación
x: caracter en texto claro
b: constante desplazamiento
m: modulo (longitud alfabeto)
Por lo que se solicitan la constante decimación y la constante de desplazamiento y se comprueban que sean validas

3- Se ejecuta la formula de cifrado: ALFABETO[((char * deci + desp) % len(ALFABETO))-1]

4- En cuanto al descifrado responde a la siguiente formula:  D = (a^-1) *(c-b) mod m
a^-1 : inverso modular --> Para que exista inversa se tiene que cumplir a*(a^-1)mod m = 1
c: letra cifrada
b: Constante de desplazamiento
m: modulo

5. Para calcular el inverso modular, primero se comprueba si el mcd entre la costante de decimacion y la longitud del
alfabeto es igual = 1, es decir ,se comprueba si a y m son primos entre si
6. Tras la comprobación anterior se realiza el algoritmo de euclides extentendido que expresa el numero como la minima combinación lineal: mcd(a,m) = a*x+m*y, siendo x el inverso modular.
7.Una vez obtenido el inverso modular se aplica la función de descifrado ALFABETO[((char - desp)*inv % len(ALFABETO))-1]


"""

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def normalize_text(text):
    result = ""
    text = text.replace(" ", "").upper()
    for c in text:
        if c in ALFABETO:
             result+=c
    return result

def mcd(a,b):
    #Algoritmo de euclides
    while a != 0:
        a, b = b % a,a
    return b

def euclides_ext(a,m):
#Algoritmo de euclides extendido
#Expresa el numero como la minima combinaciรณn lineal: mcd(a,m) = a*x+m*y
    if a == 0 :   
        return m,0,1     
    mcd,x1,y1 = euclides_ext(m % a, a)  
    #Actualizamos x e y en la llamada recursiva
    x = y1 - ( m //a ) * x1  
    y = x1  
    return mcd,x,y 

def inv_modular(a,m):
    #Devuelve el inverso modular
    if mcd(a,m) != 1:
        return None #Si a y m no son coprimos no existe inversa
    return euclides_ext(a,m)[1]

def check_clave(deci,desp):
    if deci not in range(2,97):
        print("[+]>Las constantes no estan dentro del rango admitido")
        print("[+]>Rango valido: Decimacion [2,97]")
    elif desp not in range(0,97):
        print("[+]>Las constantes no estan dentro del rango admitido")
        print("[+]>Rango valido: Desplazamiento [0,97]")
        raise SystemExit()
    if mcd(deci,len(ALFABETO)) != 1:
        print("La constante "+str(deci)+"y la longitud del alfabeto "+str(len(ALFABETO))+" no son coprimos")
        raise SystemExit()

#Cifrar afin:  C = (a * x + b ) mod m
#a: constante decimaciรณn
#b: constante desplazamiento
#m: simbolos alfabeto   
def cifra_afin(text,deci,desp):
    check_clave(deci,desp)
    result = ""
    for char in text:
        if char in ALFABETO:
            ind = ALFABETO.find(char) + 1
            result += ALFABETO[((ind * deci + desp) % len(ALFABETO))-1]
    return result


#Descifrar afin: D = (a^-1) *(c-b) mod m
#a^-1 : inverso modular --> a*(a^-1)mod m = 1
#c: letra cifrada
def descifra_afin(text,deci,desp):
    check_clave(deci,desp)
    plain = ""
    inv = inv_modular(deci,len(ALFABETO))
    for char in text:
        if char in ALFABETO:
            ind = ALFABETO.find(char) + 1
            plain += ALFABETO[((ind - desp)*inv % len(ALFABETO))-1]
    return plain


def menu():
    print("Afin")
    print("----------------\n")
    while(True):
        print("[1] Afin cipher ")
        print("[2] Afin decipher")
        print("[0] Salir")
        print("")
        opt = int(input("[+]> Elige una opcion: "))
        if opt == 0:
            break
        else:
            text = input("[+]> Introduce el texto: ")
            text = normalize_text(str(text))
            if opt == 1:
                deci = int(input("[+]> Introduce la constante decimacion: "))
                desp = int(input("[+]> Introduce el desplazamiento: "))
                print(cifra_afin(text,deci,desp))
            elif opt == 2:
                deci = int(input("[+]> Introduce la constante decimacion: "))
                desp = int(input("[+]> Introduce el desplazamiento: "))
                print(descifra_afin(text,deci,desp))
        print("\n")

menu()

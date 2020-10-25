import sys,math
from itertools import combinations

"""
El método kasiski comienza buscando cadenas de texto con al menos 3 letras consecutivas repetidas en el criptograma. Entonces la distancia entre cadenas identicas consecutivas son probablemente múltiplos de la clave utilizada, cuantas más cadenas repetidas más se acortara la posible longitud de  la clave. Para obtener la posible longitud de la clave nos quedamos con el mcd de todas las distancias. Una vez obtenido la longitud de la clave y en relación al propio funcionamiento de vigenere ,dividimos el criptograma en tantos subcriptogramas como la longitud L, esos subcriptogramas contendrán texto cifrado de forma monoalfabetica por cesar, por lo que al realizar un análisis de frecuencia podemos obtener la posible correspondencia entre las letras del texto cifradas más comunes y las letras más comunes del idioma.
Al juntar las letras mas frecuentes de cada subcriptograma obtenemos la clave más probable.

Funcionamiento del scipt:

1- Se abre el archivo donde esta almacenado el texto y se normaliza para que solo contenga caracteres del alfabeto objetivo
2-Se comprueba la longitud del texto, si esta menor que 3 veces la longitud del alfabeto , se muestra un mensaje avisando de que los resultados pueden no ser fiables
3- Se llama a la funcion identify_repeat_chains que retornara las tuplas (cadena,distancia) entre caracteres repetidos.
Para ello recorre el texto y cojeemos un string con 3 cararacteres, para cadena recorremos el texto 
y comparamos si encontramos otra cadena igual, si es así buscamos más y añadimos al la lista a retornar una tupla con la cadena y la distancia
4- Una vez obtenidas las tuplas, llamamos a la función frequency_distance_repeat, la cual mete en una lista las distancias de cada tupla y halla todas las combinaciones de distancias de longitud 2. A cada combinación calcula el mcd y actualizando un diccionario con la siguiente forma {mcd:n_veces_que_aparece} y retornamos el diccionario.
5- Llamamos a la funcion get_statics , la cual calcula el porcentaje de aparición de cada mcd retornando el que más veces aparece, siendo este mcd la longitud de la clave más probable
6- Ahora que ya sabemos la longitud llamamos a la funcion get_subcriptograms que nos devuelve una lista con tantos subcriptogramas como la longitud del texto
7- Ahora llamamos a la funcion guess_key, que intentara adivinar la clave, para ello a cada criptograma le realiza un analisis de frecuencia (Cuenta las apariciones de una letra sobre el total del subcriptograma) y añade a una lista las 3 letras más frecuentes de cada subcriptograma. Tras procesar todos los subcripgramas la función retorna 2 valores: la lista con las 3 letras más frecuentes de cada subcriptograma y la clave más probable que se corresponde con la letra más frecuente en cada subcriptogra.

Aquí acaba kasiski aunque de forma adicional se ha añadido una funcion check_guess que comprueba si la clave más probable es correcta, dado que debido a que el método de adivinación se basa en análisis de frecuencia, puedes encontrarte pequeñas variaciones según el texto que hagan que la letra más probable de cada subcriptograma no sea la letra que conforme la clave, sino que sea la segunda o tercera letra más probable. Esta funcion de verificación se basa en el Índice de coincidencia el cual tiene un valor constante por cada idioma (en este scipt solo esta habilitado para el español). En caso de que el índice de coincidencia del texto descifrado con esa clave este dentro del rango de valores del IOC del español (0.077) con un error del 5% consideraremos que esa clave puede ser una posible clave.En caso de que sea una posible clave se muestra el texto descifrado con esa clave.

Ya se sale de la scope del script pero se podría llegar a descifrar vigenere de forma automática en caso de que la clave más probable sea errónea, probando las posibles claves con los caracteres de la lista de los 3 mas frecuentes y verificándola con el IOC, reduciendo las combinaciones posibles en la fuerza bruta de 26^L (longitud) a 3^L
"""

alphabet ="ABCDEFGHIJKLMNRSTUVWXYZ"
MIN_LEN = 3 *len(alphabet)
IOC_SP = 0.0770

# AUX FUNS

def normalize_text(text):
    return text.replace(" ", "").upper()

def divisors(n):
    l = []
    for i in range(2, n//2 +1):
        if n % i == 0:
            l.append(i)

def check_min_len(text):
    if len(text) < MIN_LEN: # 3 veces el alfabeto
        print("[!]El texto es demasiado corto los resultados pueden no ser fiables")
        return False
    else:
        return True
    
def sort_list(lista):
    ordenado = {}
    for i in sorted (lista) :
        ordenado[i]=lista[i]
    return ordenado
    
def ioc(freq_list,lon):
	ind = 0
	freq_list = sort_list(freq_list)
	for i in freq_list.values():
		ind += i *(i-1)
	ind /= lon*(lon-1)
	return ind

# CAESAR
def caesar_cipher(text,desp):
    cipher = ""
    text = normalize_text(text)
    for i in range(len(text)):
        char = text[i]
        if (char.islower()):
            cipher += chr((ord(char) + desp - 97) % 26 + 97)
        else:
            cipher += chr((ord(char) + desp-65) % 26 + 65)
    return cipher

def caesar_decipher(text,desp):
    text = normalize_text(text)
    plain = ""
    for i in range(len(text)):
        char = text[i]
        if (char.islower()):
            plain += chr((ord(char) -97-desp) % 26 + 97)
        else:
            plain += chr((ord(char) -65-desp) % 26 + 65)
    return plain


# VIGENERE
def get_desp(char):
    return (ord(char.upper())-65)

def vigenere_cipher(plain,clave):
    result = ""
    plain = normalize_text(plain)
    for i in range(0,len(plain)): #Para todo el texto
        desp = get_desp(clave[i % len(clave)])
        result +=(caesar_cipher(plain[i],desp))
    return result

def vigenere_decipher(text,clave):
    result = ""
    for i in range(0,len(text)): #Para todo el texto
        desp = get_desp(clave[i % len(clave)])
        result +=(caesar_decipher(text[i],desp))
    return result

def frequency_analisys(text):
    frequency_len = {}
    count = 0
    for i in range(len(text)):
        if text[i] not in frequency_len:
            frequency_len[text[i]] = 1
        else:
            frequency_len[text[i]] = frequency_len[text[i]]+1
        count+=1
    frequency_len = sort_list(frequency_len)
    return frequency_len

def frequency_distance_repeat(tuples):
    frequency_len = {}
    distancias = []
    for i in range(len(tuples)):
        distancias.append(tuples[i][1])
    comb = combinations(distancias,2)
    for i in list(comb):
        gcd = math.gcd(i[0],i[1])
        if gcd not in frequency_len and gcd > 1:
            frequency_len[gcd] = 1
        else:
            if gcd > 1:
                frequency_len[gcd] = frequency_len[gcd]+1
    return frequency_len

def get_subcriptograms_list(text,max_prob):
	criptograms = []
	criptograms_list = get_subcriptogram(text,max_prob) 
	for i in range(max_prob):
		criptograms.append(get_criptogram_string(criptograms_list[i]))
	return criptograms
	
def get_subcriptogram(text,lon):
    criptograms = []
    for i in range(lon):  #Creamos tantas listas como longitod
        criptograms.append([])
    for i in range(len(text)):
        criptograms[i % lon].append(text[i])
    return criptograms

def get_criptogram_string(lista):
    result = ""
    for i in list(lista):
        result += i
    return result

def get_more_prob(l, max):
	#Obtenemos las 3 posiciones mรกs probable
	result = []
	for i in range(max):
		mas_prob = get_statics(l)
		result += mas_prob
		del l[mas_prob]
	return result
	  	
def get_statics(l):
    mayor = 0
    longitud = 0
    total = 0
    for i in list(l):
        total += l[i]
    for j in list(l):
        percent = round(l[j]/total*100,2)
        if percent > mayor:
            mayor = percent
            longitud = j
    return longitud

def identify_repeat_chains(text): # obtain tuplas
    i = 0
    dist = [] # Lista de tuplas (cadena,distancia)
    while i < len(text):
        cad= text[i:i+3] # Cojemos los 3 caracteres y comprobamos longitud
        lcad = len(cad)
        if lcad == 3:
            for j in range(i+1,len(text)): #Recorremos el texto
                if text[i:i+lcad] == text[j:j+lcad]: # comparamos si encontamos otra cadena de 3 igual, si es asi buscamos mรกs
                    while text[i:i+lcad] == text[j:j+lcad]:
                        lcad = lcad + 1
                    lcad = lcad -1
                    dist.append((text[i:i+3],j - i)) # Tenemos una tupla con la cadena y la distancia
            i = i + lcad-3+1
        else:
            i+=1
    return dist

def check_guess(text,key,lon):
    error = 0.05
    lim_sup = IOC_SP *(1+error)
    lim_inf = IOC_SP -(IOC_SP*error)
    text_plain = vigenere_decipher(text,key)
    fr = frequency_analisys(text_plain)
    ind = ioc(fr,len(text))
    if ind < lim_sup and ind > lim_inf:
        return True
    return False
    
def guess_key(criptograms,lon, max):
	keys = []
	for c in criptograms:
		fr = frequency_analisys(c)
		keys.append(get_more_prob(fr, max))
	most_prob_key = ""
	for letter in keys:
		most_prob_key += letter[0]
	return most_prob_key, keys
	

def analisis_kasiski(text):
    text = normalize_text(text)
    check_min_len(text)
    tuplas = identify_repeat_chains(text)
    len_freq = frequency_distance_repeat(tuplas)
    max_prob = get_statics(len_freq)
    print("[+] La longitud de la clave más probable es :",max_prob)
    criptograms = get_subcriptograms_list(text,max_prob)  #obtenemos la lista de criptogramas
    key,key_list = guess_key(criptograms,max_prob, 3)
    print("[+] La clave más probable es :",key)
    if(check_guess(text,key,max_prob)):
        pltxt = vigenere_decipher(text,key)
        print()
        print(pltxt)
        print()
        return pltxt
    else:
        max = 3
        opt = ""
        print()
        print(vigenere_decipher(text, key))
        print()
        while (not check_guess(text, key, max_prob)):
            if opt != "1":
                print("[!] La clave no parece ser la correcta :(\n")
                for i in key_list:
                    print(i)
                print()
            print("[0] Salir")
            print("[1] Aumentar tamaño de matriz")
            print("[2] Introducir clave manualmente\n")
            opt = input("¿Qué desea hacer? [0/1/2] ")
            if opt == "0":
                exit(0)
            elif opt == "1":
                max += 1
                _,key_list = guess_key(criptograms,max_prob, max)
                for i in key_list:
                    print(i)
                print()
                continue
            elif opt == "2":
                for i in key_list:
                    print(i)
                print()
                print("La longitud de la clave más probable es :", max_prob)
                key = input("Introduzca la clave que desea probar: ")
            else:
                while opt != "0" and opt != "1" and opt != "2":
                    opt = input("¿Qué desea hacer? [0/1/2] ")
                continue
            print()
            print(vigenere_decipher(text, key.upper()))
            print()
        return vigenere_decipher(text, key)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: kasiski.py <archivo con texto cifrado>")
        exit(-1)
    try:
        fp = open(sys.argv[1])
        cifrado = fp.read()
        pltxt = analisis_kasiski(cifrado)
        if pltxt != None:
            fp.close()
            nuevo = sys.argv[1] + "_descifrado.txt"
            fp = open(nuevo, "w+")
            fp.write(pltxt)
            print("El archivo descifrado se ha guardado como \"", nuevo,"\"", sep="")
    except OSError:
        print("No se encuentra el archivo \"", sys.argv[1], "\"", sep="")
        exit(-1)
    finally:
        fp.close()

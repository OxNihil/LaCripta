import math
from itertools import combinations
from collections import Counter
from itertools import permutations

alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


########AUX###################

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


####### AUTOKEY ##########

def autokey_cipher(plain,clave):
    result = ""
    key = clave+plain[0:len(clave)]+plain[len(clave):-len(clave)]
    key = normalize_text(key)
    plain = normalize_text(plain)
    res = vigenere_cipher(plain,key)
    return res 

def autokey_decipher(cipher,clave):
    result = []
    i = 0
    for letter in cipher:
        x = alfabeto.index(letter)
        if i < len(clave):
            y = alfabeto.index(clave[i].upper())
        else:
            y = alfabeto.index(result[i-len(clave)])
        desp = (((x-y)+26)%26)
        result.append(alfabeto[desp])
        i+=1
    return "".join(result)


###########IC###########################

def frequency_analisys(text):
    frequency_len = {}
    count = 0
    for i in range(len(text)):
        if text[i] not in frequency_len:
            frequency_len[text[i]] = 1
        else:
            frequency_len[text[i]] = frequency_len[text[i]]+1
        count+=1
    return frequency_len

def ic(freq_list,lon):
	ind = 0
	for i in freq_list.values():
		ind += i *(i-1)
	ind /= lon*(lon-1)
	return ind

##############KASISKI#################
MIN_LEN = 3 *len(alfabeto)

def check_min_len(text):
    if len(text) < MIN_LEN: # 3 veces el alfabeto
        print("[!]El texto es demasiado corto los resultados pueden no ser fiables")
        return False
    else:
        return True

def identify_repeat_chains(text):
    i = 0
    dist = [] # Lista de tuplas (cadena,distancia)
    while i < len(text):  
        cad= text[i:i+3] # Cojemos los 3 caracteres y comprobamos longitud
        lcad = len(cad)
        if lcad == 3:
            for j in range(i+1,len(text)): #Recorremos el texto
                if text[i:i+lcad] == text[j:j+lcad]: # si encontramos otra cadena de 3 igual, buscamos mas
                    while text[i:i+lcad] == text[j:j+lcad]:
                        lcad = lcad + 1
                    lcad = lcad -1
                    dist.append((text[i:i+3],j - i)) # Tenemos una tupla con la cadena y la distancia
            i = i + lcad-3+1
        else:
            i+=1
    return dist

def frequency_distance_repeat(tuples):
    frequency_len = {} #Dict con {mcd:frecuencia}
    distancias = []
    for i in range(len(tuples)): #Iteramos la lista de tuplas
        distancias.append(tuples[i][1]) # añadimos el valor a la lista de distancias
    comb = combinations(distancias,2) # Obtenemos las combinaciones posibles de distancias 2 a 2
    for i in list(comb): # Para cada posible combinación
        gcd = math.gcd(i[0],i[1]) #obtenemos maximo comun divisor y la frecuencia de aparición
        if gcd not in frequency_len and gcd > 1: 
            frequency_len[gcd] = 1
        else:
            if gcd > 1:
                frequency_len[gcd] = frequency_len[gcd]+1
    return frequency_len

def get_long(l):
    for key, value in l.items():
        if value == max(l.values()):
            return key

def get_subcriptogram(text,lon):
    criptograms = []
    for i in range(lon):  #Creamos tantas listas como longitud de la clave
        criptograms.append([])
    for i in range(len(text)):
        criptograms[i % lon].append(text[i])
    for i in range(len(criptograms)):
        criptograms[i] = ("".join(criptograms[i]))
    return criptograms

letter_freq_sp={"A":11.72,"B":1.49,"C":3.87,"D":4.67,"E":13.72,"F":0.69,"G":1.00,"H":1.18,"I":5.28,"J":0.52,"K":0.11,"L":5.24,"M":3.08,"N":6.83,"Ñ":0.17,"O":8.44,"P":2.89,"Q":1.11,"R":6.41,"S":7.20,"T":4.60,"U":4.55,"V":1.05,"W":0.04,"X":0.14,"Y":1.09,"Z":0.47}

def score_difference(text):
    counter = Counter(text)
    return sum([abs(counter.get(letter,0)* 100 /len(text)-letter_freq_sp[letter]) for letter in alfabeto]) / len(alfabeto)

def guess_key(criptograms):
    keys = []
    for c in criptograms:
        scoremin = 10
        key = ""
        for i in range(len(alfabeto)):
            text = caesar_decipher(c,i)
            score = score_difference(text)
            if score < scoremin:
                scoremin = score
                key = alfabeto[i]
        keys.append(key)    
    return "".join(keys)

####Vigenere IC#######
def guess_len_ic(ciphertext):
    maxdeltaioc = 0
    pos = 0
    for i in range(2,12):
        criptos = get_subcriptogram(ciphertext,i)
        iclist = []
        for j in criptos:
            freq = frequency_analisys(j)
            ioc = ic(freq,len(j))
            iclist.append(ioc)
        #calculate delta ioc
        deltaioc = sum(iclist)/len(iclist)
        if deltaioc > maxdeltaioc:
            maxdeltaioc = deltaioc
            pos = i
    return pos

#####Autokey##############3
def guess_autokey(ciphertext,minlen,maxlen):
    for keylen in range(minlen,maxlen+1):
        mindelta = 0
        mindkey = ""
        for i in permutations(alfabeto,keylen):
            key = ''.join(i)
            pt = autokey_decipher(ciphertext,key)
            freq = frequency_analisys(pt)
            dioc = ic(freq,len(pt))
            if dioc > mindelta:
                mindelta = dioc
                mindkey = key
                print(mindkey,mindelta,ceil(IOC_SP-mindelta,2),score_difference(pt))
                if score_difference(pt) < 1:
                    return mindkey
    return mindkey



if __name__ == "__main__":
    print("[+] Kasiski")
    sample = "Pn we tjzac dg ci Btnnhc, um rnyz nqdjgx nz qwzmgh anotuigfe, yo jr ujvhz tkvueh qfe xzdíp nn sifrtvh dp lqj lt eayzc vv plttlnvzd, tdlrir icmiruc, iwríg fwaef g vtlro efzgxdzr. Wei dell dg rtvh mád vcti fne natemgh, sllrzkóc ead máu ewraed, dwvtdl y bugszpgtzs nfa háuaoou, cicmeuau cwh oiprpva, pegúy pccwbbnz dg rñisbdfrc cwh woxipxwh, voyswdíic ead ttva etreeu um hn hlckvvst."
    sample = normalize_text(sample)
    if check_min_len(sample):
        print("Texto cifrado")
        print(sample)
        tuples = identify_repeat_chains(sample)
        freq = frequency_distance_repeat(tuples)
        longitud = get_long(freq)
        print("[+]Kasiski key length: "+str(longitud))
        longitud2 = guess_len_ic(sample)
        print("[+]IC key len: "+str(longitud2))
        criptos = get_subcriptogram(sample,longitud)
        key = guess_key(criptos)
        print("[key] = "+key)
    else:
        print("Texto de longitud insuficiente")
    print("[+] Autokey")
    text = "ORSRYOTLLJECDQLNOHNFLCXCQHMAOFQOFUHWULWETCRFOIPEEALNABCTIVPSFXSCJSLCZDIPVHCQHTJOOKZRWOSDDRKARMAWGIDEMCZEUORJARTTITNIXICZBHTNHZYIOJMONUFTSUFVXBRIYLOOPAOKOXGGHAUVQWESUVPEIBWRZHINDVNOFXAKZOUUSUKYWOIWJEMCRLEOKOFECKDOTSDPSOOFEEWTWUOKGWWMVIJNPYUYVUYDMTBALROQEDVDXZDFFSOCELBSWFICFUIZAUZTAFERWLGEJIEJWIKXLSWPEPLE"
    print("Guessing the key....")
    key =  guess_autokey(text,2,3)

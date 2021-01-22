import argparse, sys

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-C","-c", help="Cipher", action='store_true')
    parser.add_argument("-D","-d", help="Dechipher", action='store_true')
    parser.add_argument("-G","-g", help="Only generate keysream RC4", action='store_true')
    parser.add_argument("-k", "--key",help="Key to use",required=True)
    parser.add_argument("-v", "--verbose",help="Shows in detail how the algorithm works",action='store_true')
    parser.add_argument("-vs", "--step", help="Shows in detail how the algorithm works step by step", action='store_true')
    options = parser.parse_args(args)
    return options

def check_opts(opts):
    #Caso de error: flags invalidos
    if opts.D and (opts.C or opts.G):
        print("[!] Invalid flags")
        exit()
    elif opts.C and (opts.D or opts.G):
        print("[!] Invalid flags")
        exit()
    elif opts.G and (opts.C or opts.D):
        print("[!] Invalid flags")
        exit()

# AUX FUNS
def convert_key(s):
    return [ord(c) for c in s]

def is_hex(s):
    try:
       int(s, 16)
    except ValueError:
        return False
    return len(s) % 2 == 0

def hex_to_str(txt):
    result = []
    for i in range(int(len(txt)/2)):
        result.append(chr(bytes.fromhex(txt)[i]))
    return result

def convert_keystream(gen,lon):
    k = []
    for i in range(lon):
        k.append(next(gen))
    return k

def check_key(key):
    if len(key) > 256 or len(key) == 0:
        print("[!] Invalid key")
        exit()
    

def swap(vector,i,j):
    tmp = vector[i]
    vector[i] = vector[j]
    vector[j] = tmp

#RC4
    
def KSA(key,verbose=False, step=False):
    print("[+] Vector S initial status")
    #Inicializacion del vector de estado
    S = list(range(256)) 
    print(S)
    #Desordenacion del vector de estado
    j = 0
    keylen = len(key)
    for i in range(256):
        j = (j + S[i] + key[i % keylen]) % 256
        swap(S,i,j)
        if(verbose or step):
            print("[+] KSA: Vector S status iter "+str(i)+":")
            print(S)
            print("")
        if (step and i%8==0):
            input("Press [enter] to continue")
    return S

#Generaciรณn del flujo de cifrado pseudo-aleatorio
def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        swap(S,i,j)
        print("\n[+] PRGA: Swap pos "+str(i)+","+str(j)+": ")
        print(S)
        k = S[(S[i] + S[j]) % 256]
        yield k #Retornamos el generador

#Get the keystream 
def RC4(key,verbose=False, step=False):
    S = KSA(key,verbose, step)
    print("\n[+] Vector S status after KSA: ")
    print(S)
    return PRGA(S)

#La funcion de cifrado es la misma que la de descifrado 
def cipher(keystream,c):
    char = '%d'% (ord(c) ^ keystream)
    return char


#Creamos un registro para ir almacenando los datos RC4
class status:
    key = []
    keystream = []
    plain = []
    cipher = []

def main():
    state = status()
    opts = getOptions()
    check_opts(opts)
    #Comun a todos caso de uso
    state.key = convert_key(opts.key)
    keystream = RC4(state.key,opts.verbose,opts.step)
    if opts.D:
        while True:
            txt = input("\n[+] Input byte in hex to decipher[Write \"END\" to finish]: ")
            if txt.upper() == "END": break
            if len(txt) != 2: continue
            txt = txt.upper()
            #Comprobacion de que sea un caracter hex           
            if (not is_hex(txt)):
                    continue
            #Se ha implementado de forma que el formato del texto a descifrar tiene que ser hex
            #Debido a que el contenido a descifrar pueden ser caracteres ascii no imprimibes
            #Y en codificacion decimal la longitud de cada caracter puede ser variable
            st = hex_to_str(txt)[0]
            print(st)
            dec_keystream = next(keystream)
            state.keystream.append(dec_keystream)
            state.plain.append(cipher(dec_keystream,st))
            state.cipher.append(txt) 
            print("\n[+] KEY: "+ str(state.key))
            print("[+] KEYSTREAM: "+ str(state.keystream))
            print("[+] CIPHER: "+str(state.cipher))
            print("[+] DECIPHER: "+str(state.plain))
    if opts.G:
        while True:
            txt = input("\n[+] Press Enter to continue [Write \"END\" to finish]: ")
            if txt.upper() == "END": break
            dec_keystream = next(keystream)
            state.keystream.append(dec_keystream)
            print("\n[+] KEY: "+ str(state.key))
            print("[+] KEYSTREAM: "+ str(state.keystream))
    elif opts.C:
        while True:
            txt = input("\n[+] Input character to cipher[Write \"END\" to finish]: ")
            if txt.upper() == "END": break
            if len(txt) != 1: continue
            state.plain.append(txt)
            dec_keystream = next(keystream)
            state.keystream.append(dec_keystream)
            state.cipher.append(cipher(dec_keystream,txt)) 
            print("\n[+] KEY: "+ str(state.key))
            print("[+] KEYSTREAM: "+ str(state.keystream))
            print("[+] PLAINTEXT: "+str(state.plain))
            print("[+] CIPHER: "+str(state.cipher))
        


#main()
if len(sys.argv) < 2:
	print("Usage: python3 "+sys.argv[0]+" --help")
	sys.exit(1)

if __name__ == "__main__":	
    main()

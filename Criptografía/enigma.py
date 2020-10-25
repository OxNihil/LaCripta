import re

LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

cableado_rotor = [ 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', #1
                   'AJDKSIRUXBLHWTMCQGZNPYFVOE', #2
                   'BDFHJLCPRTXVZNYEIWGAKMUSQO', #3
                   'ESOVPZJAYQUIRHXLNFTGKDCMWB', #4
                   'VZBRGITYUPSDNHLXAWMJQOFECK', #5
                   'JPGVOUMFYQBENHZRDKASXLICTW', #6
                   'NZJHGRCXMYSWBOUFAIVLPEKQDT', #7
                   'FKQHTLXOCBJSPDZRAMEWNIUYGV'] #8
cableado_reflector = [
                'EJMZALYXVBWFCRQUONTSPIKHGD', #A
                'YRUHQSLDPXNGOKMIEBFZCWVJAT', #B
                'FVPJIAOYEDRZXWGCTKUQSBNMHL'] #C

#AUX FUNS
def char_to_pos(char):
    return int(ord(char)-65)

def change(char,alfabeto=LETRAS,veces=0):
    char = alfabeto[(char_to_pos(char)+veces) % 26]
    return char

def match_string_letters(str1,str2):
    for c in range(len(str1)):
            if str1[c] == str2[c]:
                   return True

def dfs(visited,graph,node):
    if node not in visited:
        visited.add(node)
        for neightbour in graph[node]:
            #comprobar si el vecino es nodo hoja final, si lo es añadir y no llamar recursivamente
            if neightbour not in graph:
                visited.add(neightbour)
                continue
            dfs(visited,graph,neightbour)
#

class enigmaM3:
    reflector = ""
    rotores = ""
    rotores_inv = ""
    clavijero = ""
    pos_ini= "" #Posicion inicio se actualiza con cada caracter
    pos_interna = ('A','A','A')
    opts = []
    muesca = (('Q',),('E',),('V',),('J',),('Z',),('Z','M'),('Z','M'),('Z','M'))
    #Las muescas indican donde se produce el giro del siguiente rotor en el  momento
    #en que el anterior pasa por las muescas. Una para cada rotor, salvo 6,7,8 que tiene 2
    def __init__(self,rot,ref,pos_ini,pos_int,plugboard=None):
        self.set_rotors(rot)
        self.set_reflector(ref)
        self.set_pos_ini(pos_ini)
        self.set_pos_interna(pos_int)
        self.set_plugboard(plugboard)
        self.rotores_inv = self.rotor_inverso()
        self.opts.append([rot,ref,pos_ini,pos_int,plugboard])
    #CONF - Setters
    def set_reflector(self,char):
        self.reflector = cableado_reflector[char_to_pos(char)]
    def set_rotors(self,rot):
        self.rotores = tuple([q-1 for q in rot])
    def set_pos_ini(self,pos_ini):
        self.pos_ini = list(pos_ini)
    def set_pos_interna(self,pos_int):
        self.pos_initerna = (pos_int)
    def set_plugboard(self,plugboard):
        self.clavijero = plugboard
    def set_machine(self,rot,ref,pos_ini,pos_int,plugboard):
        self.set_rotors(rot)
        self.set_reflector(ref)
        self.set_pos_ini(pos_ini)
        self.set_pos_interna(pos_int)
        self.set_plugboard(plugboard)
    #CORE - Basic Ops
    def refleja(self,char):
        #Realiza la sustitución del reflector
        #El reflector es un  num 0 - 2
        return change(char,self.reflector)
    def reset(self):
        opts = self.opts[0]
        self.__init__(opts[0],opts[1],opts[2],opts[3],opts[4])
    #CORE - Plugboard
    def apply_plugboard(self,char):
        for i in self.clavijero:
            if char == i[0]: return i[1]
            if char == i[1]: return i[0]
        return char
    #CORE - Rotor
    def rotar(self,char,veces,rotor):
        #char - caracter a cifrar
        #veces - veces que ha girado el rotor
        #rotor - rotor a utilizar
        char = change(char,rotor,veces)
        #Letra salida por el rotor
        return change(char,veces=-veces)
    
    def vuelta_rotor(self,rotor):
        salida = ""
        #Sigue por el rotor el recorrido de vuelta de la señal desde el reflector
        for i in LETRAS:
            salida += LETRAS[rotor.find(i)]
        return salida
    def rotor_avanza(self):
        #Los rotores se mueven al siguiente rotor dependiendo de su posicion
        if self.pos_ini[1] in self.muesca[self.rotores[1]]:
            #Incrementa la posicion una letra
            self.pos_ini[0] = change(self.pos_ini[0],veces=1)
            self.pos_ini[1] = change(self.pos_ini[1],veces=1)
        if self.pos_ini[2] in self.muesca[self.rotores[2]]:
            self.pos_ini[1] = change(self.pos_ini[1],veces=1)
        self.pos_ini[2] = change(self.pos_ini[2],veces=1)
    def rotor_inverso(self):
        #Devuelve una tupla conel recorrido inverso de los 8 rotores
        inv = []
        for i in range(len(cableado_rotor)):
            inv.append(self.vuelta_rotor(cableado_rotor[i]))
        return inv    
    #MAIN FUNS
    def cifrar_letra(self,char):
        #Con cada letra los rotores avanzan
        self.rotor_avanza()
        #Entrada en el clavijero
        char = self.apply_plugboard(char)
        #Camino de ida de la señal
        for i in [2,1,0]:
            veces = ord(self.pos_ini[i]) - ord(self.pos_interna[i])
            char = self.rotar(char,veces,cableado_rotor[self.rotores[i]])
        #Aplicamos reflector
        char = self.refleja(char)
        #Camino de vuelta de la señal
        for i in [0,1,2]:
            veces = ord(self.pos_ini[i]) - ord(self.pos_interna[i])
            char = self.rotar(char,veces,self.rotores_inv[self.rotores[i]])
        #Salida por el clavijero
        char = self.apply_plugboard(char)
        return char
    def descifrar(self,text):
        #Resetear estado maq?
        #Misma funcion la de cifrado y descifrado
        return self.cifrar(text)
    def cifrar(self,text):
        salida = ""
        for c in text:
            if c.isalpha(): salida += self.cifrar_letra(c)
            else: salida += c
        return salida
    
   

#Configuración Enigma default
plain = "ENUNLUGARDELAMANCHADECUYONOMBRENOQUIEROACORDARME"
#expectedZADEMFNSUHIQOWUIVUOOMTLIDLVGKAHTEEAGNWJLTDVGHNQR

#Posicion inicial rotores
inicio = ('A','B','C')
#Orden rotores
rotores = (4,1,3)
#Reflectores
reflector = 'B'
#Posicion interna
pos_interna = ('A','A','A')
#plugboard
plugboard = [('A','M'),('F','I'),('N','V'),('P','S'),('T','U'),('W','Z')]

enigma = enigmaM3(rotores,reflector,inicio,pos_interna,plugboard)
texto_cifrado = enigma.cifrar(plain)
print("##############")
print("    CIFRADO   ")
print("##############")
print(plain)
print(texto_cifrado)
print("\n##############")
print(" DESCIFRADO   ")
print("##############")
print(texto_cifrado)
enigma.reset()
texto_descifrado = enigma.descifrar(texto_cifrado)
print(texto_descifrado)
enigma.reset()


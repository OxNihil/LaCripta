reflectores = [ 'EJMZALYXVBWFCRQUONTSPIKHGD', #A    
              'YRUHQSLDPXNGOKMIEBFZCWVJAT',        
              'FVPJIAOYEDRZXWGCTKUQSBNMHL'] #C

con_rotores = [ 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', #1       
            'AJDKSIRUXBLHWTMCQGZNPYFVOE',        
            'BDFHJLCPRTXVZNYEIWGAKMUSQO',        
            'ESOVPZJAYQUIRHXLNFTGKDCMWB',        
            'VZBRGITYUPSDNHLXAWMJQOFECK',      
            'JPGVOUMFYQBENHZRDKASXLICTW',       
            'NZJHGRCXMYSWBOUFAIVLPEKQDT',        
            'FKQHTLXOCBJSPDZRAMEWNIUYGV'] #8      

vuelta_rotores = ['UWYGADFPVZBECKMTHXSLRINQOJ',
                  'AJPCZWRLFBDKOTYUQGENHXMIVS',
                  'TAGBPCSDQEUFVNZHYIXJWLRKOM',
                  'HZWVARTNLGUPXQCEJMBSKDYOIF',
                  'QCYLXWENFTZOSMVJUDKGIARPHB',
                  'SKXQLHCNWARVGMEBJPTYFDZUIO',
                  'QMGYVPEDRCWTIANUXFKZOSLHJB',
                  'QJINSAYDVKBFRUHMCPLEWZTGXO']

ALFABETO = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def normalize_text(text):
    result = ""
    text = text.replace(" ", "").upper()
    for c in text:
        if c in ALFABETO:
             result+=c
    return result

def char_to_pos(char):       
    return int(ord(char)-65) 

def change(char,charset=ALFABETO,n=0):
    pos = char_to_pos(char)+n
    char = charset[pos % 26]        
    return char

class enigmaM3:                       
    reflector = ""       
    rotores = ""      
    plugboard = ""                   
    pos_ini= "" #Posicion inicio se actualiza con cada caracter       
    pos_interna = ('A','A','A')              
    muesca = (('Q',),('E',),('V',),('J',),('Z',),('Z','M'),('Z','M'),('Z','M'))
    opts = []
    def __init__(self,rot,ref,pos_ini,pos_int,plugboard=None):       
        self.set_rotors(rot)       
        self.set_reflector(ref)       
        self.set_pos_ini(pos_ini)       
        self.set_pos_interna(pos_int)       
        self.set_plugboard(plugboard)
        self.opts.append([rot,ref,pos_ini,pos_int,plugboard])
    def set_reflector(self,char):       
        self.reflector = reflectores[char_to_pos(char)]
    def set_rotors(self,rot):       
        rots = []
        for q in range(len(rot)):
            rots.append(rot[q]-1)
        self.rotores = tuple(rots)       
    def set_pos_ini(self,pos_ini):       
        self.pos_ini = list(pos_ini)       
    def set_pos_interna(self,pos_int):                      
        self.pos_interna = (pos_int)                       
    def set_plugboard(self,plugboard):       
        self.plugboard = plugboard
    def reset(self):
        opts = self.opts[0]
        self.__init__(opts[0],opts[1],opts[2],opts[3],opts[4])
    def apply_rotor(self,char,n,rotor):
        char = change(char,rotor,n)
        return change(char,n=-n)
    def reflecta(self,char):                       
        return change(char,self.reflector)
    def rotor_avanza(self):       
        if self.pos_ini[1] in self.muesca[self.rotores[1]]:            
            self.pos_ini[0] = change(self.pos_ini[0],n=1)       
            self.pos_ini[1] = change(self.pos_ini[1],n=1)       
        if self.pos_ini[2] in self.muesca[self.rotores[2]]:       
            self.pos_ini[1] = change(self.pos_ini[1],n=1)      
        self.pos_ini[2] = change(self.pos_ini[2],n=1)
    def apply_plugboard(self,char):       
        for i in self.plugboard:       
            if char == i[0]: 
                return i[1]            
            if char == i[1]: 
                return i[0]
        return char
    def cipher_letter(self,char):
        char = self.apply_plugboard(char)
        self.rotor_avanza()
        for i in range(2,-1,-1):
            n = ord(self.pos_ini[i]) - ord(self.pos_interna[i])
            char = self.apply_rotor(char,n,con_rotores[self.rotores[i]])          
        char = self.reflecta(char)             
        for i in range(3):       
            n = ord(self.pos_ini[i]) - ord(self.pos_interna[i])       
            char = self.apply_rotor(char,n,vuelta_rotores[self.rotores[i]])             
        char = self.apply_plugboard(char)       
        return char
    def cipher(self,text):
        output = ""
        for c in text:
            output += self.cipher_letter(c)
        return output
    def decipher(self,text):
        return self.cipher(text)

#Configuración Enigma default
plain = "ENUNLUGARDELAMANCHADECUYONOMBRENOQUIEROACORDARME"
expected = "ZADEMFNSUHIQOWUIVUOOMTLIDLVGKAHTEEAGNWJLTDVGHNQR"

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
texto_cifrado = enigma.cipher(plain)

print("##############")
print("    CIFRADO   ")
print("##############")
print(plain)
print(texto_cifrado)
print(normalize_text(expected))

print("\n##############")
print(" DESCIFRADO   ")
print("##############")
print(texto_cifrado)
enigma.reset()
texto_descifrado = enigma.decipher(texto_cifrado)
print(texto_descifrado)


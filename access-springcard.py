# -*- coding: utf-8 -*-
"""
Oct  2014
@author: pushou
read RFID from SPRINGCARD  Prox'N'Roll RFID Scanner
"""
from __future__ import print_function, division
from evdev import InputDevice, categorize, ecodes, list_devices
from datetime import datetime
import Adafruit_BBIO.GPIO as GPIO
import memcache

import re
import os
import time
import sys
from pytz import timezone
try:
    import cPickle as pickle
except:
    import pickle
import sqlite3 as lite


#def eteintLed():
#	GPIO.setup("P8_10", GPIO.OUT)
#	GPIO.setup("P8_11", GPIO.OUT)
#	GPIO.output("P8_10",GPIO.LOW)
#	GPIO.output("P8_11", GPIO.LOW)

def qwertyToAzerty(lettre):
	" simple transformation QWERTY 2 AZERTY due au renvoi en QWERTY du RFID"
        #print(lettre)
        Q_to_A = {
    	'A': 'Q',
    	'Q': 'A',
    	'Z': 'W',
    	'W': 'Z',
	}
        try:
           return Q_to_A[lettre]
        except KeyError:
           return(lettre)


def getAccessId(myevent):
    """ lecture de chaque caractere renvoye par le pseudo-ckavier du rfid :'code', 'sec', 'timestamp', 'type', 'usec', 'value'"""
    if myevent == "KEY_ENTER":
       return('FINSEQ')
    else:
       code = myevent[4:]
       t=qwertyToAzerty(code)
       print("myevent:{} code:{} extract:{}".format(myevent,code,t))
       return(t)
    

def storeRfid(rfid):
	"""store du RFDI vers une base SQLITE"""
	
	fmt = "%Y-%m-%d %H:%M:%S %Z%z"
	now_utc = datetime.now(timezone('UTC'))
	print(now_utc.strftime(fmt))

        # Europe/Paris time zone
	now_paris = now_utc.astimezone(timezone('Europe/Paris'))
	print(now_paris.strftime(fmt))

        try:
	    with  open('compteur.pkl', 'rb') as pkl_file:
                semaphs=pickle.load(pkl_file)
	        compteur=int(semaphs['compteur'])
	        etat=semaphs['etat']
	except IOError:
	    compteur=0
	    etat=0
	
	print('ecriture dans la base sqlite des infos timestamp: {} machine: {} rfid: {} compteur: {} etat {}'.format(now_paris,machine,rfid,compteur,etat))
        params = (now_utc,machine,rfid,int(compteur),int(etat),0)
	print(params)

           
        cur.execute("INSERT INTO RfidTrace VALUES(NULL,?, ?, ?, ?, ?, ?)", params)
	conn.commit()
	if etat == 1:
                shared.set('eteint', True)

	#cur.execute("select * from RfidTrace")
	#print([c for c in cur.fetchall()])

if __name__ == "__main__":	
    # recuperation des pseudo touches pressees par le Prox n Roll 
    pattern=re.compile('KEY_\w$',re.UNICODE)
    # Touche de fin d'envoi du code RFID
    pattern_entrer=re.compile('KEY_ENTER$',re.UNICODE)
    machine=os.uname()[1]

    shared = memcache.Client(['127.0.0.1:11211'], debug=0) 
    database = 'rfid.db'
    conn = lite.connect(database)
    cur = conn.cursor()
    
    cur.execute("CREATE TABLE  if not exists RfidTrace(ID INTEGER PRIMARY KEY AUTOINCREMENT,eventdate DATETIME default current_timestamp, Machine TEXT,Rfid TEXT ,compteur INTEGER, etat INTEGER, traite INTEGER)")

    devices = [InputDevice(fn) for fn in list_devices()]
    for dev in devices:
       print(dev)
    try:	
        dev=InputDevice('/dev/input/event1')
	print("reading /dev/input/event1")
    except OSError:
	print("pas de prox-n-roll")
	sys.exit()
    try:
        dev.grab() # verouille le pseudo clavier  a ce programme
    except IOError:
	print('programme deja lance par circus faite circus stop')
	pass
    liste_rfidcar=list()
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            data = categorize(event)
            if data.keystate == 1:
               key_lookup = ecodes.KEY.get(data.scancode)
               if key_lookup != "KEY_LEFTSHIFT" and key_lookup != "KEY_CAPSLOCK" :
                  rfidcar=getAccessId(key_lookup)
                  # Rupture sur une la touche ENTER et le code 28 qui caracterise la fin de l'envoi du RFID par 'le prox n roll'
                  if rfidcar and rfidcar != 'FINSEQ':
       	              liste_rfidcar.append(rfidcar)
     	          if rfidcar == 'FINSEQ':
                      rfid = "".join(liste_rfidcar)  
     	              if len(liste_rfidcar) >= 1:
     	                 storeRfid(rfid)
     	              liste_rfidcar=list()

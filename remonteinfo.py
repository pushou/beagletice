# -*- coding: utf-8 -*-
"""
Oct  2014
@author: pushou
push to tice server
RfidTrace(p_ID INTEGER PRIMARY KEY AUTOINCREMENT,eventdate DATETIME default current_timestamp, Machine TEXT,Rfid TEXT ,compteur INTEGER, traite BOOLEAN)
"""
from __future__ import print_function, division
from datetime import datetime
import sqlite3 as lite
import paramiko
from pytz import timezone

def readEvents():
    #cur.execute("SELECT * FROM RfidTrace where RfidTrace.traite=0 ")
    cur.execute("SELECT compteur,GROUP_CONCAT(DISTINCT Rfid) as Rfidlist FROM RfidTrace where traite=0 GROUP BY compteur")
    return(cur.fetchall())
    
def getPreviousCompteur(compteur):
    return(cur.execute("SELECT compteur FROM RfidTrace where compteur={}".format(compteur - 1)).fetchall())

def remonteVersBase(action,*rfid):
    print(action,*rfid)
    key = paramiko.RSAKey.from_private_key_file("id_rsa.conftice")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting")
    ssh.connect(hostname = 'my.conftice.org', username = 'beagle', pkey = key)

if __name__ == "__main__":

    try:
    	database = 'rfid.db'
    	conn = lite.connect(database)
	conn.row_factory = lite.Row
    	cur = conn.cursor()
    except lite.Error, e:
        print("Erreur {}:".format(e.args[0]))
        sys.exit(1)
    listofevents = readEvents()
    previousnumber=0
    for event in listofevents:
	# (49, u'8020CBA55A604,802BBD22226B04')
	# (51, u'8020CBA55A604')
	if len(event[1].split(',')) == 1:
  	     print("j'aime de {}".format(event[1]))
             remonteVersBase('php prod/test.php',event[1])	
	else:
	     # 
	     pc = getPreviousCompteur(event[0])
             if pc:
  	         print("je suis venu ici  de {}".format(event[1]))
	     else:
  	         print("nous avons eu un contact√s  {}".format(event[1]))


             print(event)
       


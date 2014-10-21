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
import sys
from pytz import timezone


def execSql(reqsql):
    try:
    	database = 'rfid.db'
    	conn = lite.connect(database)
	conn.row_factory = lite.Row
        cur = conn.cursor()
	print(reqsql)
	cur.execute(reqsql)
        return(cur.fetchall())
    except lite.Error, e:
        print("Erreur {}:".format(e.args[0]))
        sys.exit(1)

def readAllEvents():
    req="SELECT * FROM RfidTrace where traite=0"
    return execSql(req)
    
def readHereEvents():
    req="SELECT * FROM RfidTrace where traite={} and etat={}".format(0,0)
    return execSql(req)
    
def readLikeEvents():
    req="SELECT * FROM RfidTrace where traite={} and etat={}".format(0,1)
    return execSql(req)


def readMeetEvents():
    req="SELECT compteur,GROUP_CONCAT(DISTINCT Rfid),etat,traite as Rfidlist FROM RfidTrace \
where traite={} and etat={}  GROUP BY compteur".format(0,2)
    return execSql(req)


def readEvent(rfid):
    reqsql="SELECT * FROM RfidTrace  where traite=0 and rfid={}".format(rfid)
    return execSql(req)
    
def remonteVersBase(action,*rfid):
    print(action,*rfid)
    key = paramiko.RSAKey.from_private_key_file("id_rsa.conftice")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting")
    ssh.connect(hostname = 'my.conftice.org', username = 'beagle', pkey = key)

if __name__ == "__main__":

    previousnumber=0
    print("here events")
    for here_event in readHereEvents():
	print(here_event)
    print('#' * 50)
    print("like events")
    for like_event in readLikeEvents() :
	print(like_event)
    print('#' * 50)
    print("meet events")
    for meet_event in readMeetEvents():
	print(meet_event)
    print('#' * 50)
    print("all events")
    for all_event in readAllEvents() :
	print(all_event)
    print('#' * 50)


	#if len(event[1].split(',')) == 1:
  	#     print("j'aime de {}".format(event[1]))
        #     remonteVersBase('php prod/test.php',event[1])	
	#else:
	#     # 
	#     pc = getPreviousCompteur(event[0])
        #     if pc:
  	#         print("je suis venu ici  de {}".format(event[1]))
	#     else:
  	#         print("nous avons eu un contact√s  {}".format(event[1]))
        #print(event)
       


# -*- coding: utf-8 -*-
"""
Oct  2014
@author: pushou
push to tice server
"""
from __future__ import print_function, division
from datetime import datetime
import sqlite3 as lite
import paramiko
import sys
from pytz import timezone 
import logging


def execSql(reqsql):
    try:
    	database = '/home/bin/beagletice/rfid.db'
    	#database = 'rfid.db'
    	conn = lite.connect(database)
	conn.row_factory = lite.Row
        cur = conn.cursor()
	print(reqsql)
	cur.execute(reqsql)
        conn.commit()
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
    req="SELECT * FROM RfidTrace  where traite=0 and rfid={}".format(rfid)
    return execSql(req)

def getDateEvent(id):
    req="SELECT eventdate FROM RfidTrace where id='{}'".format(id)
    dateevent=execSql(req)	
    print(dateevent)
    dateevent=datetime.strptime(dateevent[0][0].split('.')[0],"%Y-%m-%d %H:%M:%S")
    paris=timezone('Europe/Paris')
    dateevent = paris.localize(dateevent)
    print('r'*50)
    print(dateevent)
    return dateevent
    
def modifyEvent(rfid):
    print(rfid)
    req="UPDATE RfidTrace SET traite={} where Rfid='{}'".format(1,unicode(rfid))
    return execSql(req)

def remonteVersTiceServer(action):
    print(action)
    key = paramiko.RSAKey.from_private_key_file(rsakey)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting")
    ssh.connect(hostname = ticeserver, username = username, pkey = key)
    stdin, stdout, stderr = ssh.exec_command(action)
    stdin.flush()
    #data = stdout.read.splitlines()
    print(stdout.readlines())
 


if __name__ == "__main__":

    #logging.basicConfig(level=logging.DEBUG)
    rsakey='/home/pouchou/id_rsa.conftice'
    ticeserver='my.ticeconf.org'
    username='beagle'
    fmt = "%Y-%m-%dT%X%z"

    now_utc = datetime.now(timezone('UTC'))
    # Europe/Paris time zone
    now_paris = now_utc.astimezone(timezone('Europe/Paris'))

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

    #print("all events")
    #for all_event in readAllEvents() :
    #	print(all_event)
    #print('#' * 50)

    dateheure=now_paris.strftime(fmt)
    print(dateheure)
    #remonteVersTiceServer('php prod/test.php False;echo $?',rsakey,readHereEvents())
    #remonteVersTiceServer('php prod/test.php True;echo $?',rsakey,readHereEvents())
    for group_of_meetrfids in readMeetEvents():
        #print(group_of_meetrfids[1])
        #print('%' * 50)
        rfidlist = ' '.join(group_of_meetrfids[1].split(','))
        listofrfid=rfidlist.split()  
        #dateheure=getDateEvent(listofrfid[0])
        pushcommand="php prod/link.php {} {} ".format(dateheure,rfidlist)
        print(pushcommand)
        remonteVersTiceServer(pushcommand)
        for rfid in listofrfid:
            modifyEvent(rfid)
    
       
    for group_of_likerfids in readLikeEvents():
        group_of_likerfids=list(group_of_likerfids)
        machine=group_of_likerfids[2]
        rfid=group_of_likerfids[3]
        print(machine,rfid)
        #dateheure=getDateEvent(rfid)
        pushcommand="php prod/join-like.php like {} {} {} ".format(dateheure,machine,rfid)
        print(pushcommand)
        remonteVersTiceServer(pushcommand)
        modifyEvent(rfid)

    for group_of_hererfids in readHereEvents():
        group_of_hererfids=list(group_of_hererfids)
        machine=group_of_hererfids[2]
        id=group_of_hererfids[0]
        rfid=group_of_hererfids[3]
        print("id: {}".format(id))
        dateheure=getDateEvent(id)
        pushcommand="php prod/join-like.php join {} {} {} ".format(dateheure,machine,rfid)
        print(pushcommand)
        remonteVersTiceServer(pushcommand)
        modifyEvent(rfid)


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
import time
from pytz import timezone,utc 
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

def modifyAllEvents():
    req="UPDATE RfidTrace SET traite={}".format(0)
    return execSql(req)


def readAllEvents():
    req="SELECT * FROM RfidTrace"
    return execSql(req)

if __name__ == "__main__":

    
    modifyAllEvents() 
    res=readAllEvents()
    for r in res:
       print(r)
    

# -*- coding: utf-8 -*-
"""
Oct  2014
@author: pushou
push to tice server
"""
from __future__ import print_function, division
from evdev import InputDevice, categorize, ecodes, list_devices
from datetime import datetime
import sqlite3 as lite
import paramiko

def readEvent():
    cur.execute("SELECT * FROM RfidTrace where RfidTrace.traite=0 ")
    print([c for c in cur.fetchall()])
    


if __name__ == "__main__":

    try:
    	database = 'rfid.db'
    	conn = lite.connect(database)
    	cur = conn.cursor()
    except lite.Error, e:
        print("Erreur {}:".format(e.args[0]))
        sys.exit(1)
    readEvent()


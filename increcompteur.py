# -*- coding: utf-8 -*-
"""
Oct  2014
@author: pushou
"""
from __future__ import print_function, division
import Adafruit_BBIO.GPIO as GPIO
import time
try:
   import cPickle as pickle
except:
   import pickle
 
GPIO.setup("P8_12", GPIO.IN)
 
try:
    pkl_file = open('compteur.pkl', 'rb')
    compteur=pickle.load(pkl_file)
except IOError:
    compteur=0
    pkl_file = open('compteur.pkl', 'wb')
    pickle.dump(compteur,pkl_file)
finally:
    pkl_file.close()

print('compteur au demarrage:{}'.format(compteur))
old_switch_state = 0
while True:
    new_switch_state = GPIO.input("P8_12")
    if new_switch_state == 1 and old_switch_state == 0 :
        compteur+=1
	with  open('compteur.pkl', 'wb') as pkl_file:
              pickle.dump(compteur,pkl_file)
        print('boutton presse. Compteur:{}'.format(compteur))
        time.sleep(0.5)
    old_switch_state = new_switch_state

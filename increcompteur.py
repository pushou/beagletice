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

def eteintLed():
    GPIO.output("P8_10",GPIO.LOW)
    GPIO.output("P8_11",GPIO.LOW)

# LED 
GPIO.setup("P8_10", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
# Poussoirs
GPIO.setup("P8_12", GPIO.IN)
GPIO.setup("P8_13", GPIO.IN)


 
etat=0
try:
    with open('compteur.pkl', 'rb') as pkl_file:
       semaphs=pickle.load(pkl_file)
       compteur=int(semaphs['compteur'])
       print(semaphs)
except IOError:
    compteur=0

# re-init
old_switch_state_12 = 0
old_switch_state_13 = 0
eteintLed()

print('compteur: {} etat: {}'.format(compteur,etat))

while True:
    new_switch_state_12 = GPIO.input("P8_12")
    new_switch_state_13 = GPIO.input("P8_13")

    if new_switch_state_12 == 1 and old_switch_state_12 == 0 :
        compteur+=1
	#print('boutton P8_12 presse. Compteur:{} etat:{}'.format(compteur,etat))
	if  GPIO.input("P8_11") == 0:
            GPIO.output("P8_11",GPIO.HIGH)
            GPIO.output("P8_10",GPIO.LOW)
	    etat=1
	elif GPIO.input("P8_11") == 1:
            GPIO.output("P8_11",GPIO.LOW)
	    etat=0
	print('etat: {} , compteur: {}'.format(etat,compteur))
	with  open('compteur.pkl', 'wb') as pkl_file:
		pickle.dump({"compteur":compteur,"etat":etat},pkl_file)
    old_switch_state_12 = new_switch_state_12
     
     
    if new_switch_state_13 == 1 and old_switch_state_13 == 0 :
        compteur+=1
	if GPIO.input("P8_10") == 0:
	    etat=2
            compteur+=1
            GPIO.output("P8_10",GPIO.HIGH)
            GPIO.output("P8_11",GPIO.LOW)
	elif GPIO.input("P8_10") == 1:
            GPIO.output("P8_10",GPIO.LOW)
	    etat=0
	print('etat: {} , compteur: {}'.format(etat,compteur))
	with  open('compteur.pkl', 'wb') as pkl_file:
	      pickle.dump({"compteur":compteur,"etat":etat},pkl_file)
    old_switch_state_13 = new_switch_state_13
     
    time.sleep(0.1)
     
     

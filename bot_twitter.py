#! /usr/bin/env python

from rutinas.varias import *
import datetime
import time
import random


#FoxCarlos
consumer_key = "VmXGmpbpFYmqIu1z3VkQw"
consumer_secret = "vG7aSMTFljzGBSLoL3VptqMeiGNywxiRLLnViHBHl8"
access_token = "23130430-n2iGA4d48vE7pzn3jRmKoxXJLerj4z9b0mcDMBQY"
access_token_secret = "IS8Z5ncXopr9JCQCEvPuYCsMUmxfaTU15SKwR9zkkg"

'''
#PyCondor
consumer_key = "xSSork9QJbmGh3lNCQEnw"
consumer_secret = "QLoeJHYWaVyWdQ1K8n3hkYGSZJIQ1QfARnP3P0OBw"
access_token = "489892321-a4wIMtnnD58ogcINXMQkwCgRewYoX8Z0JAZwLuVQ"
access_token_secret = "CMT6zyvFxXVVbH5LjinHnOWIfy39m6mDTHg3YlLDk"
'''


#Concina
consumer_key = "wz6LRrWGEj0cfOsSqNKLg"
consumer_secret = "JQUF9IFiFOpzjpTKYxsbKl5QV6o0baoD37fxFpBEE"
access_token = "36965560-Yk26t8CCvXxLyXgivJQBCXBfn1mPiawHYutSrU09Q"
access_token_secret = "OyEiXmMsx3zJD6sOU31GYzx78hgLbEp9JsRv3G2I"

t = tuiter(consumer_key, consumer_secret, access_token, access_token_secret)
tiempo = 61 
veces = 5
frases = ['saludos Amigos , quiero la de falcao #cdrxdirectv',
 'Hola Quiero la de falcao #cdrxdirectv', 
 'Mis Panas saludos desde Venezuela please la de falcao #cdrxdirectv', 
 'Quiero la camiseta de falcao #cdrxdirectv', 
 'Quiero la camiseta del Tigre #cdrxdirectv', 
 'Quiero esa remera #cdrxdirectv', 'Yo creo que ya gane #cdrxdirectv', 
 'Me duelen los dedos de tanto escribir #cdrxdirectv', 
 'Voy por la Camiseta #cdrxdirectv']

while True:
    f = datetime.datetime.now()
    fecha = f.strftime('%d/%m/%Y %H:%M')
    aleatorio = random.choice(frases)
    mensaje = '{0} mensaje nro{1} de hoy {2}'.format(aleatorio, veces, fecha)
    print mensaje
    t.enviar(mensaje)
    time.sleep(tiempo)
    veces = veces + 1

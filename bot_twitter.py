#! /usr/bin/env python

from rutinas.varias import *
import datetime
import time


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
for veces in range(10):
    f = datetime.datetime.now()
    fecha = f.strftime('%d/%m/%Y %H:%M:%S')
    mensaje = 'Hola @foxcarlos {0}'.format(fecha)
    t.enviar(mensaje)
    time.sleep(2)


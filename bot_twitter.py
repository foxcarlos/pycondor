#! /usr/bin/env python

from rutinas.varias import *
import datetime
import time

consumer_key = "VmXGmpbpFYmqIu1z3VkQw"
consumer_secret = "vG7aSMTFljzGBSLoL3VptqMeiGNywxiRLLnViHBHl8"
access_token = "23130430-n2iGA4d48vE7pzn3jRmKoxXJLerj4z9b0mcDMBQY"
access_token_secret = "IS8Z5ncXopr9JCQCEvPuYCsMUmxfaTU15SKwR9zkkg"

'''
consumer_key = "xSSork9QJbmGh3lNCQEnw"
consumer_secret = "QLoeJHYWaVyWdQ1K8n3hkYGSZJIQ1QfARnP3P0OBw"
access_token = "489892321-a4wIMtnnD58ogcINXMQkwCgRewYoX8Z0JAZwLuVQ"
access_token_secret = "CMT6zyvFxXVVbH5LjinHnOWIfy39m6mDTHg3YlLDk"
'''

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth)
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#api.update_status('Hola desde un BOT para Twitter y Facebook')

t = tuiter(consumer_key, consumer_secret, access_token, access_token_secret)
for veces in range(10):
    f = datetime.datetime.now()
    fecha = f.strftime('%d/%m/%Y %H:%M:%S')
    mensaje = 'Hola soy un BOT para Twitter :-P  #BOTLOL #TROPA {0}'.format(fecha)
    t.enviar(mensaje)
    time.sleep(2)


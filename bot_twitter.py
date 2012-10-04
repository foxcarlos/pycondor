#! /usr/bin/env python

from rutinas.varias import *


consumer_key = "xSSork9QJbmGh3lNCQEnw"
consumer_secret = "QLoeJHYWaVyWdQ1K8n3hkYGSZJIQ1QfARnP3P0OBw"
access_token = "489892321-a4wIMtnnD58ogcINXMQkwCgRewYoX8Z0JAZwLuVQ"
access_token_secret = "CMT6zyvFxXVVbH5LjinHnOWIfy39m6mDTHg3YlLDk"

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth)
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#api.update_status('Hola desde un BOT para Twitter y Facebook')

t = tuiter(consumer_key, consumer_secret, access_token, access_token_secret)
t.enviar('Hola desde un BOT para Twitter')


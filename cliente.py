#!/usr/bin/pyhton/env

import zmq
import os
import sys
import socket

s = socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
servSock = 'tcp://{0}:{1}'.format('10.121.3.60', '5556')
socket.connect(servSock)

nombrePC = s.gethostbyname_ex(s.gethostname())
comando = []
envioInicial = [nombrePC]
devuelve = []

while True:
    
    try:        
        if isinstance(comando, list):
            devuelve.extend(envioInicial)
            devuelve.extend(comando)
            #Se transforma en string
            #darFormatoDevuelve = ','.join(str(x) for x in devuelve)
            darFormatoDevuelve = str(devuelve)
        
        elif isinstance(comando, str):
            devuelve = comando
            darFormatoDevuelve = devuelve
        
        elif isinstance(comando, float):
            devuelve = str(comando)
            darFormatoDevuelve = devuelve

    except Exception as e:
        darFormatoDevuelve = e

    print('Enviando al servidor:{0}'.format(darFormatoDevuelve))
    socket.send(darFormatoDevuelve)
    recibido = socket.recv()
    print('Recibiendo desde el servidor:{0}'.format(recibido))
    
    if recibido:
        try:
            print('Ejecutando el EVAL')
            comando = eval(recibido)  # eval(recibido)
            print('comando contiene:'.format(str(comando)))
            devuelve = []
            darFormatoDevuelve = ''
        except Exception as e:
            print(e)
            comando = e
            devuelve = []
            darFormatoDevuelve = e
    else:
        comando = ''
        devuelve = []
        darFormatoDevuelve = ''


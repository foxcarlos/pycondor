#! /usr/bin/env python

import subprocess

carpeta = raw_input('Ingrese la carpeta a Matar:')
comandoLinux = "lsof | grep {0}".format(carpeta)

try:
    resultado = subprocess.check_output(comandoLinux, shell=True)
    lista2 = [f.split() for f in resultado.split('\n')]

    for j in lista2:
        pid = j[1]
        pidName = j[8]

        if pid.isdigit():
            print('Ejecutar KILL al proceso {0} '.format(pid))
            print('Nombre del Proceso {0} '.format(pidName))

            try:
                comandoKill = subprocess.Popen(['kill', '-9', pid], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            except:
                print('Error al Momento de realizar el kill -9 al pid:{0}'.format(pid))
        else:
            print('{0} No es un proceso PID'.format(pid))
except:
    print('No se encontro ningun proceso con ese nombre:{0}'.format(carpeta))


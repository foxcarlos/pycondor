#!/usr/bin/env python
'''
PyCondor es un modulo que permite vigilar una lista de uno o varios computadores
para saber si se encuentran activos en una red lan, esto es mediante el
comando fping de linux si no lo tienes instalado puedes hacerlo en debian o
ubuntu con el comando  #aptitude install fping, si usas Windows tambien existe
una descarga , probablemente lo conseguiras aqui http://fping.sourceforge.net/;
adicional a esto tambien es capaz de verificar el porcentaje de uso en disco
de los servidores que indiquemos que verifique, dandonos asi los alertas cuando se este alcanzando
un limite de uso del disco.
Para poder monitoriar el espacio en disco de un servidor remoto es necesario montarlo primero para
que pueda ser verificado el espacio ya que esto se realiza mediante el comando df de linux, ejemplo:
imaginemos que deseamos verificar el espacio en disco de un servidor windows que tiene un recurso
compartido llamado '//publico/hc2/',  para este caso es necesario montar el servidor bien sea
mediante el comando mount o directamente desde el fstab, luego de esto entonces procedemos a
colocarlo dentro del archivo de configuracion que es el lugar donde configuraremos todos nuestros
discos a verificar tal cual

Estos alertas se hacen enviando emails, twitts y sms  a numeros telefonicos

pycondor@gmail.com
shc21152115
'''
import subprocess
import sys
import os
import ConfigParser


'''
rut = os.path.abspath('desarrollo/python')
sys.path.append(rut)
from rutinas.varias import *
'''

sys.path.append('/home/administrador/desarrollo/python/')
from rutinas.varias import *


'''
Antes de inciar la primera vez este script es necesario agregar al path de python nuestra libreria
llamada varias.py que esta ubicada dentro del paquete rutinas, para agregar nuestra aplicacion al
path de python se puede hacer de varias maneras, la primera y la mas sencilla es utilizando el
metodo sys.path.append('ruta') dentro de nuestro Script Ej:

import sys
sys.path.append('/home/administrador/desarrollo/python/')

La otra forma de hacerlo es agregando nuestra aplicacion o script directamente al paht de python
desde la linea de comando mediante la sentencia "export" Ej:

export PYTHONPATH=$PYTHONPATH:/home/administrador/desarrollo/python

Esto tiene como desventaja que al cerrar la sesion de usuario esta ruta se perdera y debera
ejecutarse de nuevo cuando se inicie sesion. Si realmente deseamos que permanezca nuetro sistema
o script siempre en el pacht de python es necesario editar o crear en la raiz de /home/ un archivo
que esta por lo regular oculto llamado .bashrc, luego que lo editemos colocamos dentro lo siguiente:

Ej: nano /home/.bashrc
Copiar lo siguiente:

export PYTHONPATH=$PYTHONPATH:/home/administrador/desarrollo/python

Guardamos y listo ya tenemos nuetra aplicacion o script dentro de la ruta de python
'''
#si decides por utilizar la primera opcion descomenta la linea de abajo
#sys.path.append('/home/administrador/desarrollo/python/')


def unir_ruta_file(archivo):
    #Toma la Ruta Actual donde se encuentra el archivo .py actual
    ruta = os.path.abspath(os.path.dirname(sys.argv[0]))
    ruta_archivo = os.path.join(ruta, archivo)
    return ruta_archivo


def configuracion(seccion):
    contacs = unir_ruta_file("pycondor.conf")
    ini = ConfigParser.ConfigParser()
    ini.read(contacs)
    regresa = ini.items(seccion)
    return regresa


def notificar(msg):
    '''
    Metodo que permite enviar los mensajes al email,twitter,Log de archivo
    y telefono.
    Parametro Recibido:El Mensaje a Enviar
    Uso:notificar('Hola esto es una prueba')
    '''

    ruta_log = unir_ruta_file('log/condor.log')

    archivo = unir_ruta_file("pycondor.conf")
    ct_email = [ctem[1] for ctem in FileConf((archivo, 'opcion', 'consultar', 'email', '', ''))]
    ct_twitter = [cttw[1] for cttw in FileConf((archivo, 'opcion', 'consultar', 'twitter', '', ''))]
    ct_tlf = [telf[1] for telf in FileConf((archivo, 'opcion', 'consultar', 'telefono', '', ''))]
    fc = FileConfig(archivo)

    #enviar un log a un archivo ubicado en /pycondor/log/condor.log
    enviar_log(msg, ruta_log)

    #Buscar en el archivo .conf si esta activa la opcion NOTIFICAR=SI
    #Si la opcion esta activa proceder a notificar a todos los contactos
    env_msg = [telf[1] for telf in FileConf((archivo, 'opcion', 'consultar', 'notificar', '', ''))]
    if env_msg[0].upper() == 'SI':
        #enviar un mensaje por contacto de twitter
        for ct_t in ct_twitter:
            msg2 = ct_t + msg
            twitter_enviar('pycondor', msg2[0:140])

        #enviar un mensaje por contacto de email
        for ct_e in ct_email:
            enviar_email(ct_e, msg)

        #enviar un mensaje por contacto telefonico
        lista_telf = fc.opcion_consultar('SMS')
        sms = Sms()
        for cttf in ct_tlf:
            sms.enviar_mejorado(lista_telf, cttf, msg)


def vigilar_ip():
    '''    Metodo Vigilar obtiene una lista de las direcciones IP desde el Metodo
    obtener_config() ubicado en el paquete rutinas.varias que se importa al
    inicar la aplciacion, el metodo vigilar recorre la lista de Servidores
    y les hace fping para verfificar si estan disponibles, de no estarlo
    envia un mensaje via twitter,correo  a los responsables un  asi como
    tambien guarda el error en un log de archivo
    '''
    ruta_log = unir_ruta_file('log/condor.log')
    enviar_log('Iniciado vigilar_ip()', ruta_log)
    archivo = unir_ruta_file("pycondor.conf")
    lista_servidores = FileConf((archivo, 'opcion', 'consultar', 'SERVIDORES_ONLINE', '', ''))
    for servidor in lista_servidores:
        x = ['fping', servidor[1]]
        comando = subprocess.Popen(x, stderr=subprocess.PIPE, \
        stdout=subprocess.PIPE)
        salida = comando.stdout.read()
        if salida.find('unreachable') > 0:
            msg = ' %s *Atencion* El Servidor %s esta Fuera de Servicio' % \
            (str_fechahora(), servidor[0])
            print msg
            notificar(msg)


def vigilar_espacio():
    '''
    Metodo que permite obtener el espacio de los discos y unidades montadas
    para luego reportarlo, los discos a verificar se encuentran configurados
    en el archivo "cfg_diskspace.py" y para obtener el espacio dipoonible
    se llama al metodo "espacio_discos" que se encuentra en el paquete
    "rutinas.varias" , si por algun motivo uno de los discos que aparecen
    en la lista no puede ser verificado entonces tambien se envia un mensaje
    indicando que dicho(s) discos no se pudieron revisar
    '''

    ruta_log = unir_ruta_file('log/condor.log')
    enviar_log('Iniciado vigilar_espacio()', ruta_log)
    archivo = unir_ruta_file("pycondor.conf")
    discos_en_config = [disco[1] \
    for disco in FileConf((archivo, 'opcion', 'consultar', 'ESPACIO_DISCO', '', ''))]
    lista_espacio = espacio_disco()
    config_solo_nombre = []
    montados_solo_nombre = []

    for lista_disco in discos_en_config:
        config_solo_nombre.append(lista_disco)
        for discos_montados in lista_espacio:
            if len(discos_montados) > 0:
                montados_solo_nombre.append(discos_montados[0])
                if lista_disco == discos_montados[0]:
                    if float(discos_montados[4].replace('%', '')) >= 99:
                        msg = ' %s El Servidor %s alcanzo el limite Maximo de uso en Disco %s ' \
                        % (str_fechahora(), discos_montados[0], discos_montados[4])
                        notificar(msg)

    #Verificar si esta montado el disco o servidor y emitir alerta
    for disco_en_config in config_solo_nombre:
        if disco_en_config not in montados_solo_nombre:
            msg = ' %s Error no se pudo monitorear el disco (%s) es probable que no este montado \
            por tal motivo no se podran verificar' % (str_fechahora(), disco_en_config)
            notificar(msg)


if __name__ == '__main__':
    ruta_log = unir_ruta_file('log/condor.log')
    enviar_log('############ Proceso Iniciado ############', ruta_log)
    vigilar_ip()
    vigilar_espacio()
    #comando_remoto()
    enviar_log('############ Proceso Terminado ############', ruta_log)

#!/usr/bin/env python

import time
from daemon import runner
import logging
import os
import sys
import zmq
from rutinas import varias
from ConfigParser import SafeConfigParser

class demonioServer():
    def __init__(self):
        '''Metodo Init donde se inicializan
        todos los procesos para dar comienzo
        al Demonio'''

        #Para saber como se llama este archivo .py que se esta ejecutando
        archivo = sys.argv[0]  # Obtengo el nombre de este  archivo
        archivoSinRuta = os.path.basename(archivo)  # Elimino la Ruta en caso de tenerla
        self.archivoActual = archivoSinRuta

        self.nombreArchivoConf = 'pyloro.cfg'
        self.fc = SafeConfigParser()

        #Propiedades de la Clase
        self.archivoLog = ''

        #Ejecutar los Procesos Inciales
        self.configInicial()
        self.configDemonio()
        self.verificaDemonio()
        self.telefonoServidor()

    def configInicial(self):
        '''Metodo que permite extraer todos los parametros
        del archivo de configuracion pyloro.conf que se
        utilizara en todo el script'''

        #Obtiene Informacion del archivo de Configuracion .cfg
        self.ruta_arch_conf = os.path.dirname(sys.argv[0])
        self.archivo_configuracion = os.path.join(self.ruta_arch_conf, self.nombreArchivoConf)
        self.fc.read(self.archivo_configuracion)

        #Obtiene el nombre del archivo .log para uso del Logging
        # (RUTAS Y archivo.log son los campos del archivo .cfg)
        seccion = 'RUTAS'
        opcion = 'archivo_log'
        self.archivoLog = self.fc.get(seccion, opcion)

    def configDemonio(self):
        '''Configuiracion del Demonio'''

        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/{0}.pid'.format(self.archivoActual)
        self.pidfile_timeout = 5

    def configLog(self):
        '''Metodo que configura los Logs de error tanto el nombre
        del archivo como su ubicacion asi como tambien los
        metodos y formato de salida'''

        #Extrae de la clase la propiedad que contiene el nombre del archivo log
        nombreArchivoLog = self.archivoLog
        self.logger = logging.getLogger("{0}".format(self.archivoActual))
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)s--> %(asctime)s - %(name)s:  %(message)s", datefmt='%d/%m/%Y %I:%M:%S %p')
        handler = logging.FileHandler(nombreArchivoLog)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return handler

    def verificaDemonio(self):
        '''Obtengo del archivo de configuracion el  Nombre del Demonio
        con su IP y Puerto, Cada demonio que se ejecute debe estar en el
        archivo de configuracion con el nombre del archivo demonio y
        su respetiva direccion IP y Puerto al cual escucha,
        en la seccion Ej:
        [DEMONIOS]
        demonio1 = demonioserver1.py 
        demonio2 = demonioserver2.py 
 
        [DEMONIO1]
        ip_telefono = 127.0.0.1
        puerto_telefono = 9796
        puerto_adb_forward = 1111
        ip_demonio_zmq = 10.121.3.48
        puerto_demonio_zmq = 6000'''
        
        seccionDemonio = 'DEMONIOS'       
        #Verfico si existe la seccion DEMONIO en el .cfg
        if self.fc.has_section(seccionDemonio):
            #Si Existe listo el contenido de la Seccion
            #Y busco si esta este archivo .py configurado alli
            for demonios in self.fc.items(seccionDemonio):
                #Reccoro la lista y verifico si esta alli
                if self.archivoActual.lower() in demonios:
                    #Si lo consigue guardo el nombre de la seccion y el nombre del archivo
                    seccion, archivo = demonios
                    seccionFinal = seccion.upper()
                    #Ahora busco si existe dicha seccion
                    if self.fc.has_section(seccionFinal):
                        listaPar = []
                        for var, par in self.fc.items(seccionFinal):
                            listaPar.append(par)
                        
                        self.ip_telefono, \
                        self.puerto_telefono, \
                        self.puerto_adb_forward, \
                        self.ip_demonio_zmq, \
                        self.puerto_demonio_zmq, \
                        self.serial_telefono = listaPar
                    else:
                        msg = 'En el archivo de configuracion {0}\
                                no se encuentra configurada la seccion {1}\
                                en la que se hizo referencia en la seccion {2}'.format(self.nombreArchivo, seccionFinal, seccionDemonio)
                else:
                    msg = ' En el archivo de configuracion {0}\
                            Dentro de la Seccion [1]\
                            no se encuentra configurado este archivo {2}\
                            en ningun items u Opcion'.format(self.nombreArchivoConf, seccionDemonio, self.archivoActual)
        else:
            msg = 'No se encuentra la Seccion {0}\
                    en el archivo de configuracion {1}'.format(seccionDemonio, self.nombreArchivoConf)
            self.logger.error(msg.strip())
            sys.exit()

    def conectarDemonio(self):
        '''Metodo que permite conectar el demonio'''

        msg = ''
        #Se crea la instancia del contexto
        context = zmq.Context()
        #Se crea el socket pasandole como parametro respuesta (REP)
        self.socket = context.socket(zmq.REP)
        #Se asocia el socket a la IP y el puerto del servidor socket ej: tcp://127.0.0.1:5000
        
        ip = self.ip_demonio_zmq
        puerto = self.puerto_demonio_zmq

        servSock = 'tcp://{0}:{1}'.format(ip, puerto)
        try:
            self.socket.bind(servSock)
            msg = 'Conexion con el servidor {0} satisfactoria'.format(servSock)
            self.logger.info(msg)
        except:
            msg = 'No se pudo conectar con el Servidor Socket {0}\
            en el Archivo de Configuracion {1}, el demonio se detendra'.format(servSock, self.nombreArchivoConf)
            self.logger.error(msg)
            sys.exit()

    def run(self):
        '''Metodo que ejecuta el demonio y lo mantiene
        ejecutandose infinitamente hasta que se ejecute
        el comando:
        python demonioServer1.py stop'''

        self.reiniciarTelefono()
        self.conectarDemonio()
        self.conectarAndroid()
        contador = 0
        self.logger.info('Felicidades..!, Demonio Iniciado con Exito')

        while True:
            #todoBien en 0 significa que es Falso
            
            #El Mensaje es una Tupla que contiene el nro de telef y el Mensaje a Enviar
            msg = self.socket.recv()
            numero, mensaje = msg.split('^')            
            self.socket.send(todoBien)
            time.sleep(5)

app = demonioServer()
handler = app.configLog()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.daemon_context.files_preserve = [handler.stream]
daemon_runner.do_action()

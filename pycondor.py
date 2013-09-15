#! /usr/bin/env python
# -*- coding: utf-8 -*-

#pycondor@gmail.com
#shc21152115

import subprocess
import sys
import os
import ConfigParser
import logging
import time
from daemon import runner
import os
import zmq
import psutil

class pyCondor():
    def __init__(self):
        #Propiedades de la Clase
        self.archivoLog = ''
        self.tiempo = 10

        self.archivoCfg()
        self.configInicial()
        self.configDemonio()

    def archivoCfg(self):
        '''Inicializa y Obtiene Informacion del archivo de Configuracion .cfg'''

        self.nombreArchivoConf = 'pycondor.cfg'
        self.fc = ConfigParser.ConfigParser()
        
        self.ruta_arch_conf = os.path.dirname(sys.argv[0])
        self.archivo_configuracion = os.path.join(self.ruta_arch_conf, self.nombreArchivoConf)
        self.fc.read(self.archivo_configuracion)

    def configInicial(self):
        '''Metodo que permite extraer todos los parametros
        del archivo de configuracion pyloro.cfg que se
        utilizara en todo el script'''

        #Para saber como se llama este archivo .py que se esta ejecutando
        archivo = sys.argv[0]  # Obtengo el nombre de este  archivo
        archivoSinRuta = os.path.basename(archivo)  # Elimino la Ruta en caso de tenerla
        self.archivoActual = archivoSinRuta
        
        #Obtiene el nombre del archivo .log para uso del Logging
        seccion = 'RUTAS'
        opcion = 'archivo_log'
        self.archivoLog = self.fc.get(seccion, opcion)

    def configDemonio(self):
        '''Configuiracion del Demonio'''

        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/{0}.pid'.format(self.archivoActual)
        self.pidfile_timeout = 5
       
    def configLog(self):
        '''Metodo que configura los Logs de error tanto el nombre
        del archivo como su ubicacion asi como tambien los 
        metodos y formato de salida'''
        
        #Extrae de la clase la propiedad que contiene el nombre del archivo log
        nombreArchivoLog = self.archivoLog
        self.logger = logging.getLogger("DemonioPyCondor")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)s--> %(asctime)s - %(name)s:  %(message)s", datefmt='%d/%m/%Y %I:%M:%S %p')
        handler = logging.FileHandler(nombreArchivoLog)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return handler

    def enviarSocket(self, registros):
        '''Parametros 2: (tupla, string):
        (Registros, 'String:Nombre del Campo de la Tabla que se actualizara')
        Este Metodo recorre una lista de las personas que se le enviara el
        mensaje SMS de Respuesta para luego enviarla via ip por Socket a 
        (el o los) Servidores serverZMQ
        NOTA: Cuando se envia al ServidorZMQ este devuelve mediante self.socket.recv()
        ('1') si todo salio bien o ('0') en caso de fallar.'''

        for fila in registros:
            numero, sms = fila
            #mensaje = self.responder
            msg = '{0}^{1}'.format(numero, sms)

            #Se extrae y muestra en el .log solo una parte del mensaje
            self.logger.info(msg[:100])
            
            #Se enviar al servidor ZMQ para que envie el SMS
            self.socket.send(msg)
            
            #Se recibe un valor que verifica si llego bien el SMS
            # '1' si todo salio bien o '0' si no se pudo enviar el SMS
            msg_in = self.socket.recv()
            noEnviado, nombreServidor = msg_in.split(',')
            if not int(noEnviado):
                msg = '''Houston Tenemos un Problema con el Telefono:{0}, 
                no se pudo enviar el SMS desde el Servidor {1}'''.format(numero, nombreServidor)
                self.logger.warn(msg)

    def notificar(self, msg):
        '''
        '''
        listaMensajes = []
        for personal in self.fc.items('TELEFONO'):
            numero = personal[1]
            mensaje = (numero, msg)
            listaMensajes.append(mensaje)
            print(listaMensajes)
            self.logger.error(listaMensajes)
            #self.enviarSocket(listaMensajes)
    
    def guardarCfg(self):
        ''' Metodo que permite guadar los cambios que se le hacen al
        archivo de configuracion .cfg'''
        
        print('Entro  GuardarCfg, ahora se procede a abrir {0}'.format(self.nombreArchivoConf))
        time.sleep(48600)
        file = open(self.nombreArchivoConf, 'wb')
        print('Ya se Abrio el archivo y ahora se ejecutara el write')
        self.fc.write(file)
        print('Se Escribio, ahora e ejecutara el close')
        file.close()
        print('terminado')

    def vigilarIP(self):
        '''    Metodo Vigilar obtiene una lista de las direcciones IP desde el
        archivo de configuracion el metodo vigilar recorre la lista de Servidores
        y les hace fping para verfificar si estan disponibles, de no estarlo
        envia un mensaje via twitter,correo  a los responsables un  asi como
        tambien guarda el error en un log de archivo
        '''
        #self.fc = ConfigParser.SafeConfigParser()
        self.fc.read(self.archivo_configuracion)

        for servidor in self.fc.items('SERVIDORES_ONLINE'):
            x = ['fping', servidor[1]]
            comando = subprocess.Popen(x, stderr=subprocess.PIPE, \
            stdout=subprocess.PIPE)
            salida = comando.stdout.read()
            if salida.find('unreachable') > 0:
                if self.fc.get('NOTIFICAR', servidor[0]).upper() == 'SI':
                    msg = '*Atencion* El Servidor %s esta Fuera de Servicio'.format(servidor[0])
                    #Cambiar .cfg a no
                    self.fc.set('NOTIFICAR', servidor[0], 'no')
                    self.guardarCfg()
                    self.notificar(msg)
            else:
                if self.fc.get('NOTIFICAR', servidor[0]).upper() == 'NO':
                    msg = '*En hora buena* El Servidor %s esta en Servicio nuevamente'.format(servidor[0])
                    #Cambiar .cfg a si
                    self.fc.set('NOTIFICAR', servidor[0], 'si')
                    self.guardarCfg()
                    self.notificar(msg)

    def vigilarEspacio(self):
        '''
        Metodo que permite obtener el espacio de los discos y unidades montadas
        para luego reportarlo, los discos a verificar se encuentran configurados
        en el archivo ".cfg" y para obtener el espacio dipoonible,  si por algun 
        motivo uno de los discos que aparecen en la lista no puede ser verificado 
        entonces tambien se envia un mensaje indicando que dicho(s) discos no se 
        pudieron revisar
        '''
        #self.fc = ConfigParser.SafeConfigParser()
        self.fc.read(self.archivo_configuracion)

        msg = ''
        for disco in self.fc.items('ESPACIO_DISCO'):
            print(disco)
            ver = subprocess.Popen(['ls', disco[1]], 
                    stderr=subprocess.PIPE, 
                    stdout=subprocess.PIPE)
            
            #Se le hace un ls al directorio a ver si esta montado y tiene archivos
            #Si no esta vacio entonces se ejecuta psutil
            if ver.stdout.read():
                try:
                    porcentEspacioUso= psutil.disk_usage(disco[1]).percent
                except:
                    porcentEspacioUso = 0.0
            else:
                porcentEspacioUso = 0.0
                            
            if porcentEspacioUso >= 99:
                if self.fc.get('NOTIFICAR', disco[0]).upper() == 'SI':
                    msg = '*Atencion* El Servidor {0} alcanzo el limite Maximo de uso en Disco {1}%'.format(disco[0], 
                            porcentEspacioUso)
                    self.fc.set('NOTIFICAR', disco[0], 'no')
                    self.guardarCfg()
                    self.notificar(msg)
            else:
                if self.fc.get('NOTIFICAR', disco[0]).upper() == 'NO':
                    msg = '*En hora buena* El Servidor {0} ya tiene capacidad aceptable de uso en Disco {1}%'.format(disco[0], 
                            porcentEspacioUso)
                    self.fc.set('NOTIFICAR', disco[0], 'si')
                    self.guardarCfg()
                    self.notificar(msg)

            if porcentEspacioUso == 0:
                if self.fc.get('NOTIFICAR', disco[0]).upper() == 'SI':
                    msg = '*Atencion* No se pudo monitorear el disco {0}, es probable que no este montado'.format(disco[0])
                    self.fc.set('NOTIFICAR', disco[0], 'no')
                    self.guardarCfg()
                    self.notificar(msg)
            else:
                if self.fc.get('NOTIFICAR', disco[0]).upper() == 'NO':
                    msg = '*En Hora buena* Ya se pudo monitorear el disco {0}'.format(disco[0])
                    self.fc.set('NOTIFICAR', disco[0], 'si')
                    self.guardarCfg()
                    self.notificar(msg)

    def buscarServidoresZMQ(self):
        ''' Busca en el archivo de configuracion pyloro.cfg todos los 
        demonios servidores y devuelve una lista'''
        
        seccionDemonio = 'DEMONIOS'
        listaServidores= []

        if self.fc.has_section(seccionDemonio):
            for demonios in self.fc.items(seccionDemonio):
                seccion, archivo = demonios
                seccionFinal = seccion.upper()
                if self.fc.has_section(seccionFinal):
                    listaPar = []
                    for var, par in self.fc.items(seccionFinal):
                        listaPar.append(par)
                                   
                    ip_telefono, \
                    puerto_telefono, \
                    puerto_adb_forward, \
                    ip_demonio_zmq, \
                    puerto_demonio_zmq, \
                    serial_telefono = listaPar
                    
                    listaServidores.append(listaPar)
                else:
                    self.logger.error('No se encuentra en el archivo de configuracion la Seccion {0}'.format(seccionFinal))
        else:
            self.logger.error('No se cuentra en el archivo de configuracion la Seccion {0}'.format(seccionDemonio))
        return listaServidores

    def main(self):
        ''' '''
        self.logger.info('Proceso iniciado <Sistema de Monitoreo pyCondor>')
        self.vigilarEspacio()
        #self.vigilarIP()
        self.logger.info('Proceso Finalizado <Sistema de monitoreo pyCondor>')

    def zmqConectar(self):
        ''' Busca en el archivo de configuracion pyloro.cfg todos los 
        demonios servidores ZMQ y los conecta'''
        
        self.socket = ''
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        lista = self.buscarServidoresZMQ()
        for server in lista:
            ip_telefono, \
            puerto_telefono, \
            puerto_adb_forward, \
            ip_demonio_zmq, \
            puerto_demonio_zmq, \
            serial_telefono = server
            
            servSock = 'tcp://{0}:{1}'.format(ip_demonio_zmq, puerto_demonio_zmq)
            try:
                self.socket.connect(servSock)
                self.logger.info('Conexion Satisfactoria con el servidor {0}'.format(servSock))
            except:
                self.logger.error('Ocurrio un Error al momento de conectar al Socket Server {0}'.format(servSock))
    
    def run(self):
        ''' Este metodo es el que permite ejecutar el hilo del demonio'''

        self.zmqConectar()

        while True:
            #Es necesario volver a conectar cuando se reincia el telefono
            #Colcoar que si no logra a cpnexpn es xq prbablemente debe estarse reiniiando el telefpmnp, qie espere 2 minutos aprox
            #antes de volver a intentarlo
            
            self.logger.debug("Debug message")
            self.main()
            time.sleep(86400)

#Instancio la Clase
app = pyCondor()
handler = app.configLog()
daemon_runner = runner.DaemonRunner(app)

#Esto garantiza que el identificador de archivo logger no quede cerrada durante daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()


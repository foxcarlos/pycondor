'''
Created on 20/02/2009
@author: Chuidiang


Ejemplo de socket en python. Un servidor que acepta clientes.
Si el cliente envia "hola", el servidor contesta "pues hola".
Si el cliente envia "adios", el servidor contesta "pues adios" y
cierra la conexion.
El servidor no acepta multiples clientes simultaneamente.
'''

import socket
from threading import Thread
<<<<<<< HEAD
import os
=======

>>>>>>> 9fa74ff5e331d092054ee1acc9e07d00c5176f76

#Clase con el hilo para atender a los clientes.
#En el constructor recibe el socket con el cliente y los datos del
#cliente para escribir por pantalla

class Cliente(Thread):
    def __init__(self, socket_cliente, datos_cliente):
        Thread.__init__(self)
        self.socket = socket_cliente
        self.datos = datos_cliente
<<<<<<< HEAD
        self.ip, self.puerto = datos_cliente
=======
>>>>>>> 9fa74ff5e331d092054ee1acc9e07d00c5176f76
 
    # Bucle para atender al cliente.       
    def run(self):
        # Bucle indefinido hasta que el cliente envie "adios"
        seguir = True
    
        while seguir:
            # Espera por datos
<<<<<<< HEAD
            peticion = self.socket.recv(1000)
            r = raw_input('{0}: Cliente {1}:'.format(peticion, str(self.datos)))
            #os.system('clear')
=======

            peticion = self.socket.recv(1000)
            #print(peticion+'\n')

            r = raw_input('{0}: Cliente {1}:'.format(peticion, str(self.datos)))
                        
>>>>>>> 9fa74ff5e331d092054ee1acc9e07d00c5176f76
            re = r if r else 'no hagas nada'
            self.socket.send(re)

             

if __name__ == '__main__':
   # Se prepara el servidor
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind(("", 8002))
   server.listen(10)
   print "Esperando clientes..."
   
   # bucle para atender clientes
   while 1:
       
      # Se espera a un cliente
      socket_cliente, datos_cliente = server.accept()
      
      # Se escribe su informacion
      #print "conectado "+str(datos_cliente)
      
      # Se crea la clase con el hilo y se arranca.
      hilo = Cliente(socket_cliente, datos_cliente)
<<<<<<< HEAD
      os.system('clear')
=======
>>>>>>> 9fa74ff5e331d092054ee1acc9e07d00c5176f76
      hilo.start()
      


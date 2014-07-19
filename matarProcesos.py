import subprocess

#ruta = '/home/shc/'
#ruta = '/home/cgarcia/'
carpeta = raw_input('Ingrese la carpeta a Matar:')
rutaYCarpeta = carpeta
#rutaYCarpeta = ruta+carpeta

print(rutaYCarpeta)
#x = ["lsof", "|", "grep", rutaYCarpeta]
#x = ["lsof", "|", "grep", "Agenda"]
#x = ['lsof', '+D', rutaYCarpeta]
x = "lsof | grep {0}".format(carpeta)

try:
    comando = subprocess.check_output(x, shell=True)
    lista2 = [f.split() for f in comando.split('\n')]
    
    #comando = subprocess.Popen(x, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    #lista = [f for f in comando.stdout.xreadlines()]
    #lista2 = [j.split() for j in lista]
    
    for j in lista2:
        pid = j[1]
        if pid.isdigit():
            print('Ejecutar KILL al proceso {0} '.format(pid))
            comandoKill = subprocess.Popen(['kill', '-9', pid], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        else:
            print('No es un proceso PID')
except:
    print('No se encontro ningun proceso con ese nombre')


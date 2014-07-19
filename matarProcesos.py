import subprocess

ruta = '/home/shc/'
#ruta = '/home/cgarcia/'
carpeta = raw_input('Ingrese la carpeta a Matar:')
rutaYCarpeta = ruta+carpeta

print(rutaYCarpeta)
x = ["lsof", "|", "grep", rutaYCarpeta]
#x = ["lsof", "|", "grep", "Agenda"]
#x = ['lsof', '+D', rutaYCarpeta]

comando = subprocess.Popen(x, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
lista = [f for f in comando.stdout.xreadlines()]
lista2 = [j.split() for j in lista]

for j in lista2:
    pid = j[1]
    if pid.isdigit():
        print('Ejecutar KILL al proceso {0} '.format(pid))
        comandoKill = subprocess.Popen(['kill', '-9', pid], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    else:
        print('No es un proceso PID')

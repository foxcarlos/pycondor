import os

def buscar(ruta, extension):
    devuelto = []
    b = os.walk(ruta)
 
    for root, dirs, files in b:
        for archivos in files:
            if extension.lower() == os.path.splitext(archivos)[1].lower():
                rya = os.path.join(root, archivos)
                devuelto.append(rya)
    return devuelto

if __name__ == "__main__":
    ruta = '/media/publico/'
    extensiones = ['.mpg', '.mkv', '.mp3', '.mva', '.wmv', '.avi', '.flv', '.mp4', '.ogg']
    for ext in extensiones:
        lis = buscar(ruta, ext)
        for l in lis:
            print(l)
    
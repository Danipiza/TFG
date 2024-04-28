import os
import sys

directorio_script = os.path.dirname(os.path.abspath(__file__))

ruta_archivo = os.path.join(directorio_script, 'Pruebas','Binario')

# Construir la ruta al archivo en otra carpeta

# Abrir el archivo en modo de agregar ('a' para agregar al final)
"""with open(ruta_archivo, 'a') as archivo:
    # Escribir un número flotante en el archivo
    numero_flotante = 3.14159
    archivo.write(str(numero_flotante) + ', ')  # Agregar el número flotante seguido de un salto de línea"""


print(ruta_archivo)
archivos = os.listdir(ruta_archivo)

for arch in archivos:
    with open(os.path.join(ruta_archivo,arch), 'a') as archivo:        
        archivo.write('\n') 
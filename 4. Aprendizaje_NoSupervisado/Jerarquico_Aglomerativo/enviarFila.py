import sys
import os
import math
from mpi4py import MPI

def lee(archivo):

    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","Cluster", archivo+".txt")

    with open(path, 'r') as file:
        content = file.read()

    array = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')      
    for i in range(0, len(datos), 2):
        x = float(datos[i])
        y = float(datos[i + 1])

        array.append([x, y])

    #print("\n",array)        
    
    return array
 



archivo="100_2D"
C=7
poblacion=lee(archivo)

n=len(poblacion)
d=len(poblacion[0])

timeStart=MPI.Wtime()
fila=[-1]
for i in range(1,n):
    dist=0
    for a in range(d):
        dist+=(poblacion[0][a]-poblacion[i][a])**2  
    fila.append(math.sqrt(dist))

timeEnd=MPI.Wtime()
print("Tiempo de ejecucion: {}\n".format(timeEnd-timeStart))
print(fila)

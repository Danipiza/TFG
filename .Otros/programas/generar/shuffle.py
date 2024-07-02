import random
import sys
import os
import math


def lee(archivo):
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".Otros","ficheros","RedNeu", archivo+".txt")

    with open(path, 'r') as file:
        content = file.read()

    array = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')      
    for i in range(0, len(datos), 3):
        altura=float(datos[i])
        peso=float(datos[i+1])
        IMC=float(datos[i+2])

        array.append([altura,peso,IMC])

    #print("\n",array)        
    
    return array

def escribe(array, archivo):
    n=len(array)
    m=len(array[0])
    
    with open(archivo, 'w') as file:         
       
        for i in range(n-1):          
            file.write("[")
            for j in range(m-1):
                file.write(str(array[i][j])+", ")
            file.write(str(array[i][m-1])+"], ")

        file.write("[")
        for j in range(m-1):
            file.write(str(array[i][j])+", ")
        file.write(str(array[n-1][m-1])+"]")
        

        



def main():
    archivoEntrada="datos80"
    archivoSalida="datos80S.txt"
    #archivoEntrada="datos2042"
    #archivoSalida="datos2042S.txt"
    
    poblacion=lee(archivoEntrada)  

    random.shuffle(poblacion)

    escribe(poblacion, archivoSalida)

    #print(poblacion)


main()
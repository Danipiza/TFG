from mpi4py import MPI
import sys
import os

# COMPILAR
# py Normalizacion.py




def main():  	
    #poblacion=lee("datos80")
    #poblacion=lee("datos2042S")   
    poblacion=lee("10000_1_10D",10)   
    

    n=len(poblacion)
    d=len(poblacion[0])
    
    print("Tam. Poblacion: {}\t Num. Variables: {}\n".format(n,d))

    timeStart = MPI.Wtime()
    
    
    
    minsV=[float("inf") for _ in range(d)]
    maxsV=[float("-inf") for _ in range(d)]

    for x in poblacion:
        for a in range(d):
            if minsV[a]>x[a]: minsV[a]=x[a]
            elif maxsV[a]<x[a]: maxsV[a]=x[a]

    normalizacion=[]   
    for x in poblacion:
        ind=[]
        for a in range(d): # NORMALIZAR
            ind.append((x[a]-minsV[a])/(maxsV[a]-minsV[a]))
        normalizacion.append(ind)

    timeEnd = MPI.Wtime()

    

    print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))   

        



        
            
    #MPI.Finalize()

def normalizar_dato(val,m,M):
    return (val-m)/(M-m)


def lee(archivo, d):
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
        
    for i in range(0, len(datos), d):
        ind=[]
        for a in range(d):
            ind.append(float(datos[i+a]))
        
        """altura=float(datos[i])
        peso=float(datos[i+1])
        IMC=float(datos[i+2])"""

        """array.append([altura,peso,IMC])"""
        array.append(ind)

    #print("\n",array)        
    
    return array


   

main()

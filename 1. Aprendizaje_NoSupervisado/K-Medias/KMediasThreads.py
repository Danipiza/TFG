from mpi4py import MPI

import sys
import os
import time
import random

import threading
import multiprocessing 
import concurrent.futures

def lee(archivo):

    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","2.Cluster", archivo+".txt")

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


def leeArchivo(archivo):
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
        
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","Matrices", archivo+".txt")
    #print(path)
       
    filas=0
    columnas=0 
    M=[]
    
    try:        
        with open(path, 'r') as archivo: # modo lectura
            for linea in archivo:                                
                filas+=1
                columnas=0
                array = [] 
                numeros_en_linea = linea.split() # Divide por espacios                                              
                for numero in numeros_en_linea:
                    array.append(int(numero))
                    columnas+=1
                M.append(array)
                
    
    except FileNotFoundError:
        print("El archivo '{}' no existe.".format(archivo+".txt"))
    
    return M, filas, columnas
  
   


# Funcion para cada thread
def kmedias(id, barrier, k, poblacion, n, d, individuos,
            fin, asignacion, centroides, centroidesNuevos, indsCluster):    
    
    print("ID",id,individuos[0])
    

    """if id==0:
        time.sleep(1)
        fin[0]=True#multiprocessing.Array('b', [True])
        centroides[0][0]=1.0
        indsCluster[0]=1
    
    
    barrier.wait()
    if fin[0]: print("SIIIIII")
    print(centroides[0][0])
    print(indsCluster[0])"""
    

    while True: # Hasta que los centroides no cambien
        
        # 1. Fase de asginacion
        for i in range(individuos[0],individuos[1]):
            print(id,":",i)
            tmp=-1
            cluster=-1
            dist=float('inf')
            # Compara la distancia del individuo actual a cada centroide
            for j in range(k): 
                tmp=0.0
                for a in range(d):
                    tmp+=abs(poblacion[i][a]-centroides[j][a])
                
                if dist>tmp:
                    dist=tmp
                    cluster=j
            asignacion[i]=cluster # Asigna su cluster (el centroide mas cercano)
            
            for j in range(d): # Dimensiones
                centroidesNuevos[cluster][j]+=poblacion[i][j]
            indsCluster[cluster]+=1 # a

        # 2. Actualiza el los centros
        """for i in range(individuos[0],individuos[1]):
            for j in range(d): # Dimensiones
                centroidesNuevos[asignacion[i]][j]+=poblacion[i][j]
            #indsCluster[asignacion[i]]+=1 # a"""

        #time.sleep(2)
        barrier.wait()
        """print(id, end=": ")"""
        """if id==0:
            for x in indsCluster:
                print(x,end=" ")
            print("\n")"""


        # 3. Compara los centroides para ver si finaliza la ejecucion      
        if id==0:
            for i in range(k): 
                for j in range(d):  
                    if indsCluster[i]!=0: centroidesNuevos[i][j]/=indsCluster[i] 

            fin[0]=True
            for i in range(k):
                for j in range(d):
                    if centroides[i][j]!=centroidesNuevos[i][j]: 
                        fin[0]=False
                        break
            
            
            for x in centroidesNuevos:
                print("[", end="")
                for y in x:
                    print(y,end=", ")
                print("], ", end="")
            print()
            # Numero de inviduos en cada cluster
            for i in range(k):
                indsCluster[i]=0
            
            # Nuevos centroides: calculados con la media de todos los individuos del cluster
            for i in range(k):
                for j in range(d):
                    centroides[i][j]=centroidesNuevos[i][j]
                    centroidesNuevos[i][j]=0.0
            
            """for x in centroides:
                for y in x:
                    print(y,end=" ")
                print()
            print("\n")"""
            #centroidesNuevos=[[0 for _ in range(d)] for _ in range(k)]
        
        barrier.wait()
        #print(id,centroides[0][0])
        
        if fin[0]==True: break

    
    print("Termina Hilo:",id)

    return asignacion,centroides
    
    


def create_threads(numThreads,barrier, k, poblacion, n, d, modo,
                   fin, asignacion, centroides, centroidesNuevos, indsCluster):
    

    threads = []

    asig=[]

    tam=n//numThreads
    mod=n%numThreads
    izq=0
    for i in range(mod):
        asig.append([izq,izq+tam+1])
        izq+=tam+1

    for i in range(mod,numThreads):
        asig.append([izq,izq+tam])
        izq+=tam

    

    for i in range(numThreads):
        # print("MASTER",i)
        """thread = threading.Thread(target=multiply_row, args=(i, barrier, matrizA, matrizB, matrizC, n,m, asig[i]))
        threads.append(thread)
        thread.start()"""

        process = multiprocessing.Process(target=kmedias, args=(i, barrier, k, poblacion, n, d, asig[i], 
                                                                fin, asignacion, centroides, centroidesNuevos, indsCluster))
        threads.append(process)
        process.start()

    # Espera a que todos terminen 
    for thread in threads:
        thread.join()

def create_threads2(k, poblacion, n, d, modo, numHilos, 
                    centroides, centroidesNuevos, indsCluster):
    threads = []

    barrier = multiprocessing.Barrier(numHilos)

    asig=[]

    tam=n//numHilos
    mod=n%numHilos
    izq=0
    for i in range(mod):
        asig.append([izq,izq+tam+1])
        izq+=tam+1

    for i in range(mod,numHilos):
        asig.append([izq,izq+tam])
        izq+=tam
    
    
    
    if modo==0: 
        print("Distancia Manhattan con {} hilos".format(numHilos))
        for i in range(numHilos):
            process=multiprocessing.Process(target=ejecutaM, 
                                            args=(i, barrier, k, d, poblacion, asig[i], False,
                                                  centroides, centroidesNuevos, indsCluster))
            threads.append(process)
            process.start()
        
    else:
        print("Distancia Euclidea con {} hilos".format(numHilos))
    
    # Espera a que todos terminen 
    for thread in threads:
        thread.join()

def ejecutaM(id, barrier, k, d, poblacion, asig, fin,
                centroides, centroidesNuevos, indsCluster):
    
    """for x in indsCluster:        
        print(x,end=" ")
    print()"""
    for x in centroides:        
        for y in x:
            print(y,end=" ")
    print()

    if id==0:         
        time.sleep(1)

        centroides[0]=[1.0,0.0]
        
        #indsCluster[0]=1

    
    barrier.wait()

    """for x in indsCluster:        
        print(x,end=" ")
    print()"""
    for x in centroides:        
        for y in x:
            print(y,end=" ")
    print()

def main():       
    PRINT = False           # boolean.  Imprimir matrices

    k=3
    #poblacion=[[1,0], [2,0], [4,0], [5,0], [11,0], [12,0]]#, [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]]    
    poblacion=lee("100_2D")
    n=len(poblacion)
    d=len(poblacion[0])
    modo=0
    fin=multiprocessing.Array('b', [False])

    numThreads=4
    barrier = multiprocessing.Barrier(numThreads)
    
    dic={} 
    # TODO COMPARTIR
    centroides=[]   # centroides iniciales 
    for i in range(k):
        while True:
            rand=random.randint(0, n-1)
            if rand not in dic:
                centroides.append(multiprocessing.Array('f', poblacion[rand]))              
                dic[rand]=1
                break
    
    aux=[[-6.844407445048651, 1.9947857141278398], [5.866124093070791, -3.010404365517683], [1.050669959806287, -4.833642770794762]]
    #aux=[[2, 0], [5, 0], [12, 0]]
    for i in range(len(aux)):
        for j in range(len(aux[0])):
            centroides[i][j]=aux[i][j]


    centroidesNuevos=[]
    for _ in range(k):
        centroidesNuevos.append(multiprocessing.Array('f', [0.0 for _ in range(d)]))
    
    indsCluster=multiprocessing.Array('i', [0 for _ in range(k)] )
    asignacion=multiprocessing.Array('i', [-1 for _ in range(n)] )
    
    #timeStart = time.perf_counter()
    timeStart = MPI.Wtime()

    create_threads(numThreads,barrier, k, poblacion, n, d, modo,
                   fin, asignacion, centroides, centroidesNuevos, indsCluster)
    """create_threads2(k, poblacion, n, d, modo, numHilos, 
                    centroides, centroidesNuevos, indsCluster)"""
    
    
    #timeEnd = time.perf_counter()
    timeEnd = MPI.Wtime()


    print("Tiempo de ejecucion: {}s".format(timeEnd-timeStart))
    
    

            
        
if __name__ == "__main__":
    main()
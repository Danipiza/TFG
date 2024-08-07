from mpi4py import MPI
import sys
import os
import math

# COMPILAR
# py silhoutte.py




"""
Si=(bi-ai)/max(bi,ai)
coef= Sum(0,n,Si)/n

ai: Distancia promedio del punto i a todos los puntos del mismo cluster
bi: Distancia promedio del punto i a todos los puntos del cluster mas cercano
"""

# TODO
def leeAsignacion(directorio, archivo):    
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".Otros","ficheros",directorio, archivo+".txt")
    print(path)

    with open(path, 'r') as file:
        content = file.read()

    ind = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')  
   
    for i in range(len(datos)):
        
        ind.append(int(datos[i]))
        
        

    #print("\n",array)        
    
    return ind

def leePuntos(directorio,archivo, d):    
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".Otros","ficheros",directorio, archivo+".txt")

    with open(path, 'r') as file:
        content = file.read()

    array = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')  
        
    for i in range(0, len(datos), d):
        ind=[]
        for a in range(d):
            ind.append(float(datos[i+a]))
        
        array.append(ind)

    #print("\n",array)        
    
    return array


# Distancia Euclidea
def mainE():
    #asig=[0,0,1,1,2,2]
    #poblacion=[[1,0], [2,0], [4,0], [5,0], [11,0], [12,0]]#, [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]]    
    #clusters=[[1.5,0],[4.5,0],[11.5,0]]

    Clusters=4
    asig=leeAsignacion("Silhouette","1000_2D_A8") 
    
    poblacion=leePuntos("Cluster","1000_2D",2)
    clusters=leePuntos("Silhouette","1000_2D_C8",2)    
    
    
    n=len(poblacion)
    m=len(clusters)
    d=len(poblacion[0])

    timeStart=MPI.Wtime()



    asignaciones=[[] for _ in range(m)]
    for i in range(n):
        asignaciones[asig[i]].append(poblacion[i])

    timeStart=MPI.Wtime()

    coef=0
    for i in range(n):
        #print("Individuo:",i)
        # CALCULA a
        clust=asig[i]
        Ai=0
        for ind in asignaciones[clust]:
            tmp=0
            for a in range(d):
                tmp+=(poblacion[i][a]-ind[a])**2
            Ai+=math.sqrt(tmp)
        Ai/=len(asignaciones[clust])-1 # No cuenta asi mismo
        #print("Ai=",Ai)

        # CALCULA b

        # Cluster mas cercano
        clust=-1
        dist=float("inf")
        for j in range(m): 
            tmp=0
            for a in range(d):
                tmp+=(poblacion[i][a]-clusters[j][a])**2
            # No hace falta hacer raiz cuadrada para saber cual es menor
            if dist>tmp and j!=asig[i]: 
                dist=tmp
                clust=j
        #print("Cluster mas cercano=",clust)

        Bi=0
        for ind in asignaciones[clust]:
            tmp=0
            for a in range(d):
                tmp+=(poblacion[i][a]-ind[a])**2
            Bi+=math.sqrt(tmp)
        Bi/=len(asignaciones[clust])
        #print("Bi=",Bi,"\n")

        coef+=(Bi-Ai)/max(Ai,Bi)    
    coef/=n
    timeEnd=MPI.Wtime()
    print("coef=",coef)
    print("Tiempo de ejecucion:",(timeEnd-timeStart))
        



   





mainE()





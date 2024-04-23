from mpi4py import MPI
import sys
import os
import math

# COMPILAR
# py silhoutte.py


# TODO
def distancia_punto_a_punto(punto1, punto2):
    """Calcula la distancia euclidiana entre dos puntos."""
    suma_cuadrados = 0
    for i in range(len(punto1)):
        suma_cuadrados += (punto1[i] - punto2[i]) ** 2
    return suma_cuadrados ** 0.5

def distancia_promedio_a_punto(punto, puntos):
    """Calcula la distancia promedio de un punto a un conjunto de puntos."""
    total_distancias = 0
    for otro_punto in puntos:
        total_distancias += distancia_punto_a_punto(punto, otro_punto)
    return total_distancias / len(puntos)

"""Calcula el coeficiente de silhouette para un conjunto de puntos y sus clusters."""
def coeficiente_silhouette(puntos, asignacion):    
    num_puntos = len(puntos)
    silhouette_vals = []

    for i, punto in enumerate(puntos):
        cluster_actual = asignacion[i]
        a = distancia_promedio_a_punto(punto, [x for j, x in enumerate(puntos) if asignacion[j] == cluster_actual])

        b_values = []
        for j, otro_punto in enumerate(puntos):
            if asignacion[j] != cluster_actual:
                b_values.append(distancia_promedio_a_punto(punto, [x for k, x in enumerate(puntos) if asignacion[k] == asignacion[j]]))

        b = min(b_values) if b_values else 0
        silhouette_vals.append((b - a) / max(a, b))

    return sum(silhouette_vals) / num_puntos


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
    asig=leeAsignacion("Silhouette","100_2D_A8") 
    
    poblacion=leePuntos("Cluster","100_2D",2)
    clusters=leePuntos("Silhouette","100_2D_C8",2)    
    
    
    n=len(poblacion)
    m=len(clusters)
    d=len(poblacion[0])

    timeStart=MPI.Wtime()
    coef=coeficiente_silhouette(poblacion,asig)
    timeEnd=MPI.Wtime()

    print("coef=",coef)
    print("Tiempo de ejecucion:",(timeEnd-timeStart))
    
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





def silhouette_y_mejor(k, mejores, poblacion,asignacion):
    # Crear figura y ejes
    fig, axs = plt.subplots(1,2, figsize=(12, 6))
    
    # Definir los datos grafico 1
    x1 = [i for i in range(1, k + 1)]    
    #y2=mejores    

    # Graficar primer diagrama
    axs[0].plot(x1, mejores, 'ro', linestyle='-')
    axs[0].set_xlabel('Clusters')
    axs[0].set_ylabel('Fitness')
    axs[0].set_title('Diagrama de codo')
    axs[0].grid(True)


     # Definir los datos grafico 2
    colors = ['blue', 'red', 'green', 'black', 'pink', 'yellow', 'magenta', 'brown', 'darkgreen', 'gray', 'fuchsia',
            'violet', 'salmon', 'darkturquoise', 'forestgreen', 'firebrick', 'darkblue', 'lavender', 'palegoldenrod',
            'navy']
    n=len(poblacion)

    x2=[[]for _ in range(k)]
    y2=[[]for _ in range(k)]
    for i in range(n):
        x2[asignacion[i]].append(poblacion[i][0])
        y2[asignacion[i]].append(poblacion[i][1])
           
    # Graficar segundo diagrama
    for i in range(k):
        axs[1].scatter(x2[i], y2[i], color=colors[i])
    
    
    axs[1].set_xlabel('X')
    axs[1].set_ylabel('Y')
    axs[1].set_title('2D-Plot')


    plt.tight_layout()
    plt.show()

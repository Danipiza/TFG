"""import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI"""
import random
import os
import math
import time

import multiprocessing
import concurrent.futures

"""
El algoritmo de clustering, KMeans, tiene como objetivo dividir unos datos 
en un numero determindo de clusters (con su respectivo centroide).
"""

def main():
    # Numero de clusters ejecutados [1-k]
    k=5
    # poblacion=[[1,0], [2,0], [4,0], [5,0], [11,0], [12,0], [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]]    
    # 6000      1 generacion de puntos aleatorios
    # 6000_2    2 generaciones de puntos aleatorios
    # 6000_3    6 generaciones de puntos aleatorios
    # 100000_2D    6 generaciones de puntos aleatorios   
    poblacion=lee("100_2_2D")
    n=len(poblacion)
    d=len(poblacion[0])
    modo=0
    numHilos=4

    centroidesNuevos=[]
    for _ in range(k):
        centroidesNuevos.append(multiprocessing.Array('f', [0.0 for _ in range(d)]))
    
    ejecuta(k, poblacion, n, d, modo, numHilos, centroidesNuevos)

   


def ejecuta(k, poblacion, n, d, modo, numHilos, centroidesNuevos):
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

    # Inicializa centros de forma aleatoria
    # diccionario para almacenar los individuos ya seleccionados y no repetir centroides
    dic={} 
    # TODO COMPARTIR
    centroides=[]   # centroides iniciales 
    for i in range(k):
        while True:
            rand=random.randint(0, n-1)
            if rand not in dic:
                centroides.append(multiprocessing.Array('f', poblacion[rand]))
                #centroides.append(poblacion[rand])                
                dic[rand]=1
                break
    
    # COMPARTIR TODO
    # Numero de inviduos en cada cluster
    #indsCluster=[0 for _ in range(k)] 
    indsCluster= multiprocessing.Array('i', [0 for _ in range(k)] )
    # Nuevos centroides: calculados con la media de todos los individuos del cluster
    
    #centroidesNuevos=[[0 for _ in range(d)] for _ in range(k)]


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
    
    for x in centroidesNuevos:        
        for y in x:
            print(y,end=" ")
    print()
    
    


def compara_centros(self, a, b):
    n=len(a)
    for i in range(n):
        for j in range(self.d):
            if a[i][j]!=b[i][j]: return False
    
    return True

def ejecutaM(id, barrier, k, d, poblacion, individuos,fin,
             centroides, centroidesNuevos, indsCluster):
    print("Numero de hilo: {}, individuos= {}\n".format(id,individuos))
    print(poblacion[individuos[0]])
    
    """for x in centroides:
        for y in x:
            print(y,end=" ")        
    print"""
    
    for x in centroidesNuevos:
        for y in x:
            print(y,end=" ")
    print()
    """for x in indsCluster:
        print(x,end=" ")
    print()"""
    
    if id==0: 
        print("0: Cambiando valor")
        time.sleep(1)
        centroidesNuevos[0]=[1.0,0.0]
        
    barrier.wait()
    time.sleep(2)
    for x in centroidesNuevos:        
        for y in x:
            print(y,end=" ")
    print()
    
    """asignacion=[-1 for i in range(individuos[0],individuos[1])]

    while True: # Hasta que los centroides no cambien
        
        # 1. Fase de asginacion
        for i in range(individuos[0],individuos[1]):
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

        # 2. Actualiza el los centros
        for i in range(individuos[0],individuos[1]):
            for j in range(d): # Dimensiones
                centroidesNuevos[asignacion[i]][j]+=poblacion[i][j]
            indsCluster[asignacion[i]]+=1

        
        


        # 3. Compara los centroides para ver si finaliza la ejecucion      
        if id==0:
            for i in range(k): 
                for j in range(d):  
                    if indsCluster[i]!=0: centroidesNuevos[i][j]/=indsCluster[i] 

            fin=True
            for i in range(k):
                for j in range(d):
                    if centroides[i][j]!=centroidesNuevos[i][j]: 
                        fin=False
            
            # Numero de inviduos en cada cluster
            indsCluster=[0 for _ in range(k)] 
            # Nuevos centroides: calculados con la media de todos los individuos del cluster
            centroidesNuevos=[[0 for _ in range(d)] for _ in range(k)]
        
        barrier.wait()
        if fin==True: break

        centroides=centroidesNuevos # No finaliza y se actualizan los centroides

    return asignacion,centroides"""
    
    

# Misma ejecucion pero con euclidea
def ejecutaE(self):
    # Inicializa centros
    dic={}
    centroides=[]
    for i in range(self.k):
        while True:
            rand = random.randint(0, self.n - 1)
            if rand not in dic:
                centroides.append(self.poblacion[rand])                
                dic[rand] = 1
                break

    
    asignacion=[-1 for i in range(self.n)]
    while True:
        # Fase de asginacion
        for i in range(self.n):
            tmp=-1
            cluster=-1
            dist=float('inf')
            for j in range(self.k):
                tmp=self.euclidea(self.poblacion[i], centroides[j])
                if dist>tmp:
                    dist=tmp
                    cluster=j
            asignacion[i]=cluster

        # Actualiza el los centros
        indsCluster=[0 for _ in range(self.k)]
        centroidesNuevos=[[0 for _ in range(self.d)] for _ in range(self.k)]
        for i in range(self.n):
            for j in range(self.d):
                centroidesNuevos[asignacion[i]][j]+=self.poblacion[i][j]
            indsCluster[asignacion[i]]+=1

        if self.print==True:
            print("Poblacion:",self.poblacion)
            print("Centroides:",centroides)
            print("indsClusters:",indsCluster)
        for i in range(self.k): 
            for j in range(self.d):              
                centroidesNuevos[i][j]/=indsCluster[i]
        
        if self.print==True: print("Nuevos Centroides:",centroidesNuevos)
        if(self.compara_centros(centroides,centroidesNuevos)): break
        centroides=centroidesNuevos

    return asignacion,centroides

def manhattan(self,a,b):
    ret=0.0
    for i in range(len(a)):
        ret+=abs(a[i]-b[i])
    return ret

def euclidea(self, a,b):
        ret=0.0
        for i in range(len(a)):
            ret+=(a[i]-b[i])**2        
        
        return math.sqrt(ret)

"""
def GUI(k, mejor, fits, coefs, poblacion,asignacion):    
    # Create figure and axes
    #fig, axs = plt.subplots(2, 2, figsize=(18, 12), gridspec_kw={'width_ratios': [1, 2]})
    
    # Define data for the first plot
    x1 = [i for i in range(1, k + 1)]  
    # Define data for the second plot
    x2 = [i for i in range(2, k + 1)] 
    # Define data for the third plot
    colors = ['blue', 'red', 'green', 'black', 'pink', 'yellow', 'magenta', 'brown', 'darkgreen', 'gray', 'fuchsia',
            'violet', 'salmon', 'darkturquoise', 'forestgreen', 'firebrick', 'darkblue', 'lavender', 'palegoldenrod',
            'navy']
    n = len(poblacion)
    x3 = [[] for _ in range(k)]
    y3 = [[] for _ in range(k)]
    for i in range(n):
        x3[asignacion[i]].append(poblacion[i][0])
        y3[asignacion[i]].append(poblacion[i][1])


    # Crear la figura y GridSpec
    fig = plt.figure(figsize=(10, 6))
    gs = GridSpec(2, 2, figure=fig)

    # Grafico 1 (arriba a la izquierda)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(x1, fits, color='b', linestyle='-')
    ax1.scatter(mejor+1, fits[mejor], color='red')  # Punto rojo 
    ax1.set_xlabel('Clusters')
    ax1.set_ylabel('Fitness')
    ax1.set_title('Diagrama de codo')
    ax1.grid(True)

    # Grafico 2 (abajo a la izquierda)
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(x2, coefs, color='b', linestyle='-') 
    ax2.scatter(mejor+1, coefs[mejor-1], color='red')  # Punto rojo 
    ax2.set_xlabel('Clusters')
    ax2.set_ylabel('Coficiente')
    ax2.set_title('Davies Bouldin')
    ax2.grid(True)
    ax2.set_xlim(1, k)  # Expandir el eje x

    # Grafico 3 (a la derecha, ocupando las 2 filas)
    ax3 = fig.add_subplot(gs[:, 1])
    # Plot the third diagram in the first row, second column
    for i in range(k):
        ax3.scatter(x3[i], y3[i], color=colors[i])
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_title('Poblacion')
    
    
    plt.tight_layout() # Ajustar la disposición de los subplots    
    plt.show() # Mostrar los gráficos

def calcula_DB_mejor(DBs):
    n=len(DBs)
    val=DBs[0]
    ret=0

    for i in range(1,n):
        if val>DBs[i]: 
            val=DBs[i]
            ret=i

    return ret          

def davies_bouldin(poblacion, k, asignacion, centroides):
    ret=0.0
    n=len(poblacion)
    
    tmp=0.0
    distanciaProm=[0.0 for _ in range(k)]    
    indsCluster=[0 for _ in range(k)] # Numero de inviduos en cada cluster    
    for i in range(n):
        distanciaProm[asignacion[i]]+=distancia(centroides[asignacion[i]],poblacion[i])        
        indsCluster[asignacion[i]]+=1
    
    for i in range(k):
        distanciaProm[i]/=indsCluster[i]
    
    distanciaClust=[[0 for _ in range(k)] for _ in range(k)]
    for i in range(k-1):
        for j in range(i+1,k):
            tmp=distancia(centroides[i],centroides[j])
            distanciaClust[i][j]=tmp
            distanciaClust[j][i]=tmp
    
    tmp=0.0
    for i in range(k):
        maxVal=0.0
        for j in range(k):
            if i==j: continue
            tmp=(distanciaProm[i]+distanciaProm[j])/(distanciaClust[i][j])
            if tmp>maxVal: maxVal=tmp
        
        ret+=maxVal
    
    ret/=k
    return ret
       

def plot2D(poblacion,asignacion,k):
    #['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
    colors=['blue','red','green','black','pink','yellow','magenta','brown','darkgreen','gray','fuchsia','violet','salmon','darkturquoise','forestgreen','firebrick', 'darkblue','lavender','palegoldenrod','navy']
    n=len(poblacion)

    x=[[]for _ in range(k)]
    y=[[]for _ in range(k)]
    for i in range(n):
        x[asignacion[i]].append(poblacion[i][0])
        y[asignacion[i]].append(poblacion[i][1])
        
    for i in range(k):
        plt.scatter(x[i], y[i], color=colors[i])            
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('2D-Plot')
    
    plt.show()
"""
"""

La funcion de evaluacion calcula la suma al cuadrado de distancias (euclidianas) 
de cada individuo al centroide de su cluster"""
def evaluacion(poblacion, asignacion,centroides,imprime):
    n=len(poblacion)
    d=len(poblacion[0])
    
    tmp=0.0
    ret=0.0 # distancia Euclidea    
    for i in range(n):
        tmp=0.0
        for a in range(d): # Recorre sus dimensiones                
            tmp+=(poblacion[i][a]-centroides[asignacion[i]][a])**2            
        ret+=(tmp**2)
            
    if imprime==True: print("Valor calculado:",ret)
    return ret

def distancia(a,b):
    ret=0.0
    for i in range(len(a)):
        ret+=(a[i]-b[i])**2        
    
    return math.sqrt(ret)




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
 
    


    
if __name__ == '__main__':
    main()



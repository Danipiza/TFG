import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import random
import os
import math

# EJECUTAR
# mpiexec -np 5 python KMediasMPI_busqueda_E_2.py

# TIEMPO: (datos=100000.txt, k=6, times=8)
# Tiempo de ejecucion normal:           612.6053993999558s
# Tiempo de ejecucion MPI (4 workers):  171.3761496000682s    

# PARALELIZAR
    # 1. Dividir toda la poblacion y repartir entre los workers.
    # 2. Repartir partes de la poblacion para que vayan procesando y enviando.      


# Despues de implementar la 1ra idea, me he dado cuenta que es mas optimo
    # dividir la poblacion entre los workers. Ya que esta poblacion no cambia,
    # solo cambia la asignacion y los centros de los clustersm


def main():      
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    

    # DATOS A COMPARTIR
    poblacion=[]
    n=0
    maxClusters=0
    times=0
    d=0
    asignacion=[]
    centroides=[]

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1



    # Inicializa centros
    if myrank==MASTER:                 
        #a,n=leeArchivo("6000")      
        #poblacion=[[x] for x in a] 
        # 6000      1 generacion de puntos aleatorios
        # 6000_2    2 generaciones de puntos aleatorios
        # 6000_3    6 generaciones de puntos aleatorios
        # 100000_2D     1 generacion de puntos aleatorios
        poblacion=lee("100000_2D")            
        
        n=len(poblacion)        # Tamaño
        d=len(poblacion[0])     # Numero de dimensiones
        
        
        maxClusters=6
        times=8//numWorkers    
    
    pobTimeStart = MPI.Wtime()
    # Envia la poblacion entera a los workers
    poblacion=comm.bcast(poblacion, root=MASTER)
    pobTimeEnd = MPI.Wtime()
    
    if myrank==MASTER: 
        print("Tarda {}s en enviar la poblacion a {} workers\n".format((pobTimeEnd-pobTimeStart),numWorkers))

    # Envia el numero de individuos, a los workers
    n=comm.bcast(n, root=MASTER)
    # Envia el numero de dimensiones a los workers
    d=comm.bcast(d, root=MASTER)
    # Envia el numero de clusters a los workers
    maxClusters=comm.bcast(maxClusters, root=MASTER)
    # Envia el numero de veces que se repite, a los workers
    times=comm.bcast(times, root=MASTER)
    
        
    totalTimeStart = MPI.Wtime()
    
    
    if myrank==MASTER:  

        fits=[]
        mejores=[]
        centroidesMejores=[]     
        
        
        # Manda la poblacion entera no tiene que hacer nada aqui
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
            
                
        for numCluster in range(1,maxClusters+1):
            timeClustStart=MPI.Wtime()
            ret=float("inf")
            mejor=[]
            centroidesMejor=[]
            
            for _ in range(times):                
                # Centroides TODO se puede mejorar la asignacion
                for i in range(1,numWorkers+1):
                    dic={}
                    centroides=[]
                    for _ in range(numCluster):
                        while True:
                            rand = random.randint(0, n-1)
                            if rand not in dic:
                                centroides.append(poblacion[rand])                
                                dic[rand] = 1
                                break                              
                    comm.send(centroides,dest=i)            
                
                # Recibe
                for w in range(1,numWorkers+1):
                    # recibe de algun worker TODO
                    """fit = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)                        
                    source_rank=status.Get_source()""" 
                    fit = comm.recv(source=w)
                    # compara con el actual
                    if fit<ret:
                        ret=fit
                        # manda un mensaje pidiendo la asignacion y centroides
                        comm.send(-3,dest=w)
                        mejor = comm.recv(source=w)
                        centroidesMejor = comm.recv(source=w)                       
                    else: comm.send(-4,dest=w)                      
                    
                              
            timeClustEnd=MPI.Wtime()
            print("Cluster (k)= {}, mejor valor= {}.\nTiempo de Ejecucion: {}".format(numCluster,ret,(timeClustEnd-timeClustStart)))        
            
            fits.append(ret)
            mejores.append(mejor)
            centroidesMejores.append(centroidesMejor)

        
        totalTimeEnd = MPI.Wtime()
        print("Tiempo de ejecucion total: {}".format(totalTimeEnd-totalTimeStart))


        DBs=[davies_bouldin(poblacion, i, mejores[i-1], centroidesMejores[i-1]) for i in range(2,maxClusters+1)]    
        dbMejor=calcula_DB_mejor(DBs)
        
        GUI(maxClusters, dbMejor+1, fits,DBs,poblacion,mejores[dbMejor+1])
    
    else : # WORKER        

        asignacion=[-1 for i in range(n)]
        for numCluster in range(1, maxClusters+1):
            for _ in range(times):
                
                centroidesNuevos=[]
                centroides=comm.recv(source=MASTER)               

                while True: # Hasta que los centroides no cambien
                    
                    # 1. Fase de asginacion
                    for i in range(n):
                        tmp=-1
                        cluster=-1
                        dist=float('inf')
                        # Compara la distancia del individuo actual a cada centroide
                        for j in range(numCluster): 
                            tmp=0.0
                            for a in range(d):
                                tmp+=(poblacion[i][a]-centroides[j][a])**2    
                            tmp=math.sqrt(tmp)    
                            if dist>tmp:
                                dist=tmp
                                cluster=j
                        asignacion[i]=cluster # Asigna su cluster (el centroide mas cercano)

                    # 2. Actualiza el los centros
                        
                    # Numero de inviduos en cada cluster
                    indsCluster=[0 for _ in range(numCluster)] 
                    # Nuevos centroides: calculados con la media de todos los individuos del cluster
                    centroidesNuevos=[[0 for _ in range(d)] for _ in range(numCluster)]
                    for i in range(n):
                        for j in range(d): # Dimensiones
                            centroidesNuevos[asignacion[i]][j]+=poblacion[i][j]
                        indsCluster[asignacion[i]]+=1


                    # Para cada cluster divide entre su numero de individuos (en cada dimension)
                    for i in range(numCluster): 
                        for j in range(d):  
                            if indsCluster[i]!=0: centroidesNuevos[i][j]/=indsCluster[i]    

                    # 3. Compara los centroides para ver si finaliza la ejecucion
                    if(compara_centros(d, centroides,centroidesNuevos)): break
                    centroides=centroidesNuevos # No finaliza y se actualizan los centroides
                
                comm.send(evaluacion(poblacion, asignacion,centroides), dest=MASTER)
                a=comm.recv(source=MASTER)
                if a==-3:
                    comm.send(asignacion, dest=MASTER)
                    comm.send(centroides, dest=MASTER)
                
                
        exit(0)
    
def compara_centros(d, a, b):
    n=len(a)
    for i in range(n):
        for j in range(d):
            if a[i][j]!=b[i][j]: return False
    
    return True




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

"""La funcion de evaluacion calcula la suma al cuadrado de distancias (euclidianas) 
de cada individuo al centroide de su cluster"""
def evaluacion(poblacion, asignacion,centroides):
    n=len(poblacion)
    d=len(poblacion[0])
    
    tmp=0.0
    ret=0.0 # distancia Euclidea    
    for i in range(n):
        tmp=0.0
        for a in range(d): # Recorre sus dimensiones                
            tmp+=(poblacion[i][a]-centroides[asignacion[i]][a])**2            
        ret+=(tmp**2)
            
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
 


main()


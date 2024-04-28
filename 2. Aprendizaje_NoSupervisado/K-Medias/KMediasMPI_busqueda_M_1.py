import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import random
import os
import math

# EJECUTAR
# mpiexec -np 5 python KMediasMPI_busqueda_M_1.py

# TIEMPO: (datos=100000.txt, k=6, times=5)
# Tiempo de ejecucion normal:           251.5163483999204s    
# Tiempo de ejecucion MPI (4 workers):  63.64491190004628s      

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
        # 6000_1_2D     1 generacion de puntos aleatorios
        # 6000_2_2D     2 generaciones de puntos aleatorios
        # 6000_3_2D     6 generaciones de puntos aleatorios
        # 100000_2D     1 generacion de puntos aleatorios
        poblacion=lee("100_1_2D")            
        
        n=len(poblacion)        # Tamaño
        d=len(poblacion[0])     # Numero de dimensiones
        
        
        maxClusters=8
        times=20

        """dic={}
        centroides=[]
        for i in range(k):
            while True:
                rand = random.randint(0, n-1)
                if rand not in dic:
                    centroides.append(poblacion[rand])                
                    dic[rand] = 1
                    break"""        
    
    # Envia el numero de clusters a los workers
    maxClusters=comm.bcast(maxClusters, root=MASTER)
    # Envia el numero de veces que se repite, a los workers
    times=comm.bcast(times, root=MASTER)
    # Envia el numero de dimensiones a los workers
    d=comm.bcast(d, root=MASTER)
    
    # Envia los centroides iniciales 
    # centroides=comm.bcast(centroides, root=MASTER)
    
    totalTimeStart = MPI.Wtime()
    
    
    if myrank==MASTER:  

        fits=[]
        mejores=[]
        centroidesMejores=[]     
        
        # ENVIA LA PARTE DE LA POBLACION QUE CADA worker ----------------------- 
        #   VA A PROCESAR EN TODA LA EJECUCION ---------------------------------
        # Numero de elementos para cada worker       
        tamProc=n//numWorkers
        # Si mcd(n,numWorkers)!=numWorkers, 
        #   es porque habra algunos workers con 1 elemento mas
        modulo=n%numWorkers
        # Punteros
        izq=0
        der=tamProc+1

        # Hay al menos 1 elemento para cada worker.
        if tamProc>=1:  
            for i in range(1, modulo+1):    
                comm.send(poblacion[izq:der],dest=i)
                # update
                izq+=tamProc+1
                der+=tamProc+1
            der-=1
            # Hay algun worker con 1 elemento menos que los demas.
            for i in range(modulo+1,numWorkers+1):
                comm.send(poblacion[izq:der],dest=i)
                # update
                izq+=tamProc
                der+=tamProc    
        # No hay al menos 1 elemento para cada worker
        #   los workers que se queden sin elemento se finalizan.
        else:
            for i in range(1, modulo+1):  
                comm.send(poblacion[izq], dest=i)   
                # update
                izq+=1							
            for i in range(modulo+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)                  
            # Se reduce el numero de workers
            numWorkers-=numWorkers-modulo
        
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
            
                
        for numCluster in range(1,maxClusters+1):
            timeClustStart=MPI.Wtime()
            ret=float("inf")            
            for _ in range(times):
                
                # Centroides
                dic={}
                centroides=[]
                for i in range(numCluster):
                    while True:
                        rand = random.randint(0, n-1)
                        if rand not in dic:
                            centroides.append(poblacion[rand])                
                            dic[rand] = 1
                            break                
                centroides=comm.bcast(centroides, root=MASTER)

                # Procesa datos, termina cuando los centros no cambian
                while True:
                    centroidesNuevos=[[0 for _ in range(d)] for _ in range(numCluster)]
                    indsCluster=[0 for _ in range(numCluster)]

                    for _ in range(numWorkers):
                        datos = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)                        
                        source_rank=status.Get_source() 
                        """print("Recibe de ", source_rank)"""
                        # Suma los centroides
                        for i in range(numCluster):
                            for j in range(d):
                                centroidesNuevos[i][j]+=datos[i][j]
                        # Suma los indices
                        datos = comm.recv(source=source_rank, tag=tag,status=status)
                        for i in range(numCluster):
                            indsCluster[i]+=datos[i]                     
                                
                    # Calcula los nuevos clusters            
                    for i in range(numCluster): 
                        for j in range(d):              
                            centroidesNuevos[i][j]/=indsCluster[i]
                    
                    """print("Cluster", len(centroidesNuevos))"""
                    # FINALIZA
                    if(compara_centros(d, centroides,centroidesNuevos)): 
                        for i in range(1,numWorkers+1):
                            comm.send(END_OF_PROCESSING,dest=i)
                        asignacion=[]
                        for i in range(1,numWorkers+1):
                            datos = comm.recv(source=i)
                            for x in datos:
                                asignacion.append(x)
                        break

                    # CONTINUA: Envia los nuevos centroides 
                    for i in range(1,numWorkers+1):
                        comm.send(centroidesNuevos,dest=i)
                    centroides=centroidesNuevos
                
                tmp=evaluacion(poblacion, asignacion,centroides)
                if tmp<ret:
                    ret=tmp
                    mejor=asignacion
                    centroidesMejor=centroides

            #print("Cluster (k)=",numCluster)            
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
        guardar_en_txt(mejores[dbMejor+1],"100_1_2D.txt")
    
    else : # WORKER
        poblacion=comm.recv(source=0)
        if poblacion==-2: exit(0)
        n=len(poblacion)


        for numCluster in range(1, maxClusters+1):
            for _ in range(times):
                
                centroides=comm.bcast(centroides, root=MASTER)

                while True:
                    # POBLACION NO CAMBIA, CUANDO TODOS LOS workers ENVIEN UN MENSAJE AL
                    #   master DICIENDO QUE LOS CENTROIDES NO HAN CAMBIADO, EL master ENVIA
                    #   UN MENSAJE PARA QUE LOS workers DEVUELVAN LA ASIGNACION FINAL

                    # FASE DE ASIGNACION            
                    asignacion=[]
                    for i in range(n):
                        tmp=-1
                        cluster=-1
                        dist=float('inf')
                        for j in range(numCluster):                    
                            tmp=0.0      
                            for a in range(d):
                                tmp+=abs(poblacion[i][a]-centroides[j][a])     
                                                
                            if dist>tmp:
                                dist=tmp
                                cluster=j
                        asignacion.append(cluster)

                    # ACTUALIZAN CENTROS
                    indsCluster=[0 for _ in range(numCluster)]
                    centroidesNuevos=[[0 for _ in range(d)] for _ in range(numCluster)]
                    for i in range(n):
                        for j in range(d):
                            #print("(WORKER {}), Cluster={}, ASIG[{}]={}".format(myrank, numCluster, i, asignacion[i]))
                            centroidesNuevos[asignacion[i]][j]+=poblacion[i][j]
                        indsCluster[asignacion[i]]+=1
                    comm.send(centroidesNuevos, dest=0)
                    comm.send(indsCluster, dest=0)
                    
                    # Reciben los nuevos centroides            
                    centroides=comm.recv(source=0)
                    if centroides==END_OF_PROCESSING:
                        comm.send(asignacion, dest=0)
                        #exit(0)
                        break
                
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
 

def guardar_en_txt(a, archivo):
    with open(archivo, 'w') as txt:
        # Convierte cada elemento en el array a cadena y luego únelos con espacios
        linea = ' '.join(map(str, a))
        # Escribe la línea en el archivo
        txt.write(linea)

main()


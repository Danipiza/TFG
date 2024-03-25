import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import random
import os
import math

import copy

# EJECUTAR
# mpiexec -np 5 python aglomerativeMPI_E.py

# PARALELIZAR
    # 1. Dividir toda la poblacion y repartir entre los workers.
    # 2. Repartir partes de la poblacion para que vayan procesando y enviando.      


# Despues de implementar la 1ra idea, me he dado cuenta que es mas optimo
    # dividir la poblacion entre los workers. Ya que esta poblacion no cambia,
    # solo cambia la asignacion y los centros de los clustersm

# TODO 
# DIVIDIR CALCULO DE DISTANCIA PARA LA FILA
# Con 13 workers da otro resultado, 5 cluster optimo


def main():      
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    

    # DATOS A COMPARTIR
    poblacion=[]
    n=0
    d=0
    C=0
    
    M=[]



    izq=0
    der=0

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1



    # Inicializa centros
    if myrank==MASTER:       
        #poblacion=[[1,0], [2,0], [4,0], [5,0], [11,0], [12,0]]#, [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]]#, [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]
        
        # 6000      1 generacion de puntos aleatorios
        # 6000_2    2 generaciones de puntos aleatorios
        # 6000_3    6 generaciones de puntos aleatorios
        # 100000_2D     1 generacion de puntos aleatorios
        poblacion=lee("300_6_2D")            
        
        n=len(poblacion)        # Tamaño
        d=len(poblacion[0])     # Numero de dimensiones
        C=7
        
        
    # Envia la poblacion entera a los workers
    poblacion=comm.bcast(poblacion, root=MASTER)   
    # Envia el numero de individuos a los workers
    n=comm.bcast(n, root=MASTER)
    # Envia el numero de dimensiones a los workers
    d=comm.bcast(d, root=MASTER)
    # Envia el numero de clusters a los workers
    C=comm.bcast(C, root=MASTER)
    
    
    totalTimeStart = MPI.Wtime()
    
    
    if myrank==MASTER:  
        print("\nEjecutando inic Matriz{}x{} (con calculo de distancias)\n".format(n,n))
        # Info TODO OPTIMIZAR?
        # Array de clusters
        clusters=[[i] for i in range(n)]        
        # Array con los centros de cada cluster
        clustersCentros=[x for x in poblacion]  

        asignacion=[[] for _ in range(C)]
        centroides=[[] for _ in range(C)]

        workers=[i for i in range(1,numWorkers+1)]
        # Diccionario con las asignaciones
        filasAsig={}
        workerFilas=[[] for _ in range(numWorkers)]
        
        # FASE1: Inicializa Matriz de distancias
        
        # ENVIA LA PARTE DE LA POBLACION QUE CADA worker ----------------------- 
        #   VA A PROCESAR EN TODA LA EJECUCION ---------------------------------
        # Numero de elementos para cada worker                      
        m=n//2
        tuplas=[[i,n-i-1] for i in range(m)]
        tam=m//numWorkers
        # Si mcd(n,numWorkers)!=numWorkers, 
        #   es porque habra algunos workers con 1 elemento mas
        modulo=m%numWorkers
        cont=0        

        # Hay al menos 1 elemento para cada worker.
        if tam>=1:  
            for i in range(1, modulo+1):
                izq=[]
                der=[]
                for _ in range(tam+1):  
                    izq.append(tuplas[cont][0])
                    der.append(tuplas[cont][1]) 

                    filasAsig[tuplas[cont][0]]=i
                    filasAsig[tuplas[cont][1]]=i                    
                                      
                    cont+=1
                der.reverse()
                for x in izq:
                    workerFilas[i-1].append(x)
                for x in der:
                    workerFilas[i-1].append(x)
                comm.send(izq,dest=i)
                comm.send(der,dest=i)
                
            # Hay algun worker con 1 elemento menos que los demas.
            for i in range(modulo+1,numWorkers+1):
                izq=[]
                der=[]
                for _ in range(tam):  
                    izq.append(tuplas[cont][0])
                    der.append(tuplas[cont][1])

                    filasAsig[tuplas[cont][0]]=i
                    filasAsig[tuplas[cont][1]]=i 
                    cont+=1
                der.reverse()
                for x in izq:
                    workerFilas[i-1].append(x)
                for x in der:
                    workerFilas[i-1].append(x)
                comm.send(izq,dest=i)
                comm.send(der,dest=i)   
        # No hay al menos 1 elemento para cada worker
        #   los workers que se queden sin elemento se finalizan.
        else:
            for i in range(1, modulo+1):  
                izq=[]
                der=[] 
                izq.append(tuplas[cont][0])
                der.append(tuplas[cont][1])
                
                workerFilas[i].append(izq[0])            
                workerFilas[i].append(der[0])

                filasAsig[tuplas[cont][0]]=i
                filasAsig[tuplas[cont][1]]=i 
                cont+=1
                    
                comm.send(izq,dest=i)
                comm.send(der,dest=i)							
            for i in range(modulo+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)                  
            # Se reduce el numero de workers
            numWorkers-=numWorkers-modulo
        
        
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------

        



        # FASE2:         
        # Repite hasta que solo haya "C" clusters
        for numCluster in range(1,n): 
            min=float("inf")
            w=-1
            
            aux=-1
            
            for i in range(numWorkers, 0, -1):
                data=comm.recv(source=workers[i-1])
                if data==END_OF_PROCESSING:                    
                    aux=workers[i-1]
                elif(data<min): # TODO CAMBIAR
                    min=data
                    w=i

            if aux!=-1:
                workers.pop(aux)
                numWorkers-=1

            # Envia al worker con menor, para que le envie sus datos
            for i in workers:
                comm.send(w,dest=i)
            
            # Recibe del worker los indices
            data=comm.recv(source=w)
                                
            # Envia a los otros workers el indice de la columna que tienen que eliminar
            for i in workers:            
                comm.send(data[0],dest=i)
                comm.send(data[1],dest=i)


            c1=data[0]
            c2=data[1]
            # Junta los cluster mas cercanos
            for x in clusters[c2]:
                clusters[c1].append(x)                
            clusters.pop(c2) 

            # Actualiza centro            
            tmp=[0.0 for _ in range(d)]
            for x in clusters[c1]:
                for y in range(d):
                    tmp[y]+=poblacion[x][y]
            for x in range(d):
                tmp[x]/=len(clusters[c1])
            clustersCentros[c1]=tmp
            clustersCentros.pop(c2)

            a = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)                        
            source_rank=status.Get_source() 
            if a==END_OF_PROCESSING:
                workers.remove(source_rank)
                numWorkers-=1


            

            for i in workers:
                comm.send(clustersCentros[c1],dest=i)

            
            if n-numCluster-1<C:                
                asignacion[n-numCluster-1]=copy.deepcopy(clusters)
                centroides[n-numCluster-1]=copy.deepcopy(clustersCentros)
            


        totalTimeEnd = MPI.Wtime()
        print("Tiempo de ejecucion total: {}\n".format(totalTimeEnd-totalTimeStart))

        asignacionesFin=[[-1 for _ in range(n)] for _ in range(C)]
        for numClust in range(C):
            for i in range(numClust+1):
                for j in asignacion[numClust][i]:
                    asignacionesFin[numClust][j]=i

        fits=[evaluacion(poblacion, asignacionesFin[i],centroides[i]) for i in range(C)]

        DBs=[davies_bouldin(poblacion, i, asignacionesFin[i-1], centroides[i-1]) for i in range(2,C+1)]    
        dbMejor=calcula_DB_mejor(DBs)
        
        GUI(C, dbMejor+1, fits,DBs,poblacion,asignacionesFin[dbMejor+1])
    
    else : # WORKER
        izq=comm.recv(source=MASTER)
        der=comm.recv(source=MASTER)
        
        tamIzq=len(izq)
        tamDer=len(der)
        
        cont=0
        M=[]
        
        # Izquierda
        for i in range(izq[0],izq[tamIzq-1]+1):
            tmp=[-1 for _ in range(i+1)]  
            for j in range(i+1,n):
                aux=0.0
                for a in range(d):
                    aux+=(poblacion[i][a]-poblacion[j][a])**2     
                tmp.append(math.sqrt(aux))
            M.append(tmp)

        # Derecha
        for i in range(der[0],der[tamDer-1]+1):
            tmp=[-1 for _ in range(i+1)]  
            for j in range(i+1,n):
                aux=0.0
                for a in range(d):
                    aux+=(poblacion[i][a]-poblacion[j][a])**2     
                tmp.append(math.sqrt(aux))
            M.append(tmp)

        #comm.send(M, dest=MASTER)

        # PADRE PROCESA
        filas=[]
        for x in izq:
            filas.append(x)
        for x in der:
            filas.append(x)
        tam=tamIzq+tamDer
        filasDic={}
        for i in range(tam):
            filasDic[filas[i]]=i


        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------

        # FASE 2
        for numCluster in range(1,n): 
            c1,c2=None,None
            distMin=float("inf")            
            for i in range(tam):
                for j in range(filas[i]+1,n):
                    if distMin>M[i][j]: 
                        distMin=M[i][j]
                        c1=i
                        c2=j 
            if c1==None: 
                distMin=float("inf")
                # TODO
                """print("W2 eliminado")
                comm.send(END_OF_PROCESSING,dest=MASTER)
                exit(0)"""                
            else:
                c1=filas[c1] #Cambia porque las filas estan divididas
            
            # Envia su minimo            
            comm.send(distMin, dest=MASTER)
            # Recibe confirmacion si tiene que enviar los indices
            w=comm.recv(source=MASTER)
            if w==myrank: 
                comm.send([c1,c2],dest=MASTER)

            c1=comm.recv(source=MASTER)
            c2=comm.recv(source=MASTER)
            #data=comm.recv(source=MASTER)

            
            
            #if data==myrank:
            if c2 in filasDic:                    
                # Elimina columna c2 de M            
                for row in M:                
                    del row[c2]

                tmp=filasDic[c2]
                # Elimina fila c2 de M
                if filasDic[c2]!=len(M): 
                    M.pop(filasDic[c2])
                    filasDic.pop(c2)
                
                
                # Actualiza indices
                
               
                filas.pop(tmp)
                tam-=1
                for i in range(tmp,tam): 
                    filasDic.pop(filas[i])               
                    filas[i]-=1
                    filasDic[filas[i]]=i
                    
              

                if tam==0:
                    comm.send(END_OF_PROCESSING, dest=MASTER)
                    exit(0)
                else:
                    comm.send(1,dest=MASTER)
            else:
                # Elimina columna c2 de M
                for row in M:
                    del row[c2]

                # Actualiza indices                      
                i=0
                while i<tam:
                    if filas[i]>c2: break
                    i+=1
                for i in range(i,tam):
                    filasDic.pop(filas[i])               
                    filas[i]-=1
                    filasDic[filas[i]]=i 
                
              
            
            
            # Elimina cluster c2
            del poblacion[c2]
            # Cambia cluster c1
            clustNew=comm.recv(source=MASTER)
            poblacion[c1]=clustNew
            
            # ACTUALIZA COLUMNAS (1 SOLO)  
            # SE TIENE QUE HACER EN TODAS LAS FILAS             
            for i in range(tam):
                if M[i][c1]==-1: break # TODO Se puede mejorar?
                aux=0.0
                for a in range(d):
                    aux+=(poblacion[filas[i]][a]-poblacion[c1][a])**2             
                M[i][c1]=math.sqrt(aux)         
            
            n-=1
            # ACTUALIZA FILA
            if w==myrank:                
                # for i in range(c1+1,len(M[filasDic[c1]])):
                for i in range(c1+1,n):                    
                    aux=0.0
                    for a in range(d):
                        aux+=(poblacion[i][a]-poblacion[c1][a])**2             
                    M[filasDic[c1]][i]=math.sqrt(aux)
                
                
            

            
            
            




        
    
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
 


main()


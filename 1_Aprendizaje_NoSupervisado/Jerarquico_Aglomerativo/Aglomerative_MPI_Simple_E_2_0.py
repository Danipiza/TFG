import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import random
import os
import math

import copy

# EJECUTAR
# mpiexec -np 4 python Aglomerative_MPI_Simple_E_2_0.py


# Similar a la mejora 2_1, solo que con otra tipo de logica de programación.
"""
Algoritmo de clustering jerarquico aglomerativo. Con mejoras MPI 

El Master se encarga de dividir las filas de manera optima, los Workers calculan las distancias
y se establece el proceso de comunicacion Master - Workers.

En esta mejora, el proceso que actualiza la fila divide el trabajo del calculo de distancias
entre los otros Workers. 

- Distancia entre clusters: Simple
- Distancia entre individuos: Euclidea
    
Una vez terminado el algoritmo, la interfaz muestra la asignacion de los individuos, con mejor
indice de Davie-Bouldin, ademas de imprimir el coeficiente, y el diagrama de codo.
"""



def main():      
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    

    # -------------------------------------------------------------------------------------
    # --- DATOS A COMPARTIR ---------------------------------------------------------------
    # -------------------------------------------------------------------------------------

    
    poblacion=[]    # Conjunto de clusters
    n=0             # Tamaño de la poblacion
    d=0             # Numero de dimensiones
    C=0             # Numero de clusters que almacena para la impresion    
    
    M=[]            # Conjunto de filas para cada worker



    # -------------------------------------------------------------------------------------
    # --- Init MPI. -----------------------------------------------------------------------
    # -------------------------------------------------------------------------------------
        
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    

    # -------------------------------------------------------------------------------------
    # --- INIT PROBLEMA -------------------------------------------------------------------
    # -------------------------------------------------------------------------------------

    # Inicializa centros
    if myrank==MASTER:       
        #poblacion=[[1,0], [2,0], [4,0], [5,0], [11,0], [12,0]]#, [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]]#, [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]        
        archivo="100000_2D"
        C=1
        poblacion=lee(archivo)
        #procesar=[40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]
        poblacion=poblacion[0:200]
        print("\nEjecutando archivo: {}, numero de clusters para la GUI: {}, distancia: Euclidea\n".format(archivo, C))           
        
        n=len(poblacion)        
        d=len(poblacion[0])   

        print("Tam. Poblacion {}".format(n))  
        
    clustersCentros=[[x] for x in poblacion]    
        
    # Envia la poblacion entera a los workers
    poblacion=comm.bcast(poblacion, root=MASTER)   
    clustersCentros=comm.bcast(clustersCentros, root=MASTER)   
    # Envia el numero de individuos a los workers
    n=comm.bcast(n, root=MASTER)
    # Envia el numero de dimensiones a los workers
    d=comm.bcast(d, root=MASTER)
    # Envia el numero de clusters a los workers
    C=comm.bcast(C, root=MASTER)
    

    # -------------------------------------------------------------------------------------
    # --- ALGORITMO -----------------------------------------------------------------------
    # -------------------------------------------------------------------------------------
    
    timeStart=MPI.Wtime()
    
        
        
    if myrank==MASTER:  
        k=C-1
        asig=[[] for _ in range(C)]
        centr=[[] for _ in range(C)]
    
        
        # Array de clusters
        clusters=[[i] for i in range(n)]            
        # Array con los centros de cada cluster
          

        asignacion=[[] for _ in range(C)]
        centroides=[[] for _ in range(C)]

        workers=[i for i in range(1,numWorkers+1)]
        workersDist=[]
        # Diccionario con las asignaciones
        filasAsig={}
        workerFilas=[[] for _ in range(numWorkers)]
        
        # FASE1: Inicializa Matriz de distancias
        

        # -------------------------------------------------------------------------------------
        # --- ENVIA LA PARTE DE LA POBLACION QUE CADA worker ----------------------------------
        # -------------------------------------------------------------------------------------
        
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
                if i==1 and n%2==1:
                    workerFilas[i-1].append(tuplas[cont][0])
                    filasAsig[tuplas[cont][0]]=1
                    cont+=1
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
        
        
        
        cont=0
        # Repite hasta que solo haya "C" clusters
        for _ in range(C, n):
            
            for i in range(1,numWorkers+1):
                comm.send(0, dest=i)
            
        #while(True): 
            # -------------------------------------------------------------------------------------
            # --- RECIBE MINIMOS ------------------------------------------------------------------
            # -------------------------------------------------------------------------------------        
            
            minW=-1
            minD=float("inf")
            
            for i in workers:
                data=comm.recv(source=i)                
                if minD>data:
                    minD=data
                    minW=i
                
                         
            # ENVIA EL ID DEL worker CON EL MINIMO
            for i in workers:
                comm.send(minW,dest=i)

            # RECIBE LA FILA Y COLUMNA DEL WORKER
            c1=comm.recv(source=minW)
            c2=comm.recv(source=minW)
            
            # ENVIA A TODOS LOS WORKERS LOS INDICES Y EL ID DEL worker CON LA FILA A ELIMINAR
            #wC1=filasAsig[c1]
            wC2=filasAsig[c2]
            for i in workers:
                comm.send(c1,dest=i)
                comm.send(c2,dest=i)
                #comm.send(wC1,dest=i)
                comm.send(wC2,dest=i)
            
            for i in workersDist:
                comm.send(filasAsig[c1],dest=i)
                comm.send(c1,dest=i)
                comm.send(c2,dest=i)
                

           
            # ACTUALIZA INDICES
            n-=1
            for i in range(c2,n): 
                filasAsig[i]=filasAsig[i+1]
            filasAsig.pop(n)  # elimina la ultima fila pues esta duplicada (ya se ha movido)
            
            
            # JUNTA LOS CLUSTERS
            for x in clusters[c2]:
                clusters[c1].append(x)            
            
            # Actualiza centro    
            for x in clustersCentros[c2]:
                clustersCentros[c1].append(x)                
            
            del clusters[c2]        # ELIMINA EL CLUSTER DE LA FILA ELIMINADA
            del clustersCentros[c2] # ELIMINA LOS CENTROS DE LA FILA ELIMINADA
            
                       
            
            
            # RECIBE DEL worker QUE ELIMINA FILAS POR SI YA NO TIENE MAS FILAS QUE ELIMINAR
            data=comm.recv(source=wC2)
            if data==-1:                        
                workers.remove(wC2)
                workersDist.append(wC2) 
                
                comm.send(0,dest=wC2)
                comm.send(filasAsig[c1],dest=wC2)
                comm.send(c1,dest=wC2)
                comm.send(c2,dest=wC2)
                

            

            # ENVIA EL NUEVO CLUSTER
            for i in workers:
                comm.send(clustersCentros[c1],dest=i)
            
            for i in workersDist:                
                comm.send(clustersCentros[c1],dest=i)
            
            
            # PARA LA GUI y comprobar el mejor numero de clusters
            if n<C+1:                 
                asig[k]=copy.deepcopy(clusters)
                centr[k]=copy.deepcopy(clustersCentros)        
                k-=1


            """if cont==16:
                print("MASTER llega", filasAsig[c1])
                exit(1)"""

            comm.recv(source=filasAsig[c1])
            
            
            cont+=1
        
        # Bucle principal (si C=1 solo se lo envia a uno)
        for i in workers:            
            comm.send(END_OF_PROCESSING, dest=i)  

        # Bucle calculando distancias
        for i in range(1,numWorkers+1):
            comm.send(END_OF_PROCESSING, dest=i)           

        timeEnd=MPI.Wtime()
        print("Tiempo de ejecucion: {}\n".format(timeEnd-timeStart))

       

        """for x in asig:
            print("Len=",len(x))#,x)"""
        
        """n=len(poblacion)
        asignacionesFin=[[-1 for _ in range(n)] for _ in range(C)]
        for numClust in range(C):
            for i in range(numClust+1):
                for j in asig[numClust][i]:
                    asignacionesFin[numClust][j]=i
            
        centroidesFin=[] 
        for numClust in range(C):
            tmpClust=[]
            for j in range(numClust+1):
                m=len(centr[numClust][j])
                tmp=[0 for _ in range(d)]
                for x in centr[numClust][j]:
                    for a in range(d):
                        tmp[a]+=x[a]
                for a in range(d):
                    tmp[a]/=m
                tmpClust.append(tmp)                      

            centroidesFin.append(tmpClust)    
        

        fits=[evaluacion(poblacion, asignacionesFin[i],centroidesFin[i]) for i in range(C)]

        DBs=[davies_bouldin(poblacion, i, asignacionesFin[i-1], centroidesFin[i-1]) for i in range(2,C+1)] 
        
        dbMejor=calcula_DB_mejor(DBs)


        GUI(C, dbMejor+1, fits,DBs,poblacion, asignacionesFin[dbMejor+1])"""

        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------

    
    else : # WORKER
        
        
        # ----------------------------------------------------------------------
        # --- RECIBE LOS INDICES DE LAS FILAS QUE VA A MANEJAR -----------------
        # ----------------------------------------------------------------------
        izq=comm.recv(source=MASTER)
        der=comm.recv(source=MASTER)
        
        tamIzq=len(izq)
        tamDer=len(der)
        tam=tamIzq+tamDer

        # ----------------------------------------------------------------------
        # --- CALCULA SU MATRIZ ------------------------------------------------
        # ----------------------------------------------------------------------
        M=[]                
        for i in range(izq[0],izq[-1]+1):
            fila=[-1 for _ in range(i+1)]
            for j in range(i+1,n):
                dist=0
                for a in range(d):
                    dist+=(poblacion[i][a]-poblacion[j][a])**2  

                fila.append(math.sqrt(dist))
            M.append(fila)

        for i in range(der[0],der[-1]+1):
            fila=[-1 for _ in range(i+1)]
            for j in range(i+1,n):
                dist=0
                for a in range(d):
                    dist+=(poblacion[i][a]-poblacion[j][a])**2  

                fila.append(math.sqrt(dist))
            M.append(fila)
        

        # ----------------------------------------------------------------------
        # --- GESTION DE FILAS -------------------------------------------------
        # ----------------------------------------------------------------------

        filas=[]
        for x in izq:
            filas.append(x)
        for x in der:
            filas.append(x)
        tam=tamIzq+tamDer
        filasDic={}
        for i in range(tam):
            filasDic[filas[i]]=i                

        

        
        cont=0
        while(True):

            data=comm.recv(source=MASTER)
            if data==END_OF_PROCESSING: break

            # --------------------------------------------------------------------
            # --- BUSCA MINIMOS --------------------------------------------------
            # --------------------------------------------------------------------
            c1=None
            c2=None
            minD=float("inf")                 
            

            for i in range(tam):
                for j in range(filas[i]+1,n):
                    if minD>M[i][j]: 
                        minD=M[i][j]
                        c1=filas[i]
                        c2=j 
            
            comm.send(minD,dest=MASTER) # ENVIA
            
            

            
            

            """data=comm.recv(source=MASTER)
            if data==-1:
                comm.send(tam,dest=MASTER)
                break"""

            # --------------------------------------------------------------------
            # --- RECIBE DE MASTER -----------------------------------------------
            # --------------------------------------------------------------------


            

            # WORKER CON EL MINIMO
            w=comm.recv(source=MASTER)
            if w==myrank: 
                comm.send(c1,dest=MASTER)
                comm.send(c2,dest=MASTER)
            
            # INDICES DEL MININMO.
            # c1 FILA QUE SE QUEDA
            # c2 FILA QUE SE ELIMINA. (COLUMNA TAMBIEN)
            c1=comm.recv(source=MASTER)
            c2=comm.recv(source=MASTER)
            #wC1=comm.recv(source=MASTER) 
            wC2=comm.recv(source=MASTER) 

            
            #print("c1:{}, c2:{}, worker={}\n".format(c1,c2,wC2))
            
            
            
            # WORKER QUE ELIMINA FILA
            if wC2==myrank:                
                # ELIMINA FILA c2                
                tmp=filasDic[c2]                
                
                if tmp!=len(M): 
                    M.pop(filasDic[c2])
                    filasDic.pop(c2)
                

                

                
                # ACTUALIZA INDICES DEL DICCIONARIO Y FILASindices
                filas.pop(tmp)
                tam-=1
                if tam==0:
                    comm.send(-1,dest=MASTER)                    
                    break
                    #exit(1) # TERMINA LA EJECUCION
                else: 
                    comm.send(1,dest=MASTER)

                # ELIMINA COLUMNA c2 
                for row in M:                
                    del row[c2]

                for i in range(tmp,tam): 
                    filasDic.pop(filas[i])               
                    filas[i]-=1
                    filasDic[filas[i]]=i
                
                
            else:
                
                # ELIMINA COLUMNA c2            
                for row in M:                
                    del row[c2]


                # ACTUALIZA INDICES                
                i=0
                while i<tam:
                    if filas[i]>c2: break
                    i+=1
                for i in range(i,tam):
                    filasDic.pop(filas[i])               
                    filas[i]-=1
                    filasDic[filas[i]]=i
                
            # ELIMINA EL CLUSTER DE LA FILA ELIMINADA
            del clustersCentros[c2]           
            
            # ACTUALIZA EL CLUSTER DE c1
            clustersCentros[c1]=comm.recv(source=MASTER)
            
        

            #if cont==4: izq[10000]=0

            # ACTUALIZA COLUMNAS (1 POR FILA) 
            c1N=len(clustersCentros[c1])                                                 
            for i in range(tam):
                if M[i][c1]==-1: break # SI ES -1 LAS DEMAS TAMBIEN LO SERAN
                                
                nDist=float("inf")
                distTMP=0
                c2N=len(clustersCentros[i])
                for x in range(c1N):            # Recorre los individuos de "c1"
                    for y in range(c2N):        # Recorre los individuos de "i2 (individuo a cambiar de la fila)
                        distTMP=0
                        for a in range(d):
                            distTMP+=(clustersCentros[c1][x][a]-clustersCentros[i][y][a])**2
                        if distTMP<nDist: nDist=distTMP # Coge la menor distancia entre el individuo "c1" e "i"

                M[i][c1]=math.sqrt(nDist)
            
            n-=1 # REDUCE EL TAMAÑO DE LA POBLACION

            """if cont==16:
                print(myrank, "llega")
                exit(1)"""
            
            # ACTUALIZA FILA (SOLO EL WORKER DE c1)
            if w==myrank:  
                
                """for i in range(1, numWorkers+1)  :
                    if i!=myrank:
                        comm.send(-1,dest=i)
                for i in range(c1+1,n):                    
                    aux=0.0
                    nDist=float("inf")
                    c2N=len(clustersCentros[i])
                    for x in range(c1N):            # Recorre los individuos de "c1"
                        for y in range(c2N):    # Recorre los individuos de "i2 (individuo a cambiar de la fila)
                            distTMP=0
                            for a in range(d):                                
                                distTMP+=(clustersCentros[c1][x][a]-clustersCentros[i][y][a])**2
                            if distTMP<nDist: nDist=distTMP # Coge la menor distancia entre el individuo "c1" e "i"                                
                    M[filasDic[c1]][i]=math.sqrt(nDist)"""
                """print(M[filasDic[c1]])
                print(myrank,"\t",n,c1)
                exit(1)"""
                i=c1+1
                div=(n-c1-1)//(numWorkers-1)
                mod=(n-c1-1)%(numWorkers-1)

                
                if div>0:
                    for j in range(1, numWorkers+1):
                        if j==myrank: continue
                        comm.send(i,dest=j)
                        i+=1
                    
                    while i<n:
                        j=comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
                        source_rank=status.Get_source()
                        data=comm.recv(source=source_rank)
                        M[filasDic[c1]][j]=math.sqrt(data)
                        
                        comm.send(i,dest=source_rank)
                        i+=1
                
                    for _ in range(numWorkers-1):                                        
                        j=comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
                        source_rank=status.Get_source()
                        data=comm.recv(source=source_rank)
                        M[filasDic[c1]][j]=math.sqrt(data)

                        comm.send(-1,dest=source_rank)
                else:
                    
                    j=1
                    r=0
                    #for j in range(1,mod+1):
                    while j<mod+1:
                        if j==myrank:
                            mod+=1
                            r=1
                        else:
                            comm.send(i,dest=j)     
                            #print(j, i)                                               
                            i+=1
                        j+=1
                    mod-=r
                    
                    """if cont==16:
                        print(myrank, "llega")
                        exit(1)
                    print()"""
                    for j in range(mod+2,numWorkers+1):
                        if j==myrank: continue
                    
                        comm.send(-1,dest=j)                

                    

                    for xyz in range(mod):                                        
                        j=comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
                        source_rank=status.Get_source()
                        data=comm.recv(source=source_rank)                        
                        M[filasDic[c1]][j]=math.sqrt(data)

                        comm.send(-1,dest=source_rank) 
                    
                comm.send(1, dest=MASTER)
            else:
                
                while True:
                    i=comm.recv(source=w)
                    
                    if i==-1: break

                    aux=0.0
                    nDist=float("inf")
                    c2N=len(clustersCentros[i])
                    for x in range(c1N):            # Recorre los individuos de "c1"
                        for y in range(c2N):    # Recorre los individuos de "i2 (individuo a cambiar de la fila)
                            distTMP=0
                            for a in range(d):                                
                                distTMP+=(clustersCentros[c1][x][a]-clustersCentros[i][y][a])**2
                            if distTMP<nDist: nDist=distTMP # Coge la menor distancia entre el individuo "c1" e "i"                                
                    comm.send(i,dest=w)
                    comm.send(nDist,dest=w)
                
            
            

            cont+=1

        #print(myrank, "Sale del bucle principal\n")
        #exit(1)
            
            
               

        contador=0
        while(True):           
            
            fin=comm.recv(source=MASTER)
            if fin==END_OF_PROCESSING: break
            
            #print("{} LLega\t{}\t{}\t{}\t{}\t{}\n".format(myrank, fin, w,c1,c2,data))
            """if myrank==4 and contador==2:
                exit(1)"""
            

            w=comm.recv(source=MASTER)
            c1=comm.recv(source=MASTER)
            c2=comm.recv(source=MASTER)

            del clustersCentros[c2]                      
            # ACTUALIZA EL CLUSTER DE c1
            data=comm.recv(source=MASTER)
            #print("ID: {}\t w => {}\tdata => {}\n".format(myrank, w, data))
            clustersCentros[c1]=data

            c1N=len(clustersCentros[c1])            


            while True:
                i=comm.recv(source=w)
                if i==-1: break

                aux=0.0
                nDist=float("inf")
                c2N=len(clustersCentros[i])
                for x in range(c1N):            # Recorre los individuos de "c1"
                    for y in range(c2N):    # Recorre los individuos de "i2 (individuo a cambiar de la fila)
                        distTMP=0
                        for a in range(d):                                
                            distTMP+=(clustersCentros[c1][x][a]-clustersCentros[i][y][a])**2
                        if distTMP<nDist: nDist=distTMP # Coge la menor distancia entre el individuo "c1" e "i"                                
                comm.send(i,dest=w)
                comm.send(nDist,dest=w)
            

            contador+=1
            cont+=1
     

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
    path=os.path.join(dir, ".otros","ficheros","2_Cluster", archivo+".txt")

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


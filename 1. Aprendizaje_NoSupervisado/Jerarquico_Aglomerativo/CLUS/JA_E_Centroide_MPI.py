from mpi4py import MPI
import os
import math


# EJECUTAR
# mpiexec -np 4 python aglomerativeMPI_E_cent.py



def main():      
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    

    # -------------------------------------------------------------------------------------
    # --- DATOS A COMPARTIR ---------------------------------------------------------------
    # -------------------------------------------------------------------------------------

    poblacionEntrada=[]
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
        archivo="50000_2D"
        C=1
        poblacionEntrada=lee(archivo)
        
        
        n=len(poblacionEntrada)        
        d=len(poblacionEntrada[0])     
        
        
      
    
    
    # Envia el numero de dimensiones a los workers
    d=comm.bcast(d, root=MASTER)
    # Envia el numero de clusters a los workers
    C=comm.bcast(C, root=MASTER)
    

    # -------------------------------------------------------------------------------------
    # --- ALGORITMO -----------------------------------------------------------------------
    # -------------------------------------------------------------------------------------
    
    procesar=[(25000+(5000*i)) for i in range(6)]
    ruta_pruebas = os.path.dirname(os.path.abspath(__file__))
        
    
    for proc in procesar:
        timeStart=MPI.Wtime()

        if myrank==MASTER:
            poblacion=[]
            for ind in poblacionEntrada[0:proc+1]:
                poblacion.append(ind)

            for i in range(1,numWorkers+1):
                comm.send(poblacion,dest=i)
        else:
            poblacion=comm.recv(source=MASTER)

        
        n=proc   
            
        if myrank==MASTER:  
            k=C-1
            asig=[[] for _ in range(C)]
            centr=[[] for _ in range(C)]
        
            
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
            
            
            #print("Master: ", filasAsig)
            
            cont=0
            # Repite hasta que solo haya "C" clusters
            while(True): 
                # -------------------------------------------------------------------------------------
                # --- RECIBE MINIMOS ------------------------------------------------------------------
                # -------------------------------------------------------------------------------------        
                
                minW=-1
                minD=float("inf")
                wElim=None
                
                for i in workers:
                    data=comm.recv(source=i)                
                    if minD>data:
                        minD=data
                        minW=i
                    
                
                
                # SOLO QUEDA UN WORKER TODO QUITAR
                if numWorkers==1: comm.send(-1, dest=workers[-1])
                else: 
                    for i in workers:
                        comm.send(0,i)
                
                # ENVIA EL ID DEL worker CON EL MINIMO
                for i in workers:
                    comm.send(minW,dest=i)

                # RECIBE LA FILA Y COLUMNA DEL WORKER
                c1=comm.recv(source=minW)
                c2=comm.recv(source=minW)
                
                # ENVIA A TODOS LOS WORKERS LOS INDICES Y EL ID DEL worker CON LA FILA A ELIMINAR
                
                
                
                aux=filasAsig[c2]
                
                                    
                
                for i in workers:
                    comm.send(c1,dest=i)
                    comm.send(c2,dest=i)
                    comm.send(aux,dest=i)
                

            
                # ACTUALIZA INDICES
                n-=1
                for i in range(c2,n): # Sin error
                #for i in range(aux,n):
                    filasAsig[i]=filasAsig[i+1]
                filasAsig.pop(n)     
                
                
                # JUNTA LOS CLUSTERS
                for x in clusters[c2]:
                    clusters[c1].append(x)
                # ELIMINA EL CLUSTER DE LA FILA ELIMINADA
                del clusters[c2]
                del clustersCentros[c2]
                
                

                # ACTUALIZA EL CLUSTER NUEVO
                clustNew=[0 for _ in range(d)]

                for x in clusters[c1]:
                    for a in range(d):
                        clustNew[a]+=poblacion[x][a]
                tam=len(clusters[c1])
                for a in range(d):
                    clustNew[a]/=tam

                # ACTUALIZA EL CLUSTER DE c1
                clustersCentros[c1]=clustNew
                
                
                
                
                # RECIBE DEL worker QUE ELIMINA FILAS
                data=comm.recv(source=aux)
                if data==-1:                        
                    workers.remove(aux)
                    

                

                # ENVIA EL NUEVO CLUSTER
                for i in workers:
                    comm.send(clustNew,dest=i)
                
               


                # TERMINA CUANDO SOLO QUEDA UNO
                if len(workers)==1: 
                    comm.send(0,dest=workers[0])
                    break
                else:
                    for i in workers:
                        comm.send(1,dest=i)
                
                #if cont==2:clusters[1000000]=1
                
                cont+=1
            
            
            
            data=comm.recv(source=workers[0])
            if data==0: # CONTINUA
                while(True):
                    c1=comm.recv(source=workers[0])
                    c2=comm.recv(source=workers[0])

                    # JUNTA LOS CLUSTERS
                    for x in clusters[c2]:
                        clusters[c1].append(x)
                    # ELIMINA EL CLUSTER DE LA FILA ELIMINADA
                    del clusters[c2]
                    del clustersCentros[c2]
                    
                    

                    # ACTUALIZA EL CLUSTER NUEVO
                    clustNew=[0 for _ in range(d)]

                    for x in clusters[c1]:
                        for a in range(d):
                            clustNew[a]+=poblacion[x][a]
                    tam=len(clusters[c1])
                    for a in range(d):
                        clustNew[a]/=tam

                    # ACTUALIZA EL CLUSTER DE c1
                    clustersCentros[c1]=clustNew

                    comm.send(clustNew,dest=workers[0])

                
                   

                    data=comm.recv(source=workers[0])
                    if data==-1: break
                    n-=1



            timeEnd = MPI.Wtime()

            for i in range(1,numWorkers+1):
                comm.send(0,dest=i)


            
            ruta=os.path.join(ruta_pruebas,'AglomerativoE_MPI{}.txt'.format(numWorkers))    
            with open(ruta, 'a') as archivo:                               
                archivo.write(str(timeEnd-timeStart) + ', ')
            
            ruta=os.path.join(ruta_pruebas,'TamDatos_MPI{}.txt'.format(numWorkers))    
            with open(ruta, 'a') as archivo:                               
                archivo.write(str(x) + ', ')

        

            # ----------------------------------------------------------------------
            # ----------------------------------------------------------------------

        
        else : # WORKER
            pasa=False
            
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

                # --------------------------------------------------------------------
                # --- BUSCA MINIMOS --------------------------------------------------
                # --------------------------------------------------------------------
                c1=None
                c2=None
                minD=float("inf")                 
                cont+=1

                for i in range(tam):
                    for j in range(filas[i]+1,n):
                        if minD>M[i][j]: 
                            minD=M[i][j]
                            c1=filas[i]
                            c2=j 
                
                comm.send(minD,dest=MASTER) # ENVIA
                
                

                
                

                data=comm.recv(source=MASTER)
                if data==-1:
                    comm.send(tam,dest=MASTER)
                    break

                # --------------------------------------------------------------------
                # --- RECIBE DE MASTER -----------------------------------------------
                # --------------------------------------------------------------------


                

                # WORKER QUE VA A ELIMINAR SU FILA
                w=comm.recv(source=MASTER)
                if w==myrank: 
                    comm.send(c1,dest=MASTER)
                    comm.send(c2,dest=MASTER)
                
                # INDICES DEL MININMO.
                # c1 FILA QUE SE QUEDA
                # c2 FILA QUE SE ELIMINA. (COLUMNA TAMBIEN)
                c1=comm.recv(source=MASTER)
                c2=comm.recv(source=MASTER)
                data=comm.recv(source=MASTER)

                
                #print("c1:{}, c2:{}, worker={}\n".format(c1,c2,data))
                
                
                
                # WORKER QUE ELIMINA FILA
                if data==myrank:                
                    # ELIMINA FILA c2                
                    #print("Worker{}: aaaaaaaa tmp={}, {}".format(myrank,c2,filasDic))
                    tmp=filasDic[c2]                
                    
                    if filasDic[c2]!=len(M): 
                        M.pop(filasDic[c2])
                        filasDic.pop(c2)
                    

                    # ELIMINA COLUMNA c2 
                    for row in M:                
                        del row[c2]

                    
                    # ACTUALIZA INDICES DEL DICCIONARIO Y FILASindices
                    filas.pop(tmp)
                    tam-=1
                    if tam==0:
                        comm.send(-1,dest=MASTER)
                        pasa=True
                        break
                        #exit(1) # TERMINA LA EJECUCION
                    else: 
                        comm.send(1,dest=MASTER)

                    
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
                del poblacion[c2]
                
                
                # ACTUALIZA EL CLUSTER DE c1
                clustNew=comm.recv(source=MASTER)
                poblacion[c1]=clustNew
                
                #if cont==4: izq[10000]=0

                

                # ACTUALIZA COLUMNAS (1 POR FILA)                                      
                for i in range(tam):
                    if M[i][c1]==-1: break # SI ES -1 LAS DEMAS TAMBIEN LO SERAN
                    aux=0.0
                    
                    for a in range(d):
                        aux+=(poblacion[filas[i]][a]-poblacion[c1][a])**2             
                    M[i][c1]=math.sqrt(aux)        
                
                n-=1 # REDUCE EL TAMAÑO DE LA POBLACION

                # ACTUALIZA FILA (SOLO EL WORKER DE c1)
                if w==myrank:                                
                    for i in range(c1+1,n):                    
                        aux=0.0
                        for a in range(d):
                            aux+=(poblacion[i][a]-poblacion[c1][a])**2             
                        M[filasDic[c1]][i]=math.sqrt(aux)


                
                data = comm.recv(source=MASTER)
                if data==0:                        
                    break
                
                #if cont==3: izq[10000]=0
                
                


            if tam==1: 
                comm.send(-1,dest=MASTER)            
                #exit(1)
            elif pasa==False: 
                comm.send(0,dest=MASTER)

                while tam!=1:
                    # --------------------------------------------------------------------
                    # --- BUSCA MINIMOS --------------------------------------------------
                    # --------------------------------------------------------------------
                    c1=None
                    c2=None
                    minD=float("inf")
                    
                    #print("WORKER:", myrank, filas,"\n")

                    for i in range(tam):
                        for j in range(filas[i]+1,n):
                            if minD>M[i][j]: 
                                minD=M[i][j]
                                c1=filas[i]
                                c2=j 
                    
                    comm.send(c1,dest=MASTER)
                    comm.send(c2,dest=MASTER)

                    # ELIMINA FILA c2
                    tmp=filasDic[c2]                
                    if filasDic[c2]!=len(M): 
                        M.pop(filasDic[c2])
                        filasDic.pop(c2)
                    

                    # ELIMINA COLUMNA c2 
                    for row in M:                
                        del row[c2]

                    
                    # ACTUALIZA INDICES DEL DICCIONARIO Y FILASindices
                    filas.pop(tmp)
                    tam-=1                

                    for i in range(tmp,tam): 
                        filasDic.pop(filas[i])               
                        filas[i]-=1
                        filasDic[filas[i]]=i

                    # ELIMINA EL CLUSTER DE LA FILA ELIMINADA
                    del poblacion[c2]
                    
                    # ACTUALIZA EL CLUSTER DE c1
                    clustNew=comm.recv(source=MASTER)
                    poblacion[c1]=clustNew


                    

                    # ACTUALIZA COLUMNAS (1 POR FILA)                                      
                    for i in range(tam):
                        if M[i][c1]==-1: break # SI ES -1 LAS DEMAS TAMBIEN LO SERAN
                        aux=0.0
                        
                        for a in range(d):
                            aux+=(poblacion[filas[i]][a]-poblacion[c1][a])**2             
                        M[i][c1]=math.sqrt(aux)        
                    
                    n-=1 # REDUCE EL TAMAÑO DE LA POBLACION

                    # ACTUALIZA FILA (SOLO EL WORKER DE c1)
                    if w==myrank:                                
                        for i in range(c1+1,n):                    
                            aux=0.0
                            for a in range(d):
                                aux+=(poblacion[i][a]-poblacion[c1][a])**2             
                            M[filasDic[c1]][i]=math.sqrt(aux)
                    
                    if tam==1:comm.send(-1,dest=MASTER)
                    else: comm.send(0,dest=MASTER)

            comm.recv(source=MASTER)        



        
       
                

def distancia(a,b):
    ret=0.0
    for i in range(len(a)):
        ret+=(a[i]-b[i])**2        
    
    return math.sqrt(ret)



def lee(archivo):

    dir=os.getcwd()
    n=len(dir)


   
    path=os.path.join(dir, archivo+".txt")

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


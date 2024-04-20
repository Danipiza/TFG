from mpi4py import MPI
import random
import os
import math
import time


"""
SINCRONO
Tam. poblacion: 2042            Num. Repeticiones: 1
Capa Master: 2
Capa Oculta 1: 10
Capa Salida: 1
Tiempo de Entrenamiento: 2.8012851000530645s

Tam. poblacion: 2042            Num. Repeticiones: 1
Capa Master: 2
Capa Oculta 1: 10
Capa Oculta 2: 10
Capa Salida: 1
Tiempo de Entrenamiento: 3.928171099978499s




ASINCRONO
Tam. poblacion: 2042            Num. Repeticiones: 1
Capa Master: 2
Capa Oculta 1: 10
Capa Salida: 1
Tiempo de Entrenamiento: 1.0534301000880077s

Tam. poblacion: 2042            Num. Repeticiones: 1
Capa Master: 2
Capa Oculta 1: 10
Capa Oculta 2: 10
Capa Salida: 1
Tiempo de Entrenamiento: 2.6440837000263855s

"""


def mainSincrono():
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    tam_poblacion=0
    tam_entrenamiento=0
    repeticiones=0

    capas=0
    numCapas=0
    tiempoF=0
    tiempoB=0
    tiempoE=0
    
    # -----------------------------------------------------------------------------------------
    # --- INIT MPI. ---------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------    
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    if myrank==MASTER:
        repeticiones=1
        tam_poblacion=2042
        tam_entrenamiento=tam_poblacion*repeticiones

        """tiempoF=0.00001
        tiempoB=0.00002
        tiempoE=0.000008"""
        tiempoF=5.758284188196001e-06
        tiempoB=1.0545260192801458e-05
        tiempoE=2.688095571033576e-07

        aux=""
        for i in range(1,numWorkers):
            aux+="Capa Oculta {}: {}\n".format(i,10)
        print("Tam. poblacion: {}\t\tNum. Repeticiones: {}".format(tam_poblacion, repeticiones))
        print("Capa Master: {}\n{}Capa Salida: {}".format(2,aux,1))

    tam_entrenamiento=comm.bcast(tam_entrenamiento,root=MASTER)
    repeticiones=comm.bcast(repeticiones,root=MASTER)
    tam_poblacion=comm.bcast(tam_poblacion,root=MASTER)

    tiempoF=comm.bcast(tiempoF,root=MASTER)
    tiempoB=comm.bcast(tiempoB,root=MASTER)
    tiempoE=comm.bcast(tiempoE,root=MASTER)

    if myrank==0: capas=[2]
    if myrank<numWorkers: capas=[10]
    else: capas=[1]
    numCapas=len(capas)

    timeEntrStart = MPI.Wtime()

    if myrank==MASTER:
        espacio=(numWorkers*2)-1  


        for ind in range(espacio):                                             
            time.sleep(tiempoF)
            comm.send(0,dest=1)
        
        # BACKPROPAGATION Y FORWARD
        for ind in range(espacio,tam_entrenamiento):            
            errores=comm.recv(source=1)

            # BACKPROPAGATION
            time.sleep(tiempoB)
            # ENVIA FORWARD                                             
            time.sleep(tiempoF)                      
            
            # Devuelve el ultimo elemento
            comm.send(0,dest=1)

        

        # BACKPROPAGATION ACTUALIZA 
        for ind in range(espacio):
            errores=comm.recv(source=1)
                    
            # BACKPROPAGATION
            time.sleep(tiempoB)
        
        timeEntrEnd = MPI.Wtime()
        print("Tiempo de Entrenamiento: {}s\n".format(timeEntrEnd-timeEntrStart))
            
    elif myrank<numWorkers:
        entrada=comm.recv(source=myrank-1) # Recibe     
        # FORWARD
        time.sleep(tiempoF)      
        # Devuelve el ultimo elemento                
        comm.send(0,dest=myrank+1)
        
        # BACKPROPAGATION Y FORWARD
        for ind in range(tam_entrenamiento-1):                             
            errores=comm.recv(source=myrank+1)        
            # BACKPROPAGATION
            time.sleep(tiempoB)
            # ENVIA AL ANTERIOR
            comm.send(errores,dest=myrank-1)
            
            # RECIBE FORWARD              
            entrada=comm.recv(source=myrank-1) # Recibe   
            time.sleep(tiempoF)
            # Devuelve el ultimo elemento
            comm.send(0,dest=myrank+1)            
            
        

        # BACKPROPAGATION
        errores=comm.recv(source=myrank+1)            
        time.sleep(tiempoB)           

        # ENVIA AL ANTERIOR
        comm.send(errores,dest=myrank-1)

    else:
        for i in range(tam_entrenamiento):            
            data=comm.recv(source=myrank-1) 

            time.sleep(tiempoE)
                   
            comm.send(0,dest=myrank-1)


def mainASincrono():
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    tam_poblacion=0
    tam_entrenamiento=0
    repeticiones=0

    capas=0
    numCapas=0
    tiempoF=0
    tiempoB=0
    tiempoE=0

    cEntrada=0
    cOculta=0
    cSalida=0
    
    # -----------------------------------------------------------------------------------------
    # --- INIT MPI. ---------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------    
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    if myrank==MASTER:
        repeticiones=1
        tam_poblacion=2042
        tam_entrenamiento=tam_poblacion*repeticiones

        tiempoF=5.758284188196001e-06
        tiempoB=1.0545260192801458e-05
        tiempoE=2.688095571033576e-07

        cEntrada=2
        cOculta=10
        cSalida=1

        aux=""
        for i in range(1,numWorkers):
            aux+="Capa Oculta {}: {}\n".format(i,cOculta)
        print("Tam. poblacion: {}\t\tNum. Repeticiones: {}".format(tam_poblacion, repeticiones))
        print("Capa Master: {}\n{}Capa Salida: {}".format(cEntrada,aux,cSalida))

    tam_entrenamiento=comm.bcast(tam_entrenamiento,root=MASTER)
    repeticiones=comm.bcast(repeticiones,root=MASTER)
    tam_poblacion=comm.bcast(tam_poblacion,root=MASTER)

    tiempoF=comm.bcast(tiempoF,root=MASTER)
    tiempoB=comm.bcast(tiempoB,root=MASTER)
    tiempoE=comm.bcast(tiempoE,root=MASTER)

    cEntrada=comm.bcast(cEntrada,root=MASTER)
    cOculta=comm.bcast(cOculta,root=MASTER)
    cSalida=comm.bcast(cSalida,root=MASTER)

    if myrank==0: capas=[cEntrada]
    if myrank<numWorkers: capas=[cOculta]
    else: capas=[cSalida]
    numCapas=len(capas)

    timeEntrStart = MPI.Wtime()

    if myrank==MASTER:
        espacio=(numWorkers*2)-1  


        for ind in range(espacio):                                             
            # ENVIA FORWARD 
            time.sleep(tiempoF)
            requestS=comm.isend(0,dest=1)
            requestS.wait()
        
        # BACKPROPAGATION Y FORWARD
        for ind in range(espacio,tam_entrenamiento):            
            request=comm.irecv(source=1)

            
            # ENVIA FORWARD                                             
            time.sleep(tiempoF) 
            requestS=comm.isend(0,dest=1)
            requestS.wait()
            
            # BACKPROPAGATION
            errores=request.wait()            
            time.sleep(tiempoB)                     
            
            

        

        # BACKPROPAGATION ACTUALIZA 
        for ind in range(espacio):
            # BACKPROPAGATION
            request=comm.irecv(source=1)
            errores = request.wait()               
            time.sleep(tiempoB)
        
        timeEntrEnd = MPI.Wtime()
        print("Tiempo de Entrenamiento: {}s\n".format(timeEntrEnd-timeEntrStart))
            
    elif myrank<numWorkers:
        # FORWARD
        request=comm.irecv(source=myrank-1) # Recibe  
        entrada=request.wait()           
        time.sleep(tiempoF)                      
        requestS=comm.isend(0,dest=myrank+1)
        requestS.wait()
        
        # BACKPROPAGATION Y FORWARD
        for ind in range(tam_entrenamiento-1):                             
            requestB=comm.irecv(source=myrank+1)        
            

            # RECIBE FORWARD              
            requestF=comm.irecv(source=myrank-1) # Recibe   
            entrada=requestF.wait()
            time.sleep(tiempoF)
            requestS=comm.isend(0,dest=myrank+1) 
            requestS.wait()
             
            # BACKPROPAGATION
            errores=requestB.wait()               
            time.sleep(tiempoB)            
            requestS=comm.isend(errores,dest=myrank-1)
            requestS.wait()
            
        
        # BACKPROPAGATION
        request=comm.irecv(source=myrank+1)
        errores=request.wait()            
        time.sleep(tiempoB)  
        requestS=comm.isend(errores,dest=myrank-1)
        requestS.wait()

    else:
        for i in range(tam_entrenamiento):   
            # ERRORES         
            request=comm.irecv(source=myrank-1) 
            data=request.wait()       
            time.sleep(tiempoE)                   
            requestS=comm.isend(0,dest=myrank-1)
            requestS.wait()


mainSincrono()
#mainASincrono()
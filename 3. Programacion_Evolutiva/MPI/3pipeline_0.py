from mpi4py import MPI 
import sys
import os
import random
import math
import time

# Solo funciona con 5
# mpiexec -np 5 python 3PipeLine_0.py

"""
TIEMPOS:
    -- BIN --
    Inicializar: 100 =>     0.00256 
    Inicializar: 500 =>     0.01028
    Init(1): 0.0000256

    Evaluacion: 100 =>      0.00044
    Evaluacion: 500 =>      0.00212
    Eval(1): 0.0000044

    Ruleta:
    Seleccion: 100 =>       0.0007295000250451267
    Seleccion: 500 =>       0.004037000006064773 
    Torneo:
    Seleccion: 100 =>       0.0009646000107750297
    Seleccion: 500 =>       0.007905300008133054
    Selec(1): 0.0000085

    Cruce: 100 => 0.0013792999961879104
    Cruce: 500 => 0.00681389999226667
    Cruce(2): 0.0000276 

    Mutacion: 500 => 0.001530299981823191
    Mutacion: 500 => 0.0074155000038445
    Mutacion(1): 0.0000153


    -- REAL --       
        -- AEROPUERTO 1. -- 
        Inicializar: 100 =>     0.000664100021822378
        Inicializar: 500 =>     0.003797799989115447
        Init(1): 0.00000704 

        Evaluacion: 100 =>      0.0022515999735333025
        Evaluacion: 500 =>      0.011403600015910342
        Eval(1): 0.0000255 
        
        Torneo:
        Seleccion: 100 =>       0.0003929999948013574
        Seleccion: 500 =>       0.002154799993149936
        Selec(1): 0.00000412 

        Cruce: 100 =>           0.0009398999973200262
        Cruce: 500 =>           0.0016090999997686595
        Cruce(2): 0.00001478  

        Mutacion: 100 =>        0.00026339999749325216
        Mutacion: 500 =>        0.0011473000049591064
        Mutacion(1): 0.000002764

        
        -- AEROPUERTO 2. -- 
        Inicializar: 100 =>     0.0012645999959204346           
        Inicializar: 500 =>     0.007206799986306578 
        Init(1): 0.0000136 

        Evaluacion: 100 =>      0.0067051000078208745            
        Evaluacion: 500 =>      0.03203959998791106   
        Eval(1): 0.0000655 
        
        Torneo:
        Seleccion: 100 =>       0.0004619000246748328       
        Seleccion: 500 =>       0.0024018000112846494
        Selec(1): 0.00000462 

        Cruce: 100 =>           0.0012033999955747277                
        Cruce: 500 =>           0.0025147999986074865         
        Cruce(2): 0.000024 

        Mutacion: 100 =>        0.0003431999939493835        
        Mutacion: 500 =>        0.0017072999908123165
        Mutacion(1): 0.00000343      
        
        
        -- AEROPUERTO 3. -- 
        Inicializar: 100 =>     0.004979499994078651       
        Inicializar: 500 =>     0.025122500024735928    
        Init(1): 0.0000397 

        Evaluacion: 100 =>      0.043053400004282594       
        Evaluacion: 500 =>      0.21199099998921156   
        Eval(1): 0.00043 
        
        Torneo:
        Seleccion: 100 =>       0.0007886000094003975    
        Seleccion: 500 =>       0.004178600007435307
        Selec(1): 0.00000805 

        Cruce: 100 =>           0.002499400026863441              
        Cruce: 500 =>           0.007980199996381998           
        Cruce(2): 0.0000418 

        Mutacion: 100 =>        0.0010578999936114997    
        Mutacion: 500 =>        0.005148399999598041
        Mutacion(1): 0.0000104

        
    
        
    -- ARBOL --
        Inicializar: 100 => 0.006509700004244223    
        Inicializar: 500 => 0.028199699998367578    
        Init(1): 0.000061 

        Evaluacion: 100 => 0.0043175000173505396   
        Evaluacion: 500 => 0.020491500006755814     
        Eval(1): 0.0000421 
        
        Torneo:
        Seleccion: 100 => 0.008453799993731081
        Seleccion: 500 => 0.03867999999783933
        Selec(1): 0.0000805 

        Cruce: 100 => 0.00231280000298284          
        Cruce: 500 => 0.01008080001338385           
        Cruce(2): 0.000042

        Mutacion: 100 => 0.00011530000483617187
        Mutacion: 500 => 0.0004474000015761703
        Mutacion(1): 0.00000115




GRAMATICA
TODO
"""



def main():
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    tam_poblacion=0
    generaciones=0
    
    
    funcion_idx=0
    
    initT=0
    evalT=0
    selecT=0
    cruceT=0
    mutT=0

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    tam_poblacion=100
    generaciones=100

    # 0-3: Bin  4-6:Real    7: Arbol    8: Gramatica
    funcion_idx=6

    if myrank==MASTER: 
        print("Tam. Poblacion: {}\tNum. Generaciones: {}\n".format(tam_poblacion, generaciones))

    if funcion_idx<=3:
        if myrank==MASTER: print("Programa Binario\n")
        initT=      0.0000256 # Solo se hace numWorkers veces

        evalT=      0.0000044 # Juntar con selec
        selecT=     0.0000085 # 0.0000129
        cruceT=     0.0000138 
        mutT=       0.0000153
        
    elif funcion_idx<=6:
        if myrank==MASTER: print("Programa Real",end=" ")
        if funcion_idx==4:
            if myrank==MASTER: print("Aeropuerto1\n")
            initT=  0.00000704  # Solo se hace numWorkers veces
            
            evalT=  0.0000255   # Dividir entre mas procesos 
            selecT= 0.00000412  
            cruceT= 0.00000739 
            mutT=   0.000002764
            
        elif funcion_idx==5:
            if myrank==MASTER: print("Aeropuerto2\n")
            initT=  0.0000136   # Solo se hace numWorkers veces

            evalT=  0.0000655   # Dividir entre mas procesos
            selecT= 0.00000462 
            cruceT= 0.000012 
            mutT=   0.00000343
        else:
            if myrank==MASTER: print("Aeropuerto3\n")
            initT=  0.0000397   # Solo se hace numWorkers veces

            evalT=  0.00043     # Dividir entre mas procesos
            selecT= 0.00000805 
            cruceT= 0.0000209 
            mutT=   0.0000104
        
    elif funcion_idx==7:
        if myrank==MASTER: print("Programa Arbol\n")
        initT=      0.000061    # Solo se hace numWorkers veces

        evalT=      0.0000421 
        selecT=     0.0000805   
        cruceT=     0.000021    # Juntar 
        mutT=       0.00000115  # tiempo nuevo: 00002215
    else:
        if myrank==MASTER: print("Programa Gramatica\n")
        initT=0
        evalT=0
        selecT=0
        cruceT=0
        mutT=0

    tiempoSinM=(initT*tam_poblacion)+(evalT*tam_poblacion)+((selecT+cruceT+mutT)*tam_poblacion*generaciones)
    if myrank==MASTER: print("Sin mejorar",tiempoSinM)

    totalTimeStart = MPI.Wtime()
    if myrank==MASTER:

        
        poblacion=[]
        if funcion_idx<4:       # BINARIO
            for _ in range(4):
                """AG.init_poblacion()
                AG.evaluacion_poblacionBin()            
                comm.send(AG.poblacion, dest=myrank+1)"""  
                time.sleep(initT*tam_poblacion)          
                time.sleep(evalT*tam_poblacion)
                
                comm.send(1, dest=myrank+1)
            
            while(generaciones>0):
                data=comm.recv(source=numWorkers)
                
                generaciones-=1
            
        elif funcion_idx<7:     # REAL
            for _ in range(4):
                """AG.init_poblacion()
                AG.evaluacion_poblacionReal()                 
                comm.send(AG.poblacion, dest=myrank+1)"""          
                time.sleep(initT*tam_poblacion)
                time.sleep(evalT*tam_poblacion)

                comm.send(1, dest=myrank+1)

            while(generaciones>0):
                data=comm.recv(source=numWorkers)
                
                generaciones-=1

        elif funcion_idx==7:    # ARBOL
            for _ in range(4):
                """AG.init_poblacionArbol()
                AG.evaluacion_poblacionArbol()                 
                comm.send(AG.poblacion, dest=myrank+1)"""
                time.sleep(initT*tam_poblacion)
                time.sleep(evalT*tam_poblacion)

                comm.send(1, dest=myrank+1)
            
            while(generaciones>0):
                data=comm.recv(source=numWorkers)
                
                generaciones-=1
        else:                   # GRAMATICA
            for _ in range(4):
                """AG.init_poblacionGramatica()
                AG.evaluacion_poblacionGramatica()                 
                comm.send(AG.poblacion, dest=myrank+1)"""            
                time.sleep(initT*tam_poblacion)
                time.sleep(evalT*tam_poblacion)

                comm.send(1, dest=myrank+1)
            
            while(generaciones>0):
                data=comm.recv(source=numWorkers)
                
                generaciones-=1
        
        totalTimeEnd = MPI.Wtime()
        print("Tiempo de ejecucion total: {}".format(totalTimeEnd-totalTimeStart))
        print("Speed up: {}\n".format(tiempoSinM/(totalTimeEnd-totalTimeStart)))
     
        
    elif myrank==1: # WORKER SELECCION      

        if funcion_idx<4:       # BINARIO
            for _ in range(4):
                """AG.poblacion=comm.recv(source=myrank-1)                
                selec=AG.seleccion_poblacionBin(5)
                comm.send(selec,dest=myrank+1)"""                
                data=comm.recv(source=myrank-1)  
                time.sleep(selecT*tam_poblacion)              
                # Selec
                comm.send(1,dest=myrank+1)

                          

            generaciones-=4

            while(generaciones>0):                
                """AG.poblacion=comm.recv(source=numWorkers)
                selec=AG.seleccion_poblacionBin(5)
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=numWorkers)
                time.sleep(selecT*tam_poblacion)                
                # Selec
                comm.send(1,dest=myrank+1)

                generaciones-=1
                
        elif funcion_idx<7:     # REAL
            for _ in range(4):
                """AG.poblacion=comm.recv(source=myrank-1)                
                selec=AG.seleccion_poblacionBin(5)
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=myrank-1) 
                time.sleep(selecT*tam_poblacion)               
                # Selec
                comm.send(1,dest=myrank+1)

                          

            generaciones-=4

            while(generaciones>0):                
                """AG.poblacion=comm.recv(source=numWorkers)
                selec=AG.seleccion_poblacionBin(5)
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=numWorkers)                
                time.sleep(selecT*tam_poblacion)
                # Selec
                comm.send(1,dest=myrank+1)

                generaciones-=1
        elif funcion_idx==7:    # ARBOL
            for _ in range(4):
                """AG.poblacion=comm.recv(source=myrank-1)                
                selec=AG.seleccion_poblacionBin(5)
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=myrank-1)
                time.sleep(selecT*tam_poblacion)               
                # Selec
                comm.send(1,dest=myrank+1)

                          

            generaciones-=4

            while(generaciones>0):                
                """AG.poblacion=comm.recv(source=numWorkers)
                selec=AG.seleccion_poblacionBin(5)
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=numWorkers) 
                time.sleep(selecT*tam_poblacion)               
                # Selec
                comm.send(1,dest=myrank+1)

                generaciones-=1
        else:                   # GRAMATICA  
            for _ in range(4):
                """AG.poblacion=comm.recv(source=myrank-1)                
                selec=AG.seleccion_poblacionBin(5)
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=myrank-1) 
                time.sleep(selecT*tam_poblacion)               
                # Selec
                comm.send(1,dest=myrank+1)

                          

            generaciones-=4

            while(generaciones>0):                
                """AG.poblacion=comm.recv(source=numWorkers)
                selec=AG.seleccion_poblacionBin(5)
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=numWorkers)    
                time.sleep(selecT*tam_poblacion)            
                # Selec
                comm.send(1,dest=myrank+1)

                generaciones-=1
        exit(1)


    elif myrank==2: # WORKER CRUCE
        
        if funcion_idx<4:       # BINARIO
            while(generaciones>0):
                """selec=[]    
                poblacion=comm.recv(source=myrank-1)          
                selec=AG.cruce_poblacionBin(poblacion)                
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=myrank-1) 
                time.sleep(cruceT*tam_poblacion)
                # Cruce
                comm.send(data,dest=myrank+1)

                generaciones-=1
            
        elif funcion_idx<7:     # REAL
            while(generaciones>0):
                """selec=[]    
                poblacion=comm.recv(source=myrank-1)          
                selec=AG.cruce_poblacionBin(poblacion)                
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=myrank-1) 
                time.sleep(cruceT*tam_poblacion)
                # Cruce
                comm.send(data,dest=myrank+1)

                generaciones-=1
        elif funcion_idx==7:    # ARBOL
            while(generaciones>0):
                """selec=[]    
                poblacion=comm.recv(source=myrank-1)          
                selec=AG.cruce_poblacionBin(poblacion)                
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=myrank-1) 
                time.sleep(cruceT*tam_poblacion)
                # Cruce
                comm.send(data,dest=myrank+1)

                generaciones-=1
        else:                   # GRAMATICA  
            while(generaciones>0):
                """selec=[]    
                poblacion=comm.recv(source=myrank-1)          
                selec=AG.cruce_poblacionBin(poblacion)                
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=myrank-1)
                time.sleep(cruceT*tam_poblacion) 
                # Cruce
                comm.send(data,dest=myrank+1)

                generaciones-=1
        exit(1)
    elif myrank==3: # WORKER MUTACION
        
        if funcion_idx<4:       # BINARIO
            while(generaciones>0):
                """selec=[]
                poblacion=comm.recv(source=myrank-1)                
                selec=AG.mutacion_poblacionBin(poblacion)
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=myrank-1) 
                time.sleep(mutT*tam_poblacion) 
                # Mutacion
                comm.send(data,dest=myrank+1)
                generaciones-=1
            
        elif funcion_idx<7:     # REAL
            while(generaciones>0):
                """selec=[]
                poblacion=comm.recv(source=myrank-1)                
                selec=AG.mutacion_poblacionBin(poblacion)
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=myrank-1) 
                time.sleep(mutT*tam_poblacion)  
                # Mutacion
                comm.send(data,dest=myrank+1)
                generaciones-=1
        elif funcion_idx==7:    # ARBOL
            while(generaciones>0):
                """selec=[]
                poblacion=comm.recv(source=myrank-1)                
                selec=AG.mutacion_poblacionBin(poblacion)
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=myrank-1) 
                time.sleep(mutT*tam_poblacion)  
                # Mutacion
                comm.send(data,dest=myrank+1)
                generaciones-=1
        else:                   # GRAMATICA  
            while(generaciones>0):
                """selec=[]
                poblacion=comm.recv(source=myrank-1)                
                selec=AG.mutacion_poblacionBin(poblacion)
                comm.send(selec,dest=myrank+1)"""
                data=comm.recv(source=myrank-1)  
                time.sleep(mutT*tam_poblacion) 
                # Mutacion
                comm.send(data,dest=myrank+1)
                generaciones-=1
        exit(1)
    elif myrank==4: # WORKER EVALUACION
        
        if funcion_idx<4:       # BINARIO
            while(generaciones>0):                                                
                """AG.poblacion=comm.recv(source=myrank-1)
                AG.evaluacion_poblacionBin()
                
                comm.send(AG.poblacion,dest=MASTER+1)
                comm.send(AG.poblacion,dest=MASTER) """
                data=comm.recv(source=myrank-1)
                time.sleep(evalT*tam_poblacion) 
                # Evaluacion                                       
                comm.send(data,dest=MASTER+1)
                comm.send(data,dest=MASTER)

                
                generaciones-=1
            
        elif funcion_idx<7:     # REAL
            while(generaciones>0):                                                
                """AG.poblacion=comm.recv(source=myrank-1)
                AG.evaluacion_poblacionBin()
                
                comm.send(AG.poblacion,dest=MASTER+1)
                comm.send(AG.poblacion,dest=MASTER) """
                data=comm.recv(source=myrank-1)
                time.sleep(evalT*tam_poblacion) 
                # Evaluacion                                       
                comm.send(data,dest=MASTER+1)
                comm.send(data,dest=MASTER)

                
                generaciones-=1
        elif funcion_idx==7:    # ARBOL
            while(generaciones>0):                                                
                """AG.poblacion=comm.recv(source=myrank-1)
                AG.evaluacion_poblacionBin()
                
                comm.send(AG.poblacion,dest=MASTER+1)
                comm.send(AG.poblacion,dest=MASTER) """
                data=comm.recv(source=myrank-1)
                time.sleep(evalT*tam_poblacion) 
                # Evaluacion                                       
                comm.send(data,dest=MASTER+1)
                comm.send(data,dest=MASTER)

                
                generaciones-=1
        else:                   # GRAMATICA  
            while(generaciones>0):                                                
                """AG.poblacion=comm.recv(source=myrank-1)
                AG.evaluacion_poblacionBin()
                
                comm.send(AG.poblacion,dest=MASTER+1)
                comm.send(AG.poblacion,dest=MASTER) """
                data=comm.recv(source=myrank-1)
                time.sleep(evalT*tam_poblacion) 
                # Evaluacion                                       
                comm.send(data,dest=MASTER+1)
                comm.send(data,dest=MASTER)

                
                generaciones-=1
        exit(1)
        

        

    
    
    
    


main()
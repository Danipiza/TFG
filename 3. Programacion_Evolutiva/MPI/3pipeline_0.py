"""if myrank==MASTER:
        poblacion=[]
        if funcion_idx<4:       # BINARIO
            for _ in range(4):
                # Init
                """AG.init_poblacion()
                # Eval
                AG.evaluacion_poblacionBin()                """
                # Envia
                """comm.send(AG.poblacion, dest=myrank+1)"""
                comm.send(1,dest=myrank+1)
            
            
            while(generaciones>0):
                data=comm.recv(source=numWorkers)
                
                generaciones-=1
            
        elif funcion_idx<7:     # REAL
            for _ in range(4):
                a=0
                # Init
                
                # Eval

                # Envia
            generaciones-=4
            
            while(generaciones>0):
                data=comm.recv(source=numWorkers)

                comm.send(data,dest=myrank+1)
                generaciones-=1
        elif funcion_idx==7:    # ARBOL
            for _ in range(4):
                a=0
                # Init
                
                # Eval

                # Envia
            generaciones-=4
            
            while(generaciones>0):
                data=comm.recv(source=numWorkers)

                comm.send(data,dest=myrank+1)
                generaciones-=1
        else:                   # GRAMATICA
            for _ in range(4):
                a=0
                # Init
                
                # Eval

                # Envia
            generaciones-=4
            
            while(generaciones>0):
                data=comm.recv(source=numWorkers)

                comm.send(data,dest=myrank+1)
                generaciones-=1
        
        totalTimeEnd = MPI.Wtime()
        #print("Valor Optimo: {}\n".format(progreso[-1]))
        print("Tiempo de ejecucion total: {}\n".format(totalTimeEnd-totalTimeStart))

        #GUI(progreso)       
        
    elif myrank==1: # WORKER SELECCION      

        if funcion_idx<4:       # BINARIO
            for _ in range(4):
                data=comm.recv(source=myrank-1)
                """AG.poblacion=comm.recv(source=myrank-1)
                selec=AG.seleccion_poblacionBin(5)
                comm.send(selec,dest=myrank+1)"""                

                comm.send(1,dest=myrank+1)
            generaciones-=4

            while(generaciones>0):
                data=comm.recv(source=numWorkers)
                """AG.poblacion=comm.recv(source=myrank-1)
                selec=AG.seleccion_poblacionBin(5)
                comm.send(selec,dest=myrank+1)"""                

                comm.send(1,dest=myrank+1)
                generaciones-=1
            exit(1)
        elif funcion_idx<7:     # REAL
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=myrank+1)
                generaciones-=1
            exit(1)
        elif funcion_idx==7:    # ARBOL
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=myrank+1)
                generaciones-=1
            exit(1)
        else:                   # GRAMATICA  
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=myrank+1)
                generaciones-=1
            exit(1)


    elif myrank==2: # WORKER CRUCE
        
        if funcion_idx<4:       # BINARIO
            while(generaciones>0):
                selec=[]
                poblacion=comm.recv(source=myrank-1)
                
                """selec=AG.cruce_poblacionBin(poblacion)                
                comm.send(selec,dest=myrank+1)"""
                comm.send(1,dest=myrank+1)
                generaciones-=1
            exit(1)
        elif funcion_idx<7:     # REAL
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=myrank+1)
                generaciones-=1
            exit(1)
        elif funcion_idx==7:    # ARBOL
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=myrank+1)
                generaciones-=1
            exit(1)
        else:                   # GRAMATICA  
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=myrank+1)
                generaciones-=1
            exit(1)

    elif myrank==3: # WORKER MUTACION
        
        if funcion_idx<4:       # BINARIO
            while(generaciones>0):
                selec=[]
                poblacion=comm.recv(source=myrank-1)
                
                """selec=AG.mutacion_poblacionBin(poblacion)
                comm.send(selec,dest=myrank+1)"""

                comm.send(1,dest=myrank+1)
                
                generaciones-=1
            exit(1)
        elif funcion_idx<7:     # REAL
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=myrank+1)
                generaciones-=1
            exit(1)
        elif funcion_idx==7:    # ARBOL
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=myrank+1)
                generaciones-=1
            exit(1)
        else:                   # GRAMATICA  
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=myrank+1)
                generaciones-=1
            exit(1)

    elif myrank==4: # WORKER EVALUACION
        
        if funcion_idx<4:       # BINARIO
            while(generaciones>0):                                
                poblacion=comm.recv(source=myrank-1)
                """AG.poblacion=poblacion
                AG.evaluacion_poblacionBin()
                
                comm.send(AG.poblacion,dest=MASTER+1)
                comm.send(AG.poblacion,dest=MASTER)"""
                
                comm.send(1,dest=MASTER+1)
                comm.send(1,dest=MASTER)
                
                generaciones-=1
            exit(1)
        elif funcion_idx<7:     # REAL
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=MASTER+1)
                generaciones-=1
            exit(1)
        elif funcion_idx==7:    # ARBOL
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=MASTER+1)
                generaciones-=1
            exit(1)
        else:                   # GRAMATICA  
            while(generaciones>0):
                data=comm.recv(source=myrank-1)

                comm.send(data,dest=MASTER+1)
                generaciones-=1
            exit(1)

        """
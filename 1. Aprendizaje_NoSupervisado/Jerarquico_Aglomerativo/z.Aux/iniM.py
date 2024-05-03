from mpi4py import MPI
import os
import math

# mpiexec -np 5 python p1.py

def main():      
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    n=0

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1


    # Inicializa centros
    if myrank==MASTER:                 
        n=1000      
        print(n)
    
    # Envia el numero de clusters a los workers
    n=comm.bcast(n, root=MASTER)
    
    timeStart = MPI.Wtime()
    
    
    if myrank==MASTER:       
        tam=0
        M=[]
        for i in range(1,numWorkers+1):
            comm.send(1, dest=i)
            tam+=1
        
        while tam<n:
            datos = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
            source_rank=status.Get_source()
            tam+=1
            M.append(datos)
            comm.send(1, dest=source_rank)
        
        for i in range(1,numWorkers+1):
            datos = comm.recv(source=i)
            M.append(datos)
            comm.send(END_OF_PROCESSING, dest=i)
            
                
        timeEnd = MPI.Wtime()
        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))

        """M[0][1]=1
        print(M[0][1], M[1][1])"""
    
    else : # WORKER
        while True:            
            a=comm.recv(source=MASTER)
            if a==END_OF_PROCESSING: 
                print("(WORKER {}) TERMINA".format(myrank))
                exit()

            out=[0 for _ in range(n)]
            comm.send(out, dest=MASTER)

        

    



main()
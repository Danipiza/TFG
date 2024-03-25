from mpi4py import MPI
import os
import math

# mpiexec -np 5 python p3.py





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

    if myrank==MASTER:
        for i in range(1,numWorkers+1):
            comm.send(1,dest=i)
            
        print("Fin MASTER")
        exit(0)
    else:
        print("Fin WORKER",myrank)
        exit(0)
    

    
        

        

    



main()
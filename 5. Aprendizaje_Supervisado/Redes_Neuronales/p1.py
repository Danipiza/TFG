from mpi4py import MPI
import random
import os
import math

# EJECUTAR
# mpiexec -np 3 python p1.py


def main():
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    # DATOS A COMPARTIR 
    a=[]  
    capas=0

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    if myrank==MASTER:
        a=[i for i in range(1,11)]

    if myrank==MASTER:
        print()
        cont=0
        espacio=(numWorkers*2)-1
        for _ in range(espacio):
            comm.send(a[cont],dest=1)
            cont+=1
        
        for i in range(10-espacio):
            data=comm.recv(source=1)
            print("M. recibe y actualiza:",data)
            
            comm.send(a[cont],dest=1)
            cont+=1

        for _ in range(espacio):
            data=comm.recv(source=1)
            print("M. recibe y actualiza:",data)
    
    elif myrank!=numProc-1: # Worker1
        print()
        data=comm.recv(source=myrank-1)
        print("W{}. recibe: {}".format(myrank,data))
        comm.send(data,dest=myrank+1)

        for _ in range(9):
            data=comm.recv(source=myrank+1)
            print("W{}. recibe y actualiza: {}".format(myrank,data))
            comm.send(data*10,dest=myrank-1)
            data=comm.recv(source=myrank-1)
            print("W{}. recibe: {}".format(myrank,data))
            comm.send(data,dest=myrank+1)
        
        data=comm.recv(source=myrank+1)
        print("W{}. recibe y actualiza: {}".format(myrank,data))
        comm.send(data*10,dest=myrank-1)               
    else: # Worker2
        print()
        for _ in range(10):
            data=comm.recv(source=myrank-1)
            print("W{}. recibe: {}".format(myrank,data))
            comm.send(data*10,dest=myrank-1)









main()

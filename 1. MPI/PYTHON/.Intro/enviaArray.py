from mpi4py import MPI
#import numpy as np

  

def main():
    # No hay MPI_Init()
    comm=MPI.COMM_WORLD
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWork=numProc-1

    if myrank==0:print("Numero de workers", numProc)
    else : print("Worker",myrank)
    
    if myrank == 0:  # Master process
        array_size = 20
        array = [(i) for i in range(20)]
        print(array)
        
        tam=array_size//numWork
        indices=[0,tam-1]
        
        for i in range(numWork):
            comm.send(array, dest=i+1)
            comm.send(indices, dest=i+1)
            indices[0]+=tam
            indices[1]+=tam        

        results = []
        for i in range(numWork):
            results.append(comm.recv())               

        print("Array:", results)

    else:  # Worker processes
        array = comm.recv(source=0)
        indices = comm.recv(source=0)
        if myrank==2:
            print("2. array:", array)
            print("2. indices:", indices)
        ret=1
        for i in range(indices[0], indices[1]+1):
            if myrank==2:print(array[i])
            ret *= array[i]
        if myrank==2: print("2. ret:",ret)
        comm.send(ret, dest=0)
    
    # End MPI environment
    MPI.Finalize()
    


main()


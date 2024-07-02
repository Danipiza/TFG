from mpi4py import MPI
#import numpy as np

# EJECUTAR
# mpiexec -np 5 python .\enviaArray.py

"""
El Master crea un array (data), y envia una parte a cada worker, para que estos eleven al cuadrado
el subarray recibido, y lo envien de vuelta. 
"""

def main():
    # No hay MPI_Init()
    comm=MPI.COMM_WORLD
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWork=numProc-1

    if myrank==0:print("Numero de workers:", numProc)
    else : print("Worker:",myrank)
    
    if myrank==0:  # Master 
        tam=20
        array=[(i) for i in range(20)]
        print(array)
        
        tam=tam//numWork
        indices=[0,tam-1]
        
        for i in range(numWork):
            comm.send(array, dest=i+1)
            comm.send(indices, dest=i+1)
            indices[0]+=tam
            indices[1]+=tam        

        results = []
        # Da igual porque Worker lo recibe
        for i in range(numWork):
            results.append(comm.recv())               

        print("Array:", results)

    else:  # Worker 
        array = comm.recv(source=0)
        indices = comm.recv(source=0)
        if myrank==2:
            print("2. array:", array)
            print("2. indices:", indices)
        ret=1
        for i in range(indices[0], indices[1]+1):
            if myrank==2:print(array[i])
            ret*=array[i]
            
        if myrank==2: print("2. ret:",ret)
        comm.send(ret, dest=0)
    
    # opcional
    MPI.Finalize()
    


main()


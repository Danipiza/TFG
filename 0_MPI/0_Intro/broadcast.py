from mpi4py import MPI


# EJECUTAR
# mpiexec -np 5 python .\broadcast.py

"""
Programa que implementa la funcion broadcast() de MPI

El Master crea un array (data), y usando broadcast() todos los procesos reciben el array.
"""

def main():
    # Inicializar MPI
    comm=MPI.COMM_WORLD
    myrank=comm.Get_rank()
    numProc=comm.Get_size()

    data=None
    if myrank==0: data=[i for i in range(5)]


    # Broadcast desde el proceso master a todos los workers
    data=comm.bcast(data, root=0)

    # Cada proceso imprime el dato recibido
    if myrank==0:print("Master tiene", numProc, "workers")
    else: print("Worker", myrank, "recibe:", data)

    # End MPI environment
    MPI.Finalize()


main()
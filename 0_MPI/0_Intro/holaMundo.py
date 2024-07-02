from mpi4py import MPI

# EJECUTAR
# mpiexec -np 5 python .\holaMundo.py

"""
Hola mundo con MPI
"""

def main():
    # Init
    comm=MPI.COMM_WORLD
    myrank=comm.Get_rank()
    numProc=comm.Get_size()

    if myrank==0: print("Proceso Master, se han creado", numProc-1, "workers")
    else: print("Hola desde el worker", myrank)

main()

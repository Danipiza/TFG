from mpi4py import MPI

MASTER = 0
END_OF_PROCESSING=-2


# EJECUTAR
# mpiexec -np 5 python .\anysource.py

"""
Programa que implementa la funcion anysource() de MPI

El Master envia enteros a los workers, estos los reciben y envia de vuelta.
El Master recibe los mensajes sin orden, usando anysource() para recibir los mensajes y enviar 
el mensaje de finalizacion (END_OF_PROCESSING)
"""




def main():
    # Variables MPI
  	

    timeStart=0.0           # double.
    timeEnd=0.0

    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    if myrank==0:
        for i in range(1,numWorkers+1):
            comm.send(i,dest=i)
        
        for i in range(numWorkers):
            val=comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
            source_rank = status.Get_source()            
            print("Master recibe:",val,"de:", source_rank)
            
            comm.send(END_OF_PROCESSING,dest=source_rank)                        

    else:
        while(True):
            val=comm.recv(source=MASTER, tag=tag,status=status)
            if val==END_OF_PROCESSING: break

            comm.send(val,dest=MASTER)    

main()
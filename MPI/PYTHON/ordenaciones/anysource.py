from mpi4py import MPI
import sys

MASTER = 0
END_OF_PROCESSING=-2
INF=sys.maxsize

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
            val = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
            source_rank = status.Get_source()            
            comm.send(-1,dest=source_rank)            
            print("Master recibe:",val,"de:", source_rank)

    else:
        while(True):
            val = comm.recv(source=MASTER, tag=tag,status=status)
            if val==-1: break

            comm.send(val,dest=MASTER)    

main()
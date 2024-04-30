from mpi4py import MPI
import time

def prueba1():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        print("Se necesitan al menos dos procesos para este ejemplo.")
        MPI.Finalize()
        exit()

    if rank==0:    
        request1 = comm.isend(1, dest=1)#, tag=123)
        request2 = comm.isend(2, dest=1)#, tag=124)
        print(f"Proceso {rank} envio el mensaje de forma asincrona.")

        request2.wait()  
        request1.wait()  
        
    else:
        request1 = comm.irecv(source=0)#, tag=123)

        request2 = comm.irecv(source=0)#, tag=124)
        data2 = request2.wait()  
        print("WORKER 1 RECIBE SEGUNDO MENSAJE:",data2)

        data1 = request1.wait()  
        print("WORKER 1 RECIBE PRIMER MENSAJE:",data1)


def prueba2():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        print("Se necesitan al menos dos procesos para este ejemplo.")
        MPI.Finalize()
        exit()

    if rank==0:    
        comm.send(1,dest=1)
        comm.send(2,dest=1)
        comm.send(3,dest=1)

        time.sleep(2)
        request1 = comm.isend(10, dest=1)#, tag=123) 
        #request1.wait()  
        
    else:
        d1=comm.recv(source=0)
        d2=comm.recv(source=0)
        d3=comm.recv(source=0)
        request1 = comm.irecv(source=0)#, tag=123)

        time.sleep(0.5)
        print("Termina 1, r1:",request1)
        time.sleep(0.5)
        print("Termina 2, r1:",request1)
        a=request1.wait()
        time.sleep(0.5)
        print("Termina 3, r1:",a)

        
prueba2()
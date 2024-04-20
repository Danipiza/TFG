from mpi4py import MPI

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

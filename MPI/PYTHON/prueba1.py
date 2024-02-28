from mpi4py import MPI

def worker():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    # Recibe el mensaje del proceso maestro
    mensaje = comm.recv(source=0)
    
    # Procesa el mensaje
    resultado = mensaje * mensaje
    
    # Envía el resultado al proceso maestro
    comm.send(resultado, dest=0)

def master():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    
    # Enviar mensaje a los workers
    mensaje = 10
    for worker_rank in range(1, size):
        comm.send(mensaje, dest=worker_rank)
    
    # Recibir resultados de los workers
    resultados = []
    for worker_rank in range(1, size):
        resultado = comm.recv(source=worker_rank)
        resultados.append(resultado)
    
    print("Resultados recibidos:", resultados)

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    if rank == 0:
        master()
    else:
        worker()

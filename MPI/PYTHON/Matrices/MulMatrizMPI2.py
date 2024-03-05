from mpi4py import MPI
import numpy as np



# Generate a matrix with random int values
def generate_matrix(valor_maximo, tam):
    return np.random.randint(0, valor_maximo, size=(tam, tam))



def main():    
    MASTER = 0              # int.      Master 
    PRINT = True           # boolean.  Imprimir matrices
    END_OF_PROCESSING = 0  # End of processing

    NROWS = 10  # Number of rows to each worker
    

    tam = 100  # Matrix size
    valor_maximo = 10  # Maximum number value for generating each matrix


    comm = MPI.COMM_WORLD
    myrank = comm.Get_rank()
    numProc = comm.Get_size()
    numWorkers=numProc-1
    print("HOLA")

    if (NROWS * (numWorkers)) > tam:
        if myrank == MASTER:
            print(f"Wrong configuration for NROWS ({NROWS}). SIZE ({tam}) < numWorkers({numProc-1})*NROWS({NROWS})")
            print("At least, each worker must receive {} rows to be processed".format(NROWS))
        MPI.Finalize()
        exit(-1)

    matrixA=[[]]
    matrixB=[[]]
    if myrank == MASTER:

        # Generate matrix A			
        print("Generating matrix A (%dx%d)\n", tam, tam);        
        matrixA=generate_matrix(valor_maximo, tam)
        if PRINT:
            print("Matrix A:\n")
            print(matrixA)
            print("\n\n")
        

        # Generate matrix B
        print("Generating matrix B (%dx%d)\n", tam, tam);   
        matrixB = generate_matrix(valor_maximo, tam)
        if PRINT:
            print("Matrix B:")
            print(matrixB)
            print("\n\n")

    # Broadcast matrix B
    matrixB = comm.bcast(matrixB, root=MASTER)

    if myrank == MASTER:
        matrixC = np.zeros((tam, tam), dtype=int)

        sent_rows = 0
        current_row = 0
        processed_rows = 0

        while processed_rows < tam:
            for i in range(1, numProc):
                sent_rows = min(NROWS, tam - current_row)

                comm.send(sent_rows, dest=i, tag=1)
                comm.send(current_row, dest=i, tag=2)
                comm.send(matrixB, dest=i, tag=3)

                current_row += sent_rows

            for i in range(1, numProc):
                sent_rows = min(NROWS, tam - processed_rows)

                received_data = comm.recv(source=i, tag=4)
                received_rows, received_matrix = received_data

                matrixC[processed_rows : processed_rows + received_rows, :] = received_matrix

                processed_rows += received_rows

        if PRINT:
            print("Matrix C:")
            print(matrixC)
            print("\n\n")

    else:
        while True:
            sent_rows = comm.recv(source=MASTER, tag=1)

            if sent_rows == END_OF_PROCESSING:
                break

            current_row = comm.recv(source=MASTER, tag=2)
            matrixB = comm.recv(source=MASTER, tag=3)

            matrixA = np.zeros((sent_rows, tam), dtype=int)
            matrixC = np.zeros((sent_rows, tam), dtype=int)

            comm.Recv(matrixA, source=MASTER, tag=5)

            for i in range(sent_rows):
                for j in range(tam):
                    matrixC[i, j] = np.dot(matrixA[i, :], matrixB[:, j])

            comm.send((sent_rows, matrixC), dest=MASTER, tag=4)

    MPI.Finalize()

main()
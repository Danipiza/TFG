from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Function to split indices evenly among workers
def split_indices(total_indices, num_workers):
    indices_per_worker = total_indices // num_workers
    remainder = total_indices % num_workers
    indices = []
    start = 0
    for i in range(num_workers):
        end = start + indices_per_worker
        if i < remainder:
            end += 1
        indices.append((start, end))
        start = end
    return indices

if rank == 0:  # Master process
    array_size = 20
    array = np.arange(array_size)
    indices_to_multiply = split_indices(array_size, size - 1)

    for i, worker_rank in enumerate(range(1, size)):
        comm.send(array, dest=worker_rank)
        comm.send(indices_to_multiply[i], dest=worker_rank)

    results = []
    for _ in range(len(indices_to_multiply)):
        results.append(comm.recv())

    print("Results from workers:", results)

else:  # Worker processes
    array = comm.recv(source=0)
    indices = comm.recv(source=0)

    result = np.prod(array[indices[0]:indices[1]])  # Calculate product
    comm.send(result, dest=0)

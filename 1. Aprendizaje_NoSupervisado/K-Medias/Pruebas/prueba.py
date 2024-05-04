from mpi4py import MPI
import math

n=10000
k=10
d=2


timeStart=MPI.Wtime()
for i in range(n):
    for j in range(k):
        x=0
        for a in range(d):
            x+=(1000-10)**2
        dist=math.sqrt(x)
        

timeEnd=MPI.Wtime()
print("Tiempo de ejecucion D. Euclidea:",(timeEnd-timeStart))
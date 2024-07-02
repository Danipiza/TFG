from mpi4py import MPI
import math
import random

def aleatorio(n, k):
    c=[]
    for i in range(n):
        tmp=[]
        for j in range(k):
            tmp.append(random.randint(1,10))
        c.append(tmp)
    return c
    



def main():
    
    k=2
    
    
    c1=aleatorio(750, k)
    c2=aleatorio(750, k)

    
    timeStart=MPI.Wtime()
    
    aux=0.0
    nDist=float("inf")
    c1N=len(c1)
    c2N=len(c2)
    for x in range(c1N):            # Recorre los individuos de "c1"
        for y in range(c2N):    # Recorre los individuos de "i2 (individuo a cambiar de la fila)
            distTMP=0
            for a in range(k):                                
                distTMP+=(c1[x][a]-c2[y][a])**2                
            if distTMP<nDist: nDist=distTMP # Coge la menor distancia entre el individuo "c1" e "i"                                
    distancia=math.sqrt(nDist)
    print("Distancia:",distancia)

    timeEnd=MPI.Wtime()

    print("Tiempo de ejecucion: {}\n".format(timeEnd-timeStart))


main()


print("Prueba")


from mpi4py import MPI
import os

# COMPILAR
# mpiexec -np 5 python MergeSortMPI.py

def main():
    MASTER = 0
    END_OF_PROCESSING=-2

    timeStart=0.0
    timeEnd=0.0

    a=[]
    b=[]
    n=0

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1
    
    if myrank==MASTER:
        a,n=leeArchivo()
        m=potencia_lb(numWorkers)
        if m!=numWorkers:
            print("Eliminando {} workers para que haya potencias de 2 workers.".format(numWorkers-m))
            for i in range(m+1,numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)
            numWorkers-=numWorkers-m

    timeStart=MPI.Wtime()
    if myrank==MASTER:
        tamProc=n//numWorkers
        modulo=n%numWorkers
        izq=0
        der=tamProc+1
        if tamProc>=1:
            for i in range(1,modulo+1):
                comm.send(a[izq:der],dest=i)
                izq+=tamProc+1
                der+=tamProc+1
            der-=1
            for i in range(modulo+1,numWorkers+1):
                comm.send(a[izq:der],dest=i)
                izq+=tamProc
                der+=tamProc
        else:
            for i in range(1, modulo+1):
                comm.send(a[izq],dest=i)
                izq+=1
            for i in range(modulo+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)
            numWorkers-=numWorkers-modulo

        workersList=[(i) for i in range(1,numWorkers+1)]
        while numWorkers!=1:
            tmp=[]
            for i in range(0,numWorkers):
                if i%2==0: 
                    comm.send(workersList[i+1],dest=workersList[i])
                    tmp.append(workersList[i])
                else: comm.send(workersList[i-1],dest=workersList[i])
            numWorkers//=2
            workersList=tmp
        comm.send(-1,dest=1)
        a = comm.recv(source=1, tag=tag,status=status)
        timeEnd = MPI.Wtime()
        print("Tiempo de ejecucion:", timeEnd-timeStart)
        if arrayOrdenado(a,n): print("Array ordenado")
        else: print("Array no ordenado")
    else: 
        a=comm.recv(source=0)
        if a==END_OF_PROCESSING: exit(0)
        n = len(a)
        minE=0
        pos=0
        for i in range(n-1):
            minE=a[i]
            pos=i
            for j in range(i+1, n):
                if minE>a[j]:
                    minE=a[j]
                    pos=j
            tmp=a[i]
            a[i]=a[pos]
            a[pos]=tmp
        while(True):
            tmp=comm.recv(source=MASTER)
            if tmp==-1:
                comm.send(a,dest=MASTER)
                break
            elif tmp>myrank: 
                b=comm.recv(source=tmp)
            else :
                comm.send(a,dest=tmp)
                break
            i=0
            j=0
            aux=[]
            n=len(a)
            m=len(b)
            while i<n and j<m:
                if a[i]<=b[j]:
                    aux.append(a[i])
                    i+=1
                else :
                    aux.append(b[j])
                    j+=1
            while i<n:
                aux.append(a[i])
                i+=1
            while j<m:
                aux.append(b[j])
                j+=1
            a=aux            
    MPI.Finalize()



def leeArchivo():
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    tfg_directorio=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))))    
    nombre_fichero=input("Introduce un nombre del fichero: ")    
    path=os.path.join(tfg_directorio, ".Otros","ficheros","No_Ordenados", nombre_fichero+".txt")
    
       
    tam=0    
    array = [] 
    try:        
        with open(path, 'r') as archivo: # modo lectura
            for linea in archivo: # Solo hay una linea                
                numeros_en_linea = linea.split() # Divide por espacios                               
                for numero in numeros_en_linea:
                    array.append(int(numero))
                    tam+=1
    
    except FileNotFoundError:
        print("El archivo '{}' no existe.".format(nombre_fichero+".txt"))
    
    return array, tam

   


def arrayOrdenado(a, n):
    """
    a: int[]    El array a comprobar
    n: int      Tamaño del array
    return.     True or False
    """
    for i in range(1,n):    
        if (a[i]!=a[i-1]+1):return False
    
    return True

def potencia_lb(n) :
    pot=1
    while 1:
        if pot*2<=n:
            pot*=2
        else : return pot

main()
from mpi4py import MPI
import os
import math

# mpiexec -np 5 python p2.py


def lee(archivo):

    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","Cluster", archivo+".txt")

    with open(path, 'r') as file:
        content = file.read()

    array = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')      
    for i in range(0, len(datos), 2):
        x = float(datos[i])
        y = float(datos[i + 1])

        array.append([x, y])

    #print("\n",array)        
    
    return array
 


def main():      
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    n=0

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1


    # Inicializa centros
    if myrank==MASTER: 
        poblacion=lee("1000_2D")                        
        n=len(poblacion)  
        print(n)
    
    # Envia el numero de clusters a los workers
    n=comm.bcast(n, root=MASTER)
    
    timeStart = MPI.Wtime()
    
    
    if myrank==MASTER:       
        tam=n//numWorkers
        M=[]
        for i in range(1,numWorkers+1):
            comm.send(tam, dest=i)
            
        
        
        
        for i in range(1,numWorkers+1):
            datos = comm.recv(source=i)
            for x in datos:
                M.append(x)
            comm.send(END_OF_PROCESSING, dest=i)
            
                
        timeEnd = MPI.Wtime()
        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))

    
    else : # WORKER
        while True:            
            a=comm.recv(source=MASTER)
            if(a==END_OF_PROCESSING): exit(0)
            
            data=[]
            for i in range(a):
                tmp=[-1 for _ in range(n//2)]          

                for j in range(n//2):
                    ret=0.0
                    for _ in range(2):
                        ret+=(1.98324-0.032901)**2        
                    
                    tmp.append(math.sqrt(ret))
                data.append(tmp)

            comm.send(data, dest=MASTER)

        

    



main()
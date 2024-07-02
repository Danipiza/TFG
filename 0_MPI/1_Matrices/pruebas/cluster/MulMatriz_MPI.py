from mpi4py import MPI
import sys
import os
import random

# EJECUTAR
# mpiexec -np 5 python MulMatriz_MPI.py


"""
Prueba de Multiplicacion de matrices.

Genera las matrices de manera aleatoria, y mide el tiempo de ejecucion. 
Mide el tiempo para los siguientes numeros de filas = [200,250,500,1000,1500,2000,2500,3000,3500,4000,4500,5000]
"""

# Generar matriz aleatoria
def genera_matriz(valor_maximo, n):
    ret=[[random.randint(0,valor_maximo) for _ in range(n)] for _ in range(n)]
    return ret


def main():    
    MASTER = 0              # int.      Master 
    PRINT = False           # boolean.  Imprimir matrices
    END_OF_PROCESSING = -1  # End of processing
    

    filas,columnas=0,0
    valor_maximo = 10  
    

    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1
    

    matrizA=[]
    matrizB=[]
    A=[]
    B=[]
    if myrank == MASTER:

        # Generate matrix A			
        #print("Generando matriz A ({}x{})".format(filas,columnas))        
        #matrizA=genera_matriz(valor_maximo,filas,columnas)
        filas=5000
        columnas=5000
        matrizA=genera_matriz(10,filas)        
        print("Matriz A ({}x{})".format(filas,columnas))
        
        if PRINT:
            print("Matriz A:\n")
            #print_matriz(matrizA)
            print(matrizA)
            print("\n\n")
        
        m=len(matrizA[0])

        # Generate matrix B
        #print("Generando matriz B ({}x{})".format(filas,columnas))        
        #matrizB = genera_matriz(valor_maximo,filas,columnas)
        
        matrizB=genera_matriz(10,filas)  
        print("Matriz B ({}x{})".format(filas,columnas))        
        if PRINT:
            print("Matriz B:")
            #print_matriz(matrizB)
            print(matrizB)
            print("\n")
        
      
    procesa=[200,250,500,1000,1500,2000,2500,3000,3500,4000,4500,5000]
    ruta_pruebas=os.path.dirname(os.path.abspath(__file__))

    for x in procesa:
        if myrank==0:
            A=[[matrizA[i][j] for j in range(x)] for i in range(x)]        
            B=[[matrizB[i][j] for j in range(x)] for i in range(x)]  
            matrizC = [[] for _ in range(x)]

        timeStart = MPI.Wtime()

        B=comm.bcast(B, root=MASTER) 
        filas=x

        

        if myrank==MASTER:
            # Init
            filaAct=0
                
            if numWorkers<=filas:  
                for i in range(1, numWorkers+1):                           
                    # Envia val
                    comm.send(filaAct, dest=i)
                    comm.send(A[filaAct], dest=i)                
                    # update
                    filaAct+=1        
            else:
                aux=numWorkers%filas
                for i in range(1, numWorkers-aux+1):                      
                    # Envia val
                    comm.send(filaAct, dest=i)
                    comm.send(A[filaAct], dest=i)                
                    # update
                    filaAct+=1							
                for i in range(numWorkers-aux+1, numWorkers+1):
                    comm.send(END_OF_PROCESSING, dest=i)                 
                
                
                numWorkers-=aux
            
            while True:	
                # Recibe los resultados de algun worker
                filaInd=comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)            
                source_rank=status.Get_source()
                filaC = comm.recv(source=source_rank, tag=tag,status=status)
                
                # Procesa los datos recibidos
                matrizC[filaInd]=filaC


                # Envia el siguiente valor a procesar 
                if filaAct<filas:
                    comm.send(filaAct, dest=status.source)
                    comm.send(A[filaAct], dest=status.source)   
                    # Update
                    filaAct+=1
                else:
                    comm.send(END_OF_PROCESSING, dest=status.source)
                    for i in range(numWorkers-1):
                        filaInd=comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)            
                        source_rank=status.Get_source()
                        filaC = comm.recv(source=source_rank, tag=tag,status=status)
                        comm.send(END_OF_PROCESSING, dest=status.source)
                    break


            
            timeEnd = MPI.Wtime()
            
            for i in range(1,numWorkers+1):
                comm.send(0,dest=i)
            
            ruta=os.path.join(ruta_pruebas,"Mul_Matriz_MPI{}.txt".format(numProc))    
            with open(ruta, 'a') as archivo:                               
                archivo.write(str(timeEnd-timeStart) + ', ')
            
            
            
        else: # Workers
            while True:
                # Recibe datos
                filaInd=comm.recv(source=0) # int.                     
                if filaInd==-1: break        
                filaA=comm.recv(source=0) # int[].                           
                
                
                tmp=0
                filaC=[]
                
                # TODO
                for i in range(x):
                    
                    for j in range(x):
                        tmp+=filaA[j]*B[j][i]
                    filaC.append(tmp)
                    tmp=0                            

                # Envia resultados
                comm.send(filaInd, dest=0)
                comm.send(filaC, dest=0)

            comm.recv(source=MASTER)
                    
            
    

    


    

main()
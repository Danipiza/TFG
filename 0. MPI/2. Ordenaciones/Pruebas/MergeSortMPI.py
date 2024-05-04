from mpi4py import MPI
import sys
import os

# COMPILAR
# mpiexec -np 5 python MergeSortMPI.py

# Este programa inicialmente tiene (np-1) workers. Pasa por un preprocesado para 
#   tener potencias de 2 workers, haciendo una aproximacion hacia abajo de la ultima
#   potencia alcanzada

# Este programa combina los algoritmos de SelectionSort y MergeSort. 
# Cada worker se encarga primero de ordenar por el metodo de SelectionSort la parte del array recibida 
#   del master. Una vez esta ordenado empieza el proceso de intercambio de mensajes entre workers. 
# El master indica a cada worker que tienen que hacer. 
#   - Si reciben un identificador mayor a su id, tienen que esperar a recibir un array de otro worker, para 
#       ordenar y almacenar ambos arrays (el suyo y el recibido). 
#   - Si reciben un identificador menor a su id, tienen que enviar su array ordenado al worker con ese identificador
#       y terminar su ejecucion.
# Con cada iteracion el master reduce el numero de workers hasta que solo quede uno, y este envie al master
#   el array entero ordenado.

datos=[]
tamArray=[]

# Signal handler 
def signal_handler(sig, frame):
    print("Ctrl+C, almacenando en ")
    guarda_datos(["MergeSortMPI.txt",
                  "TamArray.txt"])
    sys.exit(0)

def guarda_datos(archivo):    
    print(tamArray)
    for x in datos:
        print(x,"\n")
    

    with open(archivo[0], 'w') as file:
        for i, val in enumerate(datos):
            file.write("{}, ".format(val))
        file.write("\n")
    with open(archivo[1], 'w') as file:
        for i, val in enumerate(tamArray):
            file.write("{}, ".format(val))
        file.write("\n")
    
   

def main():  	
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    # Arrays 
    a=[]                    # int[].    Array de Entrada             
    b=[]                    # int[].    Array de Salida
    n=0                     # int.      Tamaño de los arrays       

                      		    

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1
    numWs=numWorkers
   		
    # Master lee el archivo .txt con el array de entrada.
    # Tambien hace al aproximacion del numero de workers a la potencia.
    if myrank==MASTER: 
        #a,n=leeArchivo("100000Desc",None)   
        n=300000
        a=[i for i in range(n,-1,-1)]
        
        m=potencia_lb(numWorkers)
        if m!=numWorkers: 
            print("Eliminando {} workers para que haya potencias de 2 workers.".format(numWorkers-m))
            for i in range(m+1,numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)
            numWorkers-=numWorkers-m
    
    #procesar=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]
    procesar=[n]
    for x in procesar: 
        # Comienza el timer, una vez inicializado todo
        timeStart = MPI.Wtime()

        if myrank==MASTER:
            b=[]
            for val in a[0:x]:
                b.append(val)
            n=len(b)
        

        if myrank==MASTER:      
            
            
            tamProc=n//numWorkers
            modulo=n%numWorkers
            izq=0
            der=tamProc+1

            if tamProc>=1:  
                for i in range(1, modulo+1):                
                    comm.send(b[izq:der],dest=i)               
                    izq+=tamProc+1
                    der+=tamProc+1
                der-=1

                for i in range(modulo+1,numWorkers+1):
                    comm.send(b[izq:der],dest=i)
                    izq+=tamProc
                    der+=tamProc    
            else:
                for i in range(1, modulo+1):   
                    comm.send(b[izq], dest=i)   
                    izq+=1							
                for i in range(modulo+1, numWorkers+1):
                    comm.send(END_OF_PROCESSING, dest=i)   
                       
            workersList=[(i) for i in range(1,numWorkers+1)]       
            while numWorkers != 1:
                tmp=[]
                for i in range(0,numWorkers):
                    if i%2==0: 
                        comm.send(workersList[i+1],dest=workersList[i])
                        tmp.append(workersList[i]) 
                    else: comm.send(workersList[i-1],dest=workersList[i])
                numWorkers//=2 
                workersList=tmp 
            
            comm.send(-1,dest=1)    
            b = comm.recv(source=1, tag=tag,status=status)
            timeEnd = MPI.Wtime()

            for i in range(1,numWs+1):
                comm.send(0,dest=i)
            numWorkers=numWs

            print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
            if arrayOrdenado(b,n): print("Array ordenado.")
            else: print("Array NO ordenado.")
            datos.append((timeEnd-timeStart))
            tamArray.append(n)
            
        else: 
            
            a=comm.recv(source=0) 
            if a!=END_OF_PROCESSING: 
                

                # -----------------------------
                # Ordena mediante SelectionSort        
                n = len(a)
                minE = 0
                pos = 0
                for i in range(n-1):
                    minE = a[i]
                    pos = i
                    for j in range(i+1, n):
                        if minE > a[j]:
                            minE = a[j]
                            pos = j            
                    tmp = a[i]
                    a[i] = a[pos]
                    a[pos] = tmp
                # -----------------------------        
                while(True):                       
                    tmp=comm.recv(source=MASTER)
                    if tmp==-1:
                        comm.send(a,dest=MASTER)
                        break
                    elif tmp>myrank: b=comm.recv(source=tmp)                
                    else :
                        comm.send(a,dest=tmp) 
                        break
                    
                    # ----------------------------
                    # Proceso merge() de MergeSort
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
                    # ----------------------------
            
            comm.recv(source=MASTER)

    if myrank==MASTER:
        guarda_datos(["MergeSort_MPI{}.txt".format(numWorkers),"TamArray.txt"])  
            
    MPI.Finalize()



def leeArchivo(archivo, carpeta):
    """
    archivo: string     Archivo a leer
    carpeta: string     Carpeta en el que se encuentra (Ordenado, No_Ordenado)

    return =>
    array: int[].       Array con los enteros leidos
    tam: int.           Tamaño del array leido
    """
    
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)


    if carpeta==None: carpeta="Ordenado"
    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","1.Array", carpeta, archivo+".txt")
    print(path)
       
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
        print("El archivo '{}' no existe.".format(archivo+".txt"))
    
    return array, tam

   


def arrayOrdenado(a, n):
    """
    a: int[]        El array a comprobar
    n: int          Tamaño del array

    return => bool  True or False
    """

    for i in range(1,n):    
        if (a[i]<a[i-1]):return False
    
    return True

def potencia_lb(n) :
    pot=1
    while 1:
        if pot*2<=n:
            pot*=2
        else : return pot

main()

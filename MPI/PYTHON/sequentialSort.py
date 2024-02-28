from mpi4py import MPI
import math
import time

# TODO FALTA TERMINARLO

#define MASTER 0 # Master process
#define END_OF_PROCESSING 0 # End of processing

# COMPILAR
# mpirun -np 5 python <name>.py

int* leeArchivo(int* n);
void printArray(int* a, int n);

# PROBAR, AL ENVIAR DATOS, 
# - ES MAS EFICIENTE ENVIAR UNA PARTE DEL ARRAY
# - PONERLO COMO VARIABLE GLOBAL
# - ENVIAR TODO EL ARRAY CON MPI_Bcast()


def worker():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
        
    
    
    mensaje = comm.recv(source=0)   # Recibe        
    comm.send(resultado, dest=0)    # Envia

def master():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    
    n=100
    a=leeArchivo() 
    print("Padre:")
    #printArray(a, n)
    # MODIFICAR, POTENCIAS DE 2, LOG2 ...
    # ENVIA TAMAÑO DEL ARRAY QUE VAN A PROCESAR 
    MPI_Bcast (&n, 1, MPI_INT, MASTER, MPI_COMM_WORLD);  
    # ENVIA EL ARRAY ENTERO
    MPI_Bcast (a, n, MPI_INT, MASTER, MPI_COMM_WORLD);  
    
    
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

int main(int argc, char *argv[]){

  	myrank=0              		# int: RANK Y NUMERO DE PROCESOS
    numProc=0
	tag=1	    				# int: TAG 
	status=None			        # MPI_Status: MPI STATUS PARA RECIBIR MENSAJES 

    timeStart=0.0               # double: CALCULAR TIEMPO DE EJECUCION
    timeEnd=0.0	

    x=2
    a=[]                        # int[]: ARRAY 
    n=0                         # int: NUMERO DE ELEMENTOS EN EL ARRAY
    izq=0
    der=0                       
    arrayProc=0
    tamProc=0
    encontrado=False            # Boolean	
	
	i=0                         # int: Aux variables 
    j=0
    k=0				
		 

    

    # Init MPI
    MPI_Init (&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);	
    MPI_Comm_size(MPI_COMM_WORLD, &numProc); # DEVUELVE EL NUMERO DE HILOS AL EJECUTAR EL PROGRAMA

    # CONTROL DE ERRORES
    """if (){
        if (myrank == MASTER) {
            printf("Wrong configuration for NROWS (%d). SIZE (%d) < numWorkers(%d)*NROWS(%d)\n", NROWS, SIZE, numProc-1, NROWS);
            printf ("At least, each worker must receive %d rows to be processed\n", NROWS);
        }
        MPI_Finalize();
        exit(-1);			
    }"""

		
    # PROCESO master LEE EL ARCHIVO
    if (myrank == MASTER) {
        
    }
    else {
        # RECIBE TAMAÑO DEL ARRAY QUE VAN A PROCESAR LOS workers
        MPI_Bcast (&n, 1, MPI_INT, MASTER, MPI_COMM_WORLD);  
        a = (int*)malloc (n*sizeof(int)); 
        
        # RECIBE EL ARRAY ENTERO
        MPI_Bcast (a, n, MPI_INT, MASTER, MPI_COMM_WORLD); 
        printf("Hijo:\n");
        printArray(a, n);          
    }   
            
    # DESPUES DE ENVIAR/RECIBIR LOS DATOS COMIENZA EL TIMER
    timeStart = time.time() #MPI_Wtime();

		# PROCESO master
		if (myrank == MASTER){
			# INIT
			arrayProc=0;
            # CAMBIAR VALORES
            tamProc=log2(n);

			# DISTRIBUIR INICIALMENTE
			for (i=1; i<numProc; i++) {
				# SEND IZQ
                MPI_Send (&arrayProc, 1, MPI_INT, i, tag, MPI_COMM_WORLD);
                # UPDATE
                arrayProc+=tamProc-1;
                # SEND DER
                MPI_Send (&arrayProc, 1, MPI_INT, i, tag, MPI_COMM_WORLD);
                arrayProc++;							
			}

			# MIENTRAS QUE HAYA ELEMENTOS POR PROCESAR
			while (arrayProc < n) {			
				# RECIBE RESULTADOS DE UNA BUSQUEDA
                printf("PADRE. Esperando\n");
                MPI_Recv (&encontrado, 1, MPI_INT, MPI_ANY_SOURCE, tag, MPI_COMM_WORLD, &status);	
                printf("PADRE. Recibe: %d\n", &encontrado);
                # FIN
                if(encontrado!=-1){
                    printf("Se ha encontrado el elemento en la posicion %d, del array\n", encontrado);
                    timeEnd = time.time() #MPI_Wtime();
                    #MPI_Abort(MPI_COMM_WORLD, 0);
                }			

				# ENVIAR SIGUIENTES DATOS				
                # SEND IZQ                
                MPI_Send (&arrayProc, 1, MPI_INT, status.MPI_SOURCE, tag, MPI_COMM_WORLD);
                # UPDATE
                if(arrayProc+tamProc>=n) arrayProc=n-1;
                else arrayProc+=tamProc-1;                    
                # SEND DER                
                MPI_Send (&arrayProc, 1, MPI_INT, status.MPI_SOURCE, tag, MPI_COMM_WORLD);
                arrayProc++;	
                #printf("PADRE. arrayProc: %d\n", arrayProc);							
			}

            if encontrado==False:
			    timeEnd = time.time() #MPI_Wtime();				
                printf("No se ha encontrado el elemento buscado\n");
            		
            printf("Tiempo de ejecucion: %f\n", timeEnd-timeStart);			
		}		
		else { # workers
            while(encontrado==-1){
                printf("HIJO. Elemento a buscar %d\n",x);
                # RECIBE IZQ
                MPI_Recv (&izq, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD, &status);                
                # RECIBE DER
                MPI_Recv (&der, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD, &status);
                printf("HIJO, %d. izq: %d, der: %d\n", myrank, izq, der);
                if(izq>=n) break;
                if(der>=n) der=n-1;
                
                for(;izq<=der&&encontrado==-1;izq++){
                    printf("Valor de a[i]: %d\n",a[izq]);
                    if(a[izq]==x) encontrado=izq;
                }
               
                MPI_Send(&encontrado, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD);
                printf("HIJO, %d. Envia encontrado: %d\n", myrank, encontrado);                
            }
        
		}
		
		# End MPI environment
  		MPI_Finalize();

    return 0;
}



def leeArchivo():
    file_name = input("Enter the name of the file: ")

    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            integers = []

            for line in lines:
                try:
                    integer = int(line.strip())
                    integers.append(integer)
                except ValueError:
                    print(f"Ignoring non-integer value: {line.strip()}")

            return integers
    except FileNotFoundError:
            print("File not found.")
        return []

def printArray(a, n):
    print("Array:")
    for i in range(n):
        print(a[i], end="")    
    print()





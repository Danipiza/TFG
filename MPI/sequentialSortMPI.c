#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <mpi.h>
#include <limits.h>

#define MASTER 0 // Master process
//#define END_OF_PROCESSING -2 // End of processing
#define INF INT_MAX

// COMPILAR
// mpicc sequentialSortMPI.c -o sequentialSortMPI -lm
// mpiexec -n 5 ./sequentialSortMPI

/*
IDEA: EL PROCESO master, GESTIONA EL PROCESO, CADA worker RECORRE EL ARRAY ENTERO CON SU ELEMENTO, 
Y COMPARA LOS DEMAS ELEMENTOS, SUMANDO A UN CONTADOR PARA QUE SE LO DEVUELVA AL master Y ESTE LO COLOQUE 
EN SU POSICION CORRECTA EN OTRO ARRAY.

*/

int* leeArchivo(int* n);
void printArray(int* a, int n);
int arrayOrdenado(int* a, int n); 

int main(int argc, char *argv[]){
    // Variables MPI
  	int myrank, tag, numProc,numWorkers;	// rank y tag de MPI y el numero de procesos creados (el primero es el master)
    MPI_Status status;			            // status para mas info 
                                                // (entre esta info esta el proceso que recibe al usar anysource)
    int END_OF_PROCESSING=-2;

    // Variable para calculo de tiempo de ejecucion
    double timeStart, timeEnd;	

    // Arrays dinamicos
    int* a;                         // Entrada
    int* b;                         // Salida
    // tamaño de los arrays 
    int n;                          
    
    // Variables del proceso MPI
    int arrayProc;                  // Puntero de la parte procesada del array a
    int pos=-1, val;                // Variables que se envian y reciben entre los procesos
    int cont;                       // Variable auxiliar para los workers, que cuentan los elementos mayores al recibido

	int i;      				    // Variable para los bucles
		 
    // Init
    tag = 1;
    srand(time(NULL));

    // Init MPI
    MPI_Init (&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);	
    MPI_Comm_size(MPI_COMM_WORLD, &numProc); // Numero de procesos al ejecutar el programa
    numWorkers=numProc-1;

    // CONTROL DE ERRORES
    /*if (<Error>){
        if (myrank == MASTER) {
            printf("Wrong configuration for NROWS (%d). SIZE (%d) < numWorkers(%d)*NROWS(%d)\n", NROWS, SIZE, numProc-1, NROWS);
            printf ("At least, each worker must receive %d rows to be processed\n", NROWS);
        }
        MPI_Finalize();
        exit(-1);			
    }*/
		
    // master lee el archivo .txt con el array de entrada
    // cuenta el tamaño del array de entrada e inicializa el array de salida
    if (myrank == MASTER) {
        a=leeArchivo(&n); 

        // Init b
        b=(int *)malloc(n*sizeof(int));
        for(i=0;i<n;i++) b[i]=INF;

        // Envia el tamaño de los arrays a los workers
        MPI_Bcast (&n, 1, MPI_INT, MASTER, MPI_COMM_WORLD);  
        // Envia el array entero a los workers
        MPI_Bcast (a, n, MPI_INT, MASTER, MPI_COMM_WORLD);  
    }
    else {
        // Recibe el tamaño de los arrays
        MPI_Bcast (&n, 1, MPI_INT, MASTER, MPI_COMM_WORLD);         
        
        a = (int*)malloc (n*sizeof(int)); // Reserva memoria              
        // Recibe el array entero
        MPI_Bcast (a, n, MPI_INT, MASTER, MPI_COMM_WORLD); 
    }   
            
    // Comienza el timer una vez inicializado todo
    timeStart = MPI_Wtime();

    if (myrank == MASTER){
        // Init
        arrayProc=0;        

        // Distribucion inicial
        if(numWorkers<=n){        
            for (i=1;i<=numWorkers;i++) {            
                // Envia val
                MPI_Send(&a[arrayProc], 1, MPI_INT, i, tag, MPI_COMM_WORLD);
                // update
                arrayProc++;							
            }
        }
        else {
            int aux=numWorkers%n;
            for (i=1;i<=numWorkers-aux;i++) {            
                // Envia val
                MPI_Send(&a[arrayProc], 1, MPI_INT, i, tag, MPI_COMM_WORLD);
                // update
                arrayProc++;							
            }
            for(i=numWorkers-aux+1;i<=numWorkers;i++){
                MPI_Send(&END_OF_PROCESSING, 1, MPI_INT, i, tag, MPI_COMM_WORLD);
            }
            numWorkers-=aux;
        }

        // Hay mas elementos a procesar
        while (arrayProc < n) {		
            pos=-1;	
            // Recibe los resultados de algun worker
            MPI_Recv (&pos, 1, MPI_INT, MPI_ANY_SOURCE, tag, MPI_COMM_WORLD, &status);	            
            MPI_Recv (&val, 1, MPI_INT, status.MPI_SOURCE, tag, MPI_COMM_WORLD, &status);
            
            // Fin
            if(arrayProc==n) break;		

            // Procesa los datos recibidos
            // Si la posicion en el array b esta ocupado, es porque es el mismo valor
            // y busca el siguiente espacio disponible
            while(b[pos]!=INF) pos++;
            b[pos]=val;


            // Envia el siguiente valor a procesar       
            MPI_Send (&a[arrayProc], 1, MPI_INT, status.MPI_SOURCE, tag, MPI_COMM_WORLD);
            // Update
            arrayProc++;							
        }

        // Ultimos valores por procesar
        while(numWorkers--){
            MPI_Recv (&pos, 1, MPI_INT, MPI_ANY_SOURCE, tag, MPI_COMM_WORLD, &status);	            
            MPI_Recv (&val, 1, MPI_INT, status.MPI_SOURCE, tag, MPI_COMM_WORLD, &status);
            while(b[pos]!=INF) pos++;
            b[pos]=val;
            MPI_Send(&END_OF_PROCESSING, 1, MPI_INT, status.MPI_SOURCE, tag, MPI_COMM_WORLD); 
        }
        timeEnd = MPI_Wtime();
        printf("Tiempo de ejecucion: %f\n", timeEnd-timeStart);	
        if(arrayOrdenado(b,n)) printf("Array ordenado\n");
        else printf("Array no ordenado\n");
    }		
    else { // workers
        while(1) {
            // Recibe el valor del array a procesar
            MPI_Recv (&val, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD, &status);
            if(val==-2) break;

            cont=0;
            for(i=0;i<n;i++){
                if(a[i]<val) cont++;
            }
            
            MPI_Send(&cont, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD);
            MPI_Send(&val, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD);               
        }    
    }
		// End MPI environment
  		MPI_Finalize();

    return 0;
}



// cambiar el metodo de seleccionar .txt, usando argv[]
int* leeArchivo(int* n){
    int arrayTam=0;
    int capacidad=10;
    int* a=(int*)malloc(capacidad*sizeof(int));
    if (a == NULL) {
        perror("Error al asignar memoria. 1er");
        exit(EXIT_FAILURE);
    }

    FILE *archivo;
    char nombre_archivo[100];
    int archivoTam;      
    printf("Introduce el nombre del archivo: ");
    scanf("%s", nombre_archivo);
    archivoTam = strlen(nombre_archivo);
    strcat(nombre_archivo, ".txt");

    archivo = fopen(nombre_archivo, "r"); // Modo lectura
    if (archivo == NULL) {
        perror("Error al abrir el archivo");
        exit(EXIT_FAILURE);
    }

    int tmp;
    while (fscanf(archivo, "%d", &tmp) == 1) {        
        if (arrayTam == capacidad) {
            capacidad *= 2;
            a = (int*)realloc(a, capacidad * sizeof(int));
            if (a == NULL) {
                perror("Error al reasignar memoria");
                exit(EXIT_FAILURE);
            }
        }

        a[arrayTam++] = tmp;        
    }

    /*for (int i = 0; i < n; i++) {
        fscanf(archivo, "%d", &a[i]);
    }*/  
    fclose(archivo); 

    *n=arrayTam;
    return a;
}

void printArray(int* a, int n){
    printf("Array:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", a[i]);
    }
    printf("\n");
}

int arrayOrdenado(int* a, int n){
    for(int i=1;i<n;i++){
        if(a[i]!=a[i-1]+1)return 0;
    }
    return 1;
}
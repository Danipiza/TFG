#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <mpi.h>

#define MASTER 0 // Master process
#define END_OF_PROCESSING 0 // End of processing

// COMPILAR
// mpicc sequentialSearchMPI.c -o sequentialSearchMPIc -lm

int* leeArchivo(int* n);
void printArray(int* a, int n);

// PROBAR, AL ENVIAR DATOS, 
// - ES MAS EFICIENTE ENVIAR UNA PARTE DEL ARRAY
// - PONERLO COMO VARIABLE GLOBAL
// - ENVIAR TODO EL ARRAY CON MPI_Bcast()


int main(int argc, char *argv[]){

  	int myrank, numProc;		// RANK Y NUMERO DE PROCESOS
	int tag;					// TAG 
	MPI_Status status;			// MPI STATUS PARA RECIBIR MENSAJES 

    double timeStart, timeEnd;	// CALCULAR TIEMPO DE EJECUCION

    int x=2;
    int* a;                     // ARRAY DINAMICO
    int n,izq,der;              // NUMERO DE ELEMENTOS EN EL ARRAY
    int arrayProc, tamProc;
    int encontrado=-1;


	int sentRows;				/** Number of rows sent */
	int currentRow;				/** Current row being processed */
	int processedRows;			/** Number of currently processed rows */
	int i, j, k;				/** Aux variables */	
		 

    // Init
    tag = 1;
    srand(time(NULL));

    // Init MPI
    MPI_Init (&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);	
    MPI_Comm_size(MPI_COMM_WORLD, &numProc); // DEVUELVE EL NUMERO DE HILOS AL EJECUTAR EL PROGRAMA

    // CONTROL DE ERRORES
    /*if (){
        if (myrank == MASTER) {
            printf("Wrong configuration for NROWS (%d). SIZE (%d) < numWorkers(%d)*NROWS(%d)\n", NROWS, SIZE, numProc-1, NROWS);
            printf ("At least, each worker must receive %d rows to be processed\n", NROWS);
        }
        MPI_Finalize();
        exit(-1);			
    }*/

		
    // PROCESO master LEE EL ARCHIVO
    if (myrank == MASTER) {
        a=leeArchivo(&n); 
        printf("Padre:\n");
        printArray(a, n);
        // MODIFICAR, POTENCIAS DE 2, LOG2 ...
        // ENVIA TAMAÑO DEL ARRAY QUE VAN A PROCESAR 
        MPI_Bcast (&n, 1, MPI_INT, MASTER, MPI_COMM_WORLD);  
        // ENVIA EL ARRAY ENTERO
        MPI_Bcast (a, n, MPI_INT, MASTER, MPI_COMM_WORLD);  
    }
    else {
        // RECIBE TAMAÑO DEL ARRAY QUE VAN A PROCESAR LOS workers
        MPI_Bcast (&n, 1, MPI_INT, MASTER, MPI_COMM_WORLD);  
        a = (int*)malloc (n*sizeof(int)); 
        
        // RECIBE EL ARRAY ENTERO
        MPI_Bcast (a, n, MPI_INT, MASTER, MPI_COMM_WORLD); 
        printf("Hijo:\n");
        printArray(a, n);          
    }   
            
    // DESPUES DE ENVIAR/RECIBIR LOS DATOS COMIENZA EL TIMER
    timeStart = MPI_Wtime();

		// PROCESO master
		if (myrank == MASTER){
			// INIT
			arrayProc=0;
            // CAMBIAR VALORES
            tamProc=log2(n);

			// DISTRIBUIR INICIALMENTE
			for (i=1; i<numProc; i++) {
				// SEND IZQ
                MPI_Send (&arrayProc, 1, MPI_INT, i, tag, MPI_COMM_WORLD);
                // UPDATE
                arrayProc+=tamProc-1;
                // SEND DER
                MPI_Send (&arrayProc, 1, MPI_INT, i, tag, MPI_COMM_WORLD);
                arrayProc++;							
			}

			// MIENTRAS QUE HAYA ELEMENTOS POR PROCESAR
			while (arrayProc < n) {			
				// RECIBE RESULTADOS DE UNA BUSQUEDA
                printf("PADRE. Esperando\n");
                MPI_Recv (&encontrado, 1, MPI_INT, MPI_ANY_SOURCE, tag, MPI_COMM_WORLD, &status);	
                printf("PADRE. Recibe: %d\n", &encontrado);
                // FIN
                if(encontrado!=-1){
                    printf("Se ha encontrado el elemento en la posicion %d, del array\n", encontrado);
                    timeEnd = MPI_Wtime();
                    //MPI_Abort(MPI_COMM_WORLD, 0);
                }			

				// ENVIAR SIGUIENTES DATOS				
                // SEND IZQ                
                MPI_Send (&arrayProc, 1, MPI_INT, status.MPI_SOURCE, tag, MPI_COMM_WORLD);
                // UPDATE
                if(arrayProc+tamProc>=n) arrayProc=n-1;
                else arrayProc+=tamProc-1;                    
                // SEND DER                
                MPI_Send (&arrayProc, 1, MPI_INT, status.MPI_SOURCE, tag, MPI_COMM_WORLD);
                arrayProc++;	
                //printf("PADRE. arrayProc: %d\n", arrayProc);							
			}

            if(encontrado==-1) {
			    timeEnd = MPI_Wtime();				
                printf("No se ha encontrado el elemento buscado\n");
            }		
            printf("Tiempo de ejecucion: %f\n", timeEnd-timeStart);			
		}		
		else { // workers
            while(encontrado==-1){
                printf("HIJO. Elemento a buscar %d\n",x);
                // RECIBE IZQ
                MPI_Recv (&izq, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD, &status);                
                // RECIBE DER
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

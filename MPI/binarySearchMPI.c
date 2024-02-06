#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <mpi.h>
//#include <climits>

#define MASTER 0 // Master process
#define END_OF_PROCESSING -2 // End of processing
#define INF INT_MAX

// COMPILAR
// mpicc sequentialSearchMPI.c -o sequentialSearchMPIc -lm


/*
IDEA: EL PROCESO master GESTIONA X HILOS, [LOG2(n), log10(n),...], 
CADA worker COMPRUEBA EL FIN Y INI DE SUS PARTE A PROCESAR Y SI PUEDE 
ESTAR EL VALOR EN ESA SECCION, SE EXPANDE DE NUEVO CON ESOS VALORES

TIENE QUE ESTAR ORDENADO
*/

int* leeArchivo(int* n);
void printArray(int* a, int n);
int arrayOrdenado(int* a, int n); 

int main(int argc, char *argv[]){
    // Variables MPI
  	int myrank, tag, numProc;		// rank y tag de MPI y el numero de procesos creados (el primero es el master)
    MPI_Status status;			    // status para mas info 
                                        // (entre esta info esta el proceso que recibe al usar anysource)

    // Variable para calculo de tiempo de ejecicion
    double timeStart, timeEnd;	

    // Arrays dinamicos
    int* a;                         // Entrada
    // tamaño de los arrays 
    int n;      

    int x;                    
    
    // Variables del proceso MPI
    int punt, izq, der;
    int tamProc, modProc;
    int aux;

    int encontrado=-1;

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
        //printf("Padre:\n"); printArray(a, n);

        if(!arrayOrdenado(a,n)) {            
            printf ("El array de entrada tiene que estar ordenado\n");        
            MPI_Finalize();
            exit(-1);		
        }

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
        //printf("Hijo:\n"); printArray(a, n);          
    }   
            
    // Comienza el timer una vez inicializado todo
    timeStart = MPI_Wtime();

    if (myrank == MASTER){
        // Init
        punt=0;
        tamProc=n/numProc;  
        modProc=n%numProc;    

        // Distribucion inicial
        for (i=1; i<numProc-1; i++) {            
            // Envia izq
            MPI_Send (&punt, 1, MPI_INT, i, tag, MPI_COMM_WORLD);
            punt+=tamProc+((i-1)<modProc?1:0);
            MPI_Send (&punt, 1, MPI_INT, i, tag, MPI_COMM_WORLD);
            // update
            punt++;							
        }

        // Hay mas elementos a procesar
        while (encontrado==-1) {		
            //pos=-1;	
            // Recibe los resultados de algun worker
            //printf("PADRE. Esperando\n");
            izq=-1;
            for(int i=1;i<numProc;i++){
                MPI_Recv(&aux, 1, MPI_INT, i, tag, MPI_COMM_WORLD, &status);
                if (aux==-2){ // encontrado
                    MPI_Recv(&encontrado, 1, MPI_INT, i, tag, MPI_COMM_WORLD, &status);                    
                }
                else if(aux!=-1){
                    izq=aux;
                    MPI_Recv(&der, 1, MPI_INT, i, tag, MPI_COMM_WORLD, &status);
                }	            
            }            
            //printf("PADRE. Recibe, pos: %d, val: %d\n", pos, val);	
            
            // Fin
            if(izq==-1){
                printf("El valor: %d, no esta en el array\n", x);
            }
            else if(encontrado!=-1){
                printf("El valor: %d, esta en la posicion %d\n", x, encontrado);
            }

            if(arrayProc==n){
                printf("No hay mas elementos que procesar\n", encontrado);
                timeEnd = MPI_Wtime();
                for(int i=1;i<numProc;i++){
                    MPI_Send(END_OF_PROCESSING, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // amp?
                }
                //MPI_Abort(MPI_COMM_WORLD, 0);
            }		

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
        
        printf("Tiempo de ejecucion: %f\n", timeEnd-timeStart);	
        arrayOrdenado(b,n); // Comprueba si esta ordenado        		
    }		
    else { // workers
        while(pos!=-2) {
            //printf("HIJO. Elemento a buscar %d\n",x);
            // Recibe el valor del array a procesar
            MPI_Recv (&val, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD, &status);
            if(pos==-2) break;

            //printf("HIJO, %d. izq: %d, der: %d\n", myrank, izq, der);
            cont=0;
            for(i=0;i<n;i++){
                if(a[i]<pos) cont++;
            }
            
            MPI_Send(&cont, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD);
            MPI_Send(&val, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD); 
            printf("HIJO, %d. Envia la posicion: %d, con valor: %d\n", myrank, cont, val);               
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
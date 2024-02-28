#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <mpi.h>

#define MASTER 0 // Master process
#define INF INT_MAX


// COMPILAR
// mpicc binarySearchMPI.c -o binarySearchMPI -lm
// mpiexec -n <numProc> ./binarySearchMPI


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
  	int myrank, tag, numProc, numWorkers;		// rank y tag de MPI y el numero de procesos creados (el primero es el master)
    MPI_Status status;			    // status para mas info 
                                        // (entre esta info esta el proceso que recibe al usar anysource)
    int END_OF_PROCESSING = -2;

    // Variable para calculo de tiempo de ejecicion
    double timeStart, timeEnd;	

    // Arrays dinamicos
    int* a;                         // Entrada
    // tamaño de los arrays 
    int n;      

    int x=78;                    
    
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
        //printf("Padre:\n"); printArray(a, n);

        if(!arrayOrdenado(a,n)) {            
            printf ("El array de entrada tiene que estar ordenado\n");        
            MPI_Abort(MPI_COMM_WORLD,-1);
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
        tamProc=n/numWorkers;  
        modProc=n%numWorkers;    

        // Distribucion inicial
        if(tamProc>=1){
            for(i=1;i<=numWorkers;i++){
                printf("MASTER. envia izq: %d\n", punt);
                MPI_Send(&punt, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // Envia izq
                // Si el tamaño del array no es multiplo del nuumero de procesos, se asigna el espacio restante a los primeros
                punt+=tamProc-1+((i-1)<modProc?1:0); 
                printf("MASTER. envia der: %d\n", punt);
                MPI_Send(&punt, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // Envia der
                punt++;
            }
        }
        else {  // Hay mas procesos que elementos en el array
                // Se asigna un valor a los primeros procesos
            for(i=1;i<=modProc;i++){ 
                MPI_Send(&punt, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // Envia izq
                MPI_Send(&punt, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // Envia der
                punt++;
            }
            for(i=modProc+1;i<=numWorkers;i++){
                MPI_Send(&END_OF_PROCESSING, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // amp?
                numWorkers--; // Reduce en numero de workers activos
            }
        }


        // Todavia no ha finalizado la busqueda
        while (encontrado==-1) {	
            // Recibe los resultados de los workers activos
            punt=-1;
            for(int i=1;i<=numWorkers;i++) { // workers activos
                MPI_Recv(&aux, 1, MPI_INT, i, tag, MPI_COMM_WORLD, &status);
                if (aux==-2) { // valor encontrado
                    timeEnd = MPI_Wtime();
                    MPI_Recv(&encontrado, 1, MPI_INT, i, tag, MPI_COMM_WORLD, &status);                    
                }
                else if(aux!=-1) { // esta en el intervalo,
                    izq=aux;
                    punt=izq;
                    MPI_Recv(&der, 1, MPI_INT, i, tag, MPI_COMM_WORLD, &status);
                }	            
            }            	
            
            // Fin
            if(encontrado!=-1) { // Se ha encontrado el valor se mandan los mensajes de finalizacion a los workers activos
                printf("El valor: %d, esta en la posicion %d\n", x, encontrado);
                for(int i=1;i<=numWorkers;i++){
                    MPI_Send(&END_OF_PROCESSING, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // amp?
                }
                break;
            }
            else if(punt==-1) { // punt No se actualiza por lo que el valor existe en el array
                timeEnd = MPI_Wtime();
                printf("El valor: %d, no esta en el array\n", x);
                for(int i=1;i<=numWorkers;i++) {
                    MPI_Send(&END_OF_PROCESSING, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // amp?
                }
                break;
            }             
            	

            // Procesa los datos recibidos            
            tamProc=der-izq+1;
            modProc=tamProc%numWorkers;  
            tamProc=tamProc/numWorkers;  
            if(tamProc>=1){
                for(i=1;i<=numWorkers;i++){
                    MPI_Send(&punt, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // izq
                    punt+=tamProc-1+((i-1)<modProc?1:0);
                    MPI_Send(&punt, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // der
                    punt++;
                }
            }
            else { 
                for(i=1;i<=modProc;i++){
                    MPI_Send(&punt, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // izq
                    MPI_Send(&punt, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // der
                    punt++;
                }
                for(i=modProc+1;i<=numWorkers;i++){
                    MPI_Send(&END_OF_PROCESSING, 1, MPI_INT, i, tag, MPI_COMM_WORLD); // amp?
                    numWorkers--;
                }
            }             						
        }
        
        printf("Tiempo de ejecucion: %f\n", timeEnd-timeStart);	             		
    }		
    else { // workers
        while(1) {            
            // Recibe izq 
            MPI_Recv (&izq, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD, &status);
            if(izq==-2) break;
            // Recibe der
            MPI_Recv (&der, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD, &status);

            // Procesar
            encontrado=-1;            
            if(a[der]>=x&&a[izq]<=x) {
                encontrado=izq;
                if(a[der]==x) { encontrado=-2; pos=der; }
                else if(a[izq]==x) { encontrado=-2; pos=izq; }
            }
            
            
            MPI_Send(&encontrado, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD);
            if(encontrado==-2) MPI_Send(&pos, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD);
            else if(encontrado==izq) MPI_Send(&der, 1, MPI_INT, MASTER, tag, MPI_COMM_WORLD);
            //printf("HIJO, %d. Envia: %d\n", myrank, encontrado);               
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
        //if(a[i]!=a[i-1]+1) return 0;
        if(a[i]<a[i-1]) return 0;
    }
    return 1;
}
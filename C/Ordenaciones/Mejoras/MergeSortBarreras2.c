// 2. IMPLEMENTACION CON LOG(n) HILOS
// Si el numero de hilos es impar los ultimos ultimo hilo procesa 3 comparaciones de array

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>

#include <math.h> // log2, ceil (-lm) enlazar la biblioteca

// 2 Posibles implementaciones,
// - Hacer potencias de 2 hilos
// - Hacer log2(n) hilos y al dividir el espacio si queda 7 hilos 2 2 3 
//    y comparar 3 partes del array en vez de 2

// Compilar
// gcc MergeSortBarreras.c -o MergeSortBarreras -pthread -lm

//#define NUM_HILOS 2

void merge(int izq, int der);
void mergeSort(int izq, int der);
int arrayOrdenado(int n); 
void printArray(int n);
int leeArchivo();


pthread_barrier_t barrera;

typedef struct {
    int izq;
    int der;
    int id;
} DatosHilo;

int* a;


// En caso de que haya que procesar una parte del array con tamaño impar
// En el hilo se asigna a los impares (primeros) porque asi tambien lo procesa el merge
// Si no lo procesa mal

void *funcion_merge1(void *arg) {
    DatosHilo *datos = (DatosHilo *)arg;
    int izq = datos->izq;
    int der = datos->der;
    int id = datos->id;
    printf("Hilo %d, izq: %d, der:%d\n", id,izq,der);

    mergeSort(izq,der);    
    
    // Espera a los demas hilos
    pthread_barrier_wait(&barrera);
}

void *funcion_merge2(void *arg) {
    DatosHilo *datos = (DatosHilo *)arg;
    int izq = datos->izq;
    int der = datos->der;
    int id = datos->id;
    printf("Hilo %d, izq: %d, der:%d\n", id,izq,der);

    merge(izq,der);    
    
    // Espera a los demas hilos
    pthread_barrier_wait(&barrera);
}

int main() {    
    int n=leeArchivo();
    int NUM_HILOS=ceil(log2(n));

    if(NUM_HILOS%2==1) NUM_HILOS--;

    pthread_t hilos[NUM_HILOS]; // Numeros de hilos con potencias de 2 para reducir logaritmicamente el tiempo
    DatosHilo datos[NUM_HILOS];
    
    printArray(n);   

    
    // Primera parte
    pthread_barrier_init(&barrera, NULL, NUM_HILOS);
    
    printf("Creando hilos\n");  
    int tmp=n/NUM_HILOS;
    int hilosMod=n%NUM_HILOS;
    int aux=hilosMod;

    int cont=0;
    for (int i = 0; i < NUM_HILOS; i++) { 
        datos[i].id = i + 1;

        datos[i].izq=0+cont;
        cont+=tmp-1;
        if(hilosMod-->0)cont++; 
        datos[i].der=cont;
        cont++;
        pthread_create(&hilos[i], NULL, funcion_merge1, &datos[i]);        
    }

    // Esperar a que todos los hilos terminen
    for (int i = 0; i < NUM_HILOS; i++) {
        pthread_join(hilos[i], NULL);
    } 
    pthread_barrier_destroy(&barrera); // Destruir la barrera
    printArray(n);

    //int impar=NUM_HILOS%2!=0;
    //NUM_HILOS/=2;
    NUM_HILOS=ceil(NUM_HILOS/2.0);
    
    // Segunda parte
    while(NUM_HILOS!=1){
        printf("\n");
        // Inicializar barrera
        pthread_barrier_init(&barrera, NULL, NUM_HILOS);

        printf("Creando hilos\n");  
        tmp=n/NUM_HILOS;
        hilosMod=n%NUM_HILOS;

        cont=0;
        for (int i = 0; i < NUM_HILOS; i++) { 
            datos[i].id = i + 1;

            datos[i].izq=0+cont;
            cont+=tmp-1;
            if(hilosMod-->0)cont++; 
            datos[i].der=cont;
            cont++;
            pthread_create(&hilos[i], NULL, funcion_merge2, &datos[i]);        
        }
    
        // Esperar a que todos los hilos terminen
        for (int i = 0; i < NUM_HILOS; i++) {
            pthread_join(hilos[i], NULL);
        }        
        
        pthread_barrier_destroy(&barrera); // Destruir la barrera
        NUM_HILOS=ceil(NUM_HILOS/2.0);
        printArray(n);
    }
    merge(0,n-1);

    printf("Todos los hilos han terminado\n");

    printArray(n);
    if(arrayOrdenado(n)) printf("Ordenado\n");
    else printf("No ordenado\n");

    free(a); // Libera memoria 

    return 0;
}


void merge(int izq, int der) {       
    int n=(der-izq), m=n/2;
    int i=izq, j=m+1, k=izq;
    
    int aux[n+1]; // Solo crea memoria para la parte que se va a ordenar
    int cont=0; 
    for (i=izq; i<=der; i++) aux[cont++]=a[i];
    
    i=0;			   
    while (i<=m && j<=n) {                                     
        if (aux[i]<=aux[j]) a[k++]=aux[i++];			
        else a[k++]=aux[j++];
    }
            
    // copia los elementos que quedan de la primera mitad (si los hay)
    while (i<=m) { a[k++]=aux[i++]; } 
    while (j<=n) { a[k++]=aux[j++]; }         
}

void mergeSort(int izq, int der) {
    if (izq<der) {        
        int m=(izq+der)/2; // Mitad del array actual        
        mergeSort(izq, m); // Ordena la mitad 1
        mergeSort(m+1, der); // Ordena la mitad 2      
        merge(izq, der);  // Ordena las mitades ordenadas
    }
}

int arrayOrdenado(int n){
    for(int i=1;i<n;i++){
        if(a[i]!=a[i-1]+1)return 0;
    }
    return 1;
}

void printArray(int n){
    printf("Array:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", a[i]);
    }
    printf("\n");
}

int leeArchivo(){
    int arrayTam=0;
    int capacidad=10;
    a=(int*)malloc(capacidad*sizeof(int));
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

    return arrayTam;
}

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>

// Compilar
// gcc MergeSortBarreras.c -o MergeSortBarreras -pthread

#define NUM_HILOS 2

pthread_barrier_t barrera;

typedef struct {
    int izq;
    int der;

    int id;
} DatosHilo;

int* a;

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



void *funcion_hilo(void *arg) {
    DatosHilo *datos = (DatosHilo *)arg;
    int izq = datos->izq;
    int der = datos->der;
    int id = datos->id;
    printf("Hilo %d, izq: %d, der:%d\n", id,izq,der);

    mergeSort(izq,der);
    
    // Espera a los demas hilos
    pthread_barrier_wait(&barrera);

    return NULL;
}

void leeArchivo(int n){
    FILE *archivo;
    char nombre_archivo[100];
    int archivoTam;

    //int *parametros;
    
   
    printf("Introduce el nombre del archivo: ");
    scanf("%s", nombre_archivo);
    archivoTam = strlen(nombre_archivo);
    strcat(nombre_archivo, ".txt");

    archivo = fopen(nombre_archivo, "r"); // Modo lectura
    if (archivo == NULL) {
        perror("Error al abrir el archivo");
        exit(1);
    }

    a = (int *)malloc(n * sizeof(int));

    for (int i = 0; i < n; i++) {
        fscanf(archivo, "%d", &a[i]);
    }    


    fclose(archivo);    
    
}

int main() {
    pthread_t hilos[NUM_HILOS]; // Numeros de hilos con potencias de 2 para reducir logaritmicamente el tiempo
    DatosHilo datos[NUM_HILOS];
    
    int n=4;
    leeArchivo(n);

    printf("Array:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", a[i]);
    }
    printf("\n");


    // Inicializar barrera
    pthread_barrier_init(&barrera, NULL, NUM_HILOS);

    //while(numHilos==1){
        printf("Creando hilos\n");
        // Crear hilos
        int cont=0;
        for (int i = 0; i < NUM_HILOS; i++) { // GESTIONAR BIEN
            datos[i].id = i + 1;
            datos[i].izq=0+cont;
            cont+=49;
            datos[i].der=cont;
            cont++;
            pthread_create(&hilos[i], NULL, funcion_hilo, &datos[i]);        
        }
    
        // Esperar a que todos los hilos terminen
        for (int i = 0; i < NUM_HILOS; i++) {
            pthread_join(hilos[i], NULL);
        }        
        
        
    //}
    pthread_barrier_destroy(&barrera); // Destruir la barrera

    printf("Todos los hilos han terminado\n");

    printf("Array:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", a[i]);
    }
    printf("\n");

    free(a); // Libera memoria 

    return 0;
}

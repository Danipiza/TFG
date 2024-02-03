#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int* a;

// Funcion que ordena 2 subarrays
// First subarray is arr[l..m]
// Second subarray is arr[m+1..r]
// Complejidad temporal: O(n log n)
// Complejidad espacial: O(n)
void merge(/*int* a,*/ int izq, int der) {       
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

void mergeSort(/*int a[],*/ int izq, int der) {
    if (izq<der) {        
        int m=(izq+der)/2; // Mitad del array actual        
        mergeSort(/*a,*/ izq, m); // Ordena la mitad 1
        mergeSort(/*a,*/ m+1, der); // Ordena la mitad 2      
        merge(/*a,*/ izq, der);  // Ordena las mitades ordenadas
    }
}

int arrayOrdenado(int n){
    for(int i=1;i<n;i++){
        if(a[i]!=a[i-1]+1)return 0;
    }
    return 1;
}

int main(){
    
    FILE *archivo;
    char nombre_archivo[100];
    int archivoTam;

    //int *a;
    int n=100;
   
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
    // array = (int *)realloc(array, capacidad * sizeof(int)); // aumentar tamaño

    for (int i = 0; i < n; i++) {
        fscanf(archivo, "%d", &a[i]);
    }
    

    /*printf("Array:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", a[i]);
    }*/
    printf("\n");

    fclose(archivo);    
   


    mergeSort(/*a,*/0,n-1);
    if(arrayOrdenado(n)) printf("Ordenado\n");
    else printf("No Ordenado\n");
    /*printf("Array:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", a[i]);
    }
    printf("\n");*/


    free(a); // Libera memoria 

    return 0;
}

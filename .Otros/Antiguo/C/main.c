#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <aio.h>


// Complejidad temporal: O(n^2)
// Complejidad espacial: O(1)
void swapBubble(int a[], int pos) {
    int tmp=a[pos];
    a[pos] = a[pos+1];
    a[pos+1] = tmp;
}
void bubbleSort(int a[], int n) {    
    for(int i=0; i<n-1; i++) {
        for(int j=0; j<n-1-i; j++) {
            if(a[j]>a[j+1]) swapBubble(a, j);
        }
    }
}

// Complejidad temporal: O(n^2)
// Complejidad espacial: O(1)
void mueve(int a[], int pos) {
    int tmp=a[pos--];
    while(pos>=0 && tmp<a[pos]) {
        a[pos+1] = a[pos];
        pos--;
    }
    if(pos<0) pos = 0;
    else pos++;
    a[pos] = tmp;    
}
void insertionSort(int a[], int n) {
    for(int i = 1; i<n; i++) {
        if(a[i-1]>a[i]) mueve(a,i);
    }
}

// Funcion que ordena 2 subarrays
// First subarray is arr[l..m]
// Second subarray is arr[m+1..r]
// Complejidad temporal: O(n log n)
// Complejidad espacial: O(n)
void merge(int a[], int izq, int m, int der, int n) {       
    int i=izq, j=m+1, k=izq;    
    int aux[n];
    for (i=izq; i<=der; i++) aux[i]=a[i];
    
    i=izq;     
    while (i<=m && j<=der) {                                     
        if (aux[i]<=aux[j]) a[k++]=aux[i++];
        else a[k++]=aux[j++];
    }

    // copia los elementos que quedan de la primera mitad (si los hay)
    while (i<=m) { a[k++]=aux[i++]; } 
    while (j<=der) { a[k++]=aux[j++]; } 
}
void mergeSort(int a[], int izq, int der, int n) {
    if (izq<der) {        
        int m=(izq+der)/2; // Mitad del array actual        
        mergeSort(a, izq, m, n); // Ordena la mitad 1
        mergeSort(a, m+1, der, n); // Ordena la mitad 2      
        merge(a, izq, m, der, n);  // Ordena las mitades ordenadas
    }
}

// Complejidad temporal: O(n log n), peor caso = O(n^2)
// Complejidad espacial: O(log n)
int particion(int a[], int izq, int der) {
    int pivote = a[der], posPivote = der--;
    int eIzq=a[izq], eDer=a[der], tmp;
    while (izq<=der) {
        eIzq = a[izq]; eDer = a[der];

        while (eIzq<pivote) { izq++; eIzq = a[izq]; }
        while (eDer>=pivote && izq<=der) { der--; eDer = a[der]; }

        if (izq < der) {
            tmp = a[izq];
            a[izq] = a[der];
            a[der] = tmp;
            izq++; der--;
        }
    }
    // swap
    a[posPivote] = a[izq];
    a[izq] = pivote;
    return izq;
}
void quickSort(int a[], int izq, int der) {
    if (izq<der) {
        int pInd = particion(a, izq, der);
        quickSort(a, izq, pInd-1);
        quickSort(a, pInd+1, der);
    }
}

// Complejidad temporal: O(n^2)
// Complejidad espacial: O(1)
void swapSelection(int a[], int i, int j) {
    int tmp=a[i];
    a[i] = a[j];
    a[j] = tmp;
}
void selectionSort(int a[], int n) {    
    int minE=0, pos=0;
    for(int i=0; i<n-1; i++) {
        minE = a[i];
        pos = i;
        for(int j=i+1; j<n; j++) {
            if(minE>a[j]) { minE = a[j]; pos = j; }
        }
        swapSelection(a,i,pos);			
    }
}

// Imprime array
void printArray(int a[], int n) {
    for (int i = 0; i < n; i++) { printf("%d, ", a[i]); }
    printf("\n");
}
void crearArraySinDuplicados(int a[], int n, int neg) {
    int* nums = (int*)malloc(n * sizeof(int));

    // Inicialización del array nums
    if (!neg) {  // [1, n]
        for (int i = 0; i < n; i++) {
            nums[i] = i + 1;
        }
    } else {  // [-n/2, n/2)
        for (int i = 0; i < n; i++) {
            nums[i] = i - n / 2;
        }
    }

    srand(time(NULL)); // Inicialización de la semilla para la generación de números aleatorios
    int j = 0;
    for (int i = 0; i < n; i++) {
        j = rand() % (n - i);
        a[i] = nums[j];

        // Eliminar el elemento seleccionado del array nums
        for (int k = j; k < n - i - 1; k++) {
            nums[k] = nums[k + 1];
        }
    }

    free(nums);
}
void crearArrayConDuplicados(int a[], int n, int neg) {
    srand(time(NULL));

    if (!neg) {  // [1, n]
        for (int i = 0; i < n; i++) {
            a[i] = rand() % n + 1;
        }
    } else {  // [-n/2, n/2]
        for (int i = 0; i < n; i++) {
            a[i] = rand() % (n + 1) - n / 2;
        }
    }
}
void printMenu(){
    printf("Menu:\n");
    printf("1. BubbleSort\n");
    printf("2. InsertionSort\n");
    printf("3. MergeSort\n");
    printf("4. QuickSort\n");
    printf("5. SelectionSort\n");    
}
int compruebaOrdenacion(int a[], int n){
    int i = 1;
    while(i<n && a[i]>=a[i-1]){
        i++;
    }
    return i==n;
}

int main() {
    int n, dup;
    printf("Introduce el tamaño del array: ");
    scanf("%d", &n);
    int a[n];
    printf("0. Sin duplicados\n");
    printf("1. Con duplicados\n");
    scanf("%d", &dup);
    if(!dup) crearArraySinDuplicados(a,n,0);
    else crearArrayConDuplicados(a,n,0);

    printMenu();

    // Solicitar al usuario que ingrese un número para seleccionar una opción
    int opc;
    printf("Selecciona una ordenacion: ");
    scanf("%d", &opc);

    
    printf("Array inicial:\n");
    printArray(a, n);
    clock_t ini, fin;

    // Ejecutar la función correspondiente según la opción seleccionada
    switch (opc) {             
        case 1:
            ini = clock();
            bubbleSort(a,n);
            fin = clock();
            break;
        case 2:
            ini = clock();
            insertionSort(a,n);
            fin = clock();
            break;
        case 3:
            ini = clock();            
            mergeSort(a,0,n-1,n);
            fin = clock();
            break;
        case 4:
            ini = clock();
            quickSort(a,0,n-1);
            fin = clock();
            break;
        case 5:
            ini = clock();
            selectionSort(a,n);
            fin = clock();
            break;
        default:
            printf("Opcion no valida\n"); break;
    }

    printf("\nArray ordenado:\n");
    printArray(a, n);
    // Calcula el tiempo transcurrido
    double tiempoTotal = (double)(fin - ini) / CLOCKS_PER_SEC;

    // Imprime el tiempo transcurrido
    printf("Tiempo de ejecución: %f segundos\n", tiempoTotal);
    if(compruebaOrdenacion(a,n)) printf("Ordenado correctamente\n");
    else printf("No esta ordenado\n");

    return 0;
}

#include <stdio.h>
#include <stdlib.h>

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

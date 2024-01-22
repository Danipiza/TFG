#include <stdio.h>
#include <stdlib.h>

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
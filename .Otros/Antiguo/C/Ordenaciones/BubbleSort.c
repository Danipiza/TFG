#include <stdio.h>
#include <stdlib.h>


// Complejidad temporal: O(n^2)
// Complejidad espacial: O(1)
void swap(int a[], int pos) {
    int tmp=a[pos];
    a[pos] = a[pos+1];
    a[pos+1] = tmp;
}
void bubbleSort(int a[], int n) {    
    for(int i=0; i<n-1; i++) {
        for(int j=0; j<n-1-i; j++) {
            if(a[j]>a[j+1]) swap(a, j);
        }
    }
}
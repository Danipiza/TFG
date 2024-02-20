#include <stdio.h>
#include <stdlib.h>

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

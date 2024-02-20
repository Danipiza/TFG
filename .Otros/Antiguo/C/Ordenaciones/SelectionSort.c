#include <stdio.h>
#include <stdlib.h>

// Complejidad temporal: O(n^2)
// Complejidad espacial: O(1)
void swap(int a[], int i, int j) {
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
        swap(a,i,pos);			
    }
}

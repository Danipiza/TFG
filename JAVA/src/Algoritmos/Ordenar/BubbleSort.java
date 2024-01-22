package Algoritmos.Ordenar;
/*
	Es un algoritmo que mueve en cada iteracion el valor maximo
		en un intervalo que va decreciendo en 1 por el final.
	Es decir, la 1ra iteracion pone en (n-1)vo lugar el valor max
		2da iteracion en el (n-2)vo lugar el valor maximo del intervalo   	
*/

public class BubbleSort {
	
	private void swap(int[] a, int pos) {
		int tmp = a[pos];
		a[pos] = a[pos+1];
		a[pos+1] = tmp;
	}
	
	public void sort(int[] a) {
		int n = a.length;
		for(int i = 0; i<n-1 ; i++) {
			for(int j = 0; j<n-1-i ; j++) {
				if(a[j]>a[j+1]) swap(a, j);
			}
		}
	}
	
}

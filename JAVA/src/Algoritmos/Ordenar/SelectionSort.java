package Algoritmos.Ordenar;

/*
	Es un algoritmo que va ordenando conforme pasan las iteraciones. Igual que bubblesort
	El iterador empieza en el 1er elemento. En cada iteracion recorre la parte no ordenada
		y escoge el menor elemento para cambiarlo con el 1er elemento de la parte no ordenada.

*/

public class SelectionSort {
	
	private void swap(int[] a, int i, int j) {
		int tmp = a[i];
		a[i]=a[j];
		a[j]=tmp;
	}
	
	public void sort(int[] a) {
		int n = a.length;
		int minE = 0, pos = 0;
		for(int i = 0; i < n-1; i++) {
			minE = a[i];
			pos = i;
			for(int j = i+1; j < n; j++) {
				if(minE>a[j]) { minE = a[j]; pos = j; }
			}
			swap(a,i,pos);			
		}
	}
}

package Algoritmos.Ordenar;

/*
	Es un algoritmo que va ordenando conforme pasan las iteraciones.
	El iterador empieza en el 1er elemento. Elige el siguiente elemento. 
		Si es mayor que el anterior pasa al siguiente elemento.
		Si no es mayor mueve los que sean mayor a la derecha hasta
			encontrar su sitio.   
*/

public class InsertionSort {

	private void mueve(int[] a, int pos) {
		int tmp = a[pos--];
		while(pos>=0 && tmp<a[pos]) {
			a[pos+1] = a[pos];
			pos--;
		}
		if(pos<0) pos = 0;
		else pos++;
		a[pos] = tmp;
		
	}
	
	public void sort(int[] a) {
		int n = a.length;
		for(int i = 1; i<n; i++) {
			if(a[i-1]>a[i]) mueve(a,i);
		}
	}
	
}

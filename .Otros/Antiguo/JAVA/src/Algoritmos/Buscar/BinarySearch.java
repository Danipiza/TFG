package Algoritmos.Buscar;

/*
Es un algoritmo que va decreciendo el tamaño del array donde busca por la mitad.

Requiere que el array este ordenado.
Coste de preprocesado O(nlog n)

Coste temporal O(log n)
Coste espacial O(1)
*/

public class BinarySearch {
	
	private int pos;
	
	public boolean search(int a[], int x){
		int m;
		int i = 0, j = a.length;
		
		while(i<j) {
			m = (i+j)/2;
			if(a[m]==x) { pos = m; return true; }
			else if(a[m]>x) j = m-1;
			else i = m+1;
		}
		pos = -1;
		
		return false;
	}
	
	public int getPos() { return this.pos; }
	
}

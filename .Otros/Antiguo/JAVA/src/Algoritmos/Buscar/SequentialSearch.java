package Algoritmos.Buscar;

/*
Es un algoritmo que recorre linealmente todo el array
Coste Temporal: O(n)
Coste Espacial: O(1)
*/

public class SequentialSearch {	
	
	private int pos;
	
	public boolean search(int a[], int x, int ini, int fin) {		
		for(int i = ini; i < fin; i++) {
			if(a[i] == x) { pos = i; return true; }
		}

		pos=-1;
		return false;
	}
	
	public int getPos() { return this.pos; }
}

package Algoritmos.Ordenar;

/* 	
 	Es un algoritmo de divide y vencerás.
   	Caso base, solo hay un elemento o ninguno esa parte esta ordenada
   	Caso recursivo, comparamos los elementos con un pivote y los ponemos 
   		a la izquierda si son menores o la derecha si son mayores
   	
   	Lo que hacemos es tener 2 punteros, uno a la izquierda y el otro a la derecha. 
   		Izq busca el 1er elemento mayor que el pivote empezando por el principio. 
   		Der busca el 1er elemento menor que el pivote empezando por el final. 
   	Termina cuando el puntero izq es mayor que der
*/

public class QuickSort {
	
	private int particion(int a[], int izq, int der) {
		int pivote = a[der], posPivote = der--;		
		int eIzq = a[izq], eDer = a[der];
		int tmp = 0;
		while(izq<der) {
			while(eIzq<pivote) { izq++; eIzq=a[izq]; }
			while(eDer>pivote && izq<der) { der--; eDer=a[der]; }
			
			if(izq<der) { // swap
				tmp = a[izq];
				a[izq] = a[der];
				a[der] = tmp;
				// aumenta los punteros
				izq++; eIzq = a[izq];
				der--; eDer = a[der];
				if(izq==der)izq++;
			}			
		}
		// swap
		a[posPivote] = a[izq];
		a[izq] = pivote;
		return izq;
	}	
		
	
	public void sort(int a[], int izq, int der) {
	    if (izq < der) {
	        int pInd = particion(a, izq, der);

	        sort(a, izq, pInd-1);
	        sort(a, pInd+1, der);
	    }
	}
	
}

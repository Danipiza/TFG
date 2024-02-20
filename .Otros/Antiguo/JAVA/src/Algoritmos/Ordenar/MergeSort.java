package Algoritmos.Ordenar;

/*
	Divide parte el array en subarrays de 1 elemento. Y luego los
		compara para ir cambiandolos.
*/

public class MergeSort {

	public void merge(int a[], int izq, int der){
		int n=(der-izq), m=n/2;
		int i=izq, j=m+1, k=izq;
		
		int[] aux = new int[n+1]; // Solo crea memoria para la parte que se va a ordenar
		int cont=0; 
		for (i=izq; i<=der; i++) aux[cont++]=a[i];
	    
		i=0;			   
		while (i<=m && j<=n) {                                     
			if (aux[i]<=aux[j]) a[k++]=aux[i++];			
			else a[k++]=aux[j++];
		}
		        
		// copia los elementos que quedan de la primera mitad (si los hay)
		while (i<=m) { a[k++]=aux[i++]; } 
		while (j<=n) { a[k++]=aux[j++]; } 
	}
	
	public void mergesort(int a[],int izq, int der){
		if (izq < der){
			int m=(izq+der)/2;
            mergesort(a,izq, m);
            mergesort(a,m+1, der);                                                                                
            merge(a,izq, der);                                                                                 
	    }
	}	
		
}

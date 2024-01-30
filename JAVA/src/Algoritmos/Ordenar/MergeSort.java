package Algoritmos.Ordenar;

/*
	Divide parte el array en subarrays de 1 elemento. Y luego los
		compara para ir cambiandolos.
*/

public class MergeSort {

	private void merge(int a[], int izq, int m, int der){
	   int i = izq, j = m+1, k = izq;
	   int[] aux = new int[a.length]; 	   
	   for (i=izq; i<=der; i++) aux[i]=a[i];
	    
	   i=izq; 
	   
	   while (i<=m && j<=der) {                                     
          if (aux[i]<=aux[j]) a[k++]=aux[i++];
          else a[k++]=aux[j++];
	   }
		        
	   // copia los elementos que quedan de la primera mitad (si los hay)
	   while (i<=m) { a[k++]=aux[i++]; } 
	   while (j<=der) { a[k++]=aux[j++]; } 
	}
	
	public void mergesort(int a[],int izq, int der){
	    if (izq < der){
            int m=(izq+der)/2;
            mergesort(a,izq, m);
            mergesort(a,m+1, der);                                                                                
            merge(a,izq, m, der);                                                                                 
	    }
	}	
		
}

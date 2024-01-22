package Main;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import Algoritmos.Ordenar.*;


public class Main {
	
	
	private static void crearArraySinDuplicados(int[] a, int n, boolean neg) {
		List<Integer> nums = new ArrayList<Integer>();
		if(!neg) 	// [1, n] 
			for(int i = 1; i<=n; i++) { nums.add(i); }		
		else  		// [-n/2, n/2)
			for(int i = -n/2; i<n/2; i++) { nums.add(i); }	
		
		Random r = new Random();
		int j=0;
		for(int i = 0; i<n; i++) {
			j = r.nextInt(n-i);
			a[i] = nums.get(j);
			nums.remove(j);
		}
		
	}
	
	private static void crearArrayConDuplicados(int[] a, int n, boolean neg) {
		Random r = new Random();
		
		if(!neg) 	// [1, n] 
			for(int i = 0; i<n; i++) { a[i] = r.nextInt(n)+1; }		
		else  		// [-n/2, n/2]
			for(int i = 0; i<n; i++) { a[i] = r.nextInt(n+1)-n/2; }			
	}
	
	private static void imprimeArray(int[] a) {
		for(int x: a) System.out.print(x + " ");
		System.out.println();
	}
	
	@SuppressWarnings("unused")
	public static void main(String[] args) {
		QuickSort quickSort = new QuickSort();
		BubbleSort bubbleSort = new BubbleSort();
		InsertionSort insertionSort = new InsertionSort();
		SelectionSort selectionSort = new SelectionSort();
		MergeSort mergeSort = new MergeSort();
		
		
		int[] b = new int[100000];
		crearArraySinDuplicados(b,100000,true);
		imprimeArray(b);
		long comienzo = System.currentTimeMillis();
		mergeSort.mergesort(b, 0, b.length-1);
		long fin = System.currentTimeMillis();
		imprimeArray(b);		
		long total = fin - comienzo;
		System.out.println("Tarda: " + total/1000.0 + " segundos");

		
		/*while(true) {
			int[] b = new int[100];
			crearArraySinDuplicados(b,100,true);
			imprimeArray(b);
			mergeSort.mergesort(b, 0, b.length-1);
			imprimeArray(b);
		}*/
		
		//int[] a = {5,4,2,6,8,1,3,7,15,12,14,13,11,10,9};
		//int[] a = {7,8,5,2,4,6,3};
		//imprimeArray(a);
		//quickSort.sort(a, 0, a.length-1);
		//bubbleSort.sort(a);
		//insertionSort.sort(a);
		//selectionSort.sort(a);
		
		//mergeSort.mergesort(b, 0, b.length-1);
		//imprimeArray(a);
	}

}

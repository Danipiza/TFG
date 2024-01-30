package Main;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.StringTokenizer;

import Algoritmos.Buscar.*;
import Algoritmos.Ordenar.*;
import Mejoras.SequentialSearch.SeqHilos;


public class Main {
	
		
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
		
		SequentialSearch sequencialSearch = new SequentialSearch(); 
		BinarySearch binarySearch = new BinarySearch();
		
		
		
		
		int[] a = new int[100000];
		String t;
		int num, i = 0;
		try {
            // Abre el archivo 
            BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream("datos4.txt")));
            String linea = br.readLine(); // Lee la línea del archivo            
            br.close(); // Cierra el BufferedReader

            // StringTokenizer divide la linea en tokens
            if (linea != null) {                
                StringTokenizer tokenizer = new StringTokenizer(linea);
                
                while (tokenizer.hasMoreTokens()) {
                    t = tokenizer.nextToken();
                    num = Integer.parseInt(t);
                    a[i++] = num;
                }
            } else System.out.println("El archivo esta vacio");
        } catch (IOException e) {
            e.printStackTrace();
        }
		
		SeqHilos p = new SeqHilos(a);
		
		long comienzo, fin, total;
		
		
		try {
			p.ex(61309);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		
		comienzo = System.nanoTime();
		sequencialSearch.search(a, 61309, 0, a.length-1);		
		fin = System.nanoTime();
		total = fin - comienzo;
		System.out.println("(Normal) Tarda: " + total + " nanosegundos");
		
		/*if(binarySearch.search(a, 77)) {
			System.out.println("Esta en el array, en la posicion " + binarySearch.getPos());
		}
		else System.out.println("No esta en el array");*/
		
		
		
		
		/*int[] b = new int[100000];
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

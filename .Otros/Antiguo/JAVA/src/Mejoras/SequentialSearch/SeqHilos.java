package Mejoras.SequentialSearch;

import Algoritmos.Buscar.SequentialSearch;

public class SeqHilos {

	private int a[];
	private int x;
	private boolean encontrado;
	
	public SeqHilos(int a[]) {
		this.a = a;
		encontrado = false;		
	}
	
	public class MultiThread extends Thread {
		
		private long id;		
		private int pos;
		private int desp;
				
		SequentialSearch seqSearch;
		
		MultiThread(long id, int pos){
			seqSearch = new SequentialSearch();
			this.id = id;
			this.pos = pos;
		}	
		
		// Sequential search		
		public void run() {
			for(int i = pos; i < pos+desp && !encontrado; i++) {
				if(a[i] == x) {					
					encontrado=true;
					pos = i;					
					return; 
				}
			}							
		}
	}
	
	
	public void ex(int x) throws InterruptedException {
		this.x = x;
		int N = 100;
		MultiThread p[] = new MultiThread[N];
		
		long comienzo, fin, total;
		
		comienzo = System.nanoTime();
		
		for(int i = 0; i < N; i++) {
			p[i] = new MultiThread(i+1, 100*(i));		
			p[i].start(); 
		}		
					
		// Espera a que los hilos terminen 
		for(int i = 0; i < N; i++) {			
			p[i].join();												
		}
		
		fin = System.nanoTime();
		total = fin - comienzo;
		System.out.println("(Hilos) Tarda: " + total + " nanosegundos");
		
		System.out.println("Los " + N + " procesos han terminado");

	}
}

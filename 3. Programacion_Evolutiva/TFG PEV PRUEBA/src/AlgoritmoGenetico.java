

public class AlgoritmoGenetico {
	
	static public class Gen {
		public int[] v;

		public Gen(int l) {
			v = new int[l];
			init(l);
		}

		public Gen(Gen gen) {
			v = new int[gen.v.length];
			for (int i = 0; i < gen.v.length; i++) {
				v[i] = gen.v[i];
			}
		}

		private void init(int l) {
			for (int i = 0; i < l; i++) {
				v[i] = (Math.random() <= 0.5 ? 1 : 0);
			}
		}

	}
	
	static public class Individuo {

		
		public Gen[] genes;
		public double fitness;
		public double[] fenotipo;	
		
		public Individuo(int num, int[] tam_genes, double xMax[], double[] xMin) {
			genes = new Gen[num];
			fenotipo = new double[num];
			fitness = 0;
			for (int i = 0; i < num; i++) {
				genes[i] = new Gen(tam_genes[i]);
			}
		}
		
		public Individuo(Individuo poblacion) {
			int num = poblacion.genes.length;
		
			genes = new Gen[num];
			fenotipo = new double[num];
			fitness = 0;
			for (int i = 0; i < num; i++) {
				genes[i] = new Gen(poblacion.genes[i]);
			}
		
		}
		
		private int bin2dec(Gen gen) {
			int ret = 0;
			int cont = 1;
			for (int i = gen.v.length - 1; i >= 0; i--) {
				if (gen.v[i] == 1)
					ret += cont;
				cont *= 2;
			}
			return ret;
		}
		
		public void calcular_fenotipo(double[] xMax, double[] xMin) {
			for (int i = 0; i < genes.length; i++) {
				fenotipo[i] = calcular_fenotipoCromosoma(genes[i], xMax[i], xMin[i]);
			}
		}
		
		private double calcular_fenotipoCromosoma(Gen ind, double xMax, double xMin) {
			return xMin + bin2dec(ind) * ((xMax - xMin) / (Math.pow(2, ind.v.length) - 1));
		}
		
		public void printIndividuo() {
			for (Gen c : genes) {
				for (int a : c.v) {
					System.out.print(a + " ");
				}
			}
		
			System.out.println(" fenotipo x1: " + fenotipo[0] + " fenotipo x2: " + fenotipo[1]);
		}



	}

	// Parametros interfaz
	static private int tam_poblacion;
	static private int generaciones;	
	static private double prob_cruce;	
	static private double prob_mut;
	static private double precision;
	
	static private int num_genes;	
	static private int tam_individuo;
	static private int[] tam_genes;
	static private Individuo[] poblacion;

	// Evaluacion
	static private double fitness_total;
	static private double[] prob_seleccion;
	static private double[] prob_seleccionAcum;

	
	static private double mejor_total;


	static private double[] maximos;
	static private double[] minimos;

	static private void setValores() {
		tam_poblacion = 100;
		generaciones = 20;
		prob_cruce = 0.6;		
		prob_mut = 0.05;
		precision = 0.01;
		
		maximos= new double[2];
		minimos= new double[2];
		
		maximos[0]=maximos[1]=10;
		minimos[0]=minimos[1]=-10;
		
		num_genes=2;
		tam_genes = tamGenes();
	
		mejor_total = Double.MIN_VALUE;
	}

	static public void ejecuta() {
		Individuo[] selec = null;
				
		
		setValores();
		
		

		init_poblacion();
		evaluacion_poblacion();


		while (generaciones-- != 0) {
			selec = seleccion_poblacion(tam_poblacion, 5);
			
			poblacion = cruce_poblacion(selec);
			poblacion = mutacion_poblacion();
			
			evaluacion_poblacion();
		}
		System.out.println(mejor_total);
	}

	static private int[] tamGenes() {
		int ret[] = new int[num_genes];
		for (int i = 0; i < num_genes; i++) {
			tam_individuo += ret[i] = tamGen(precision, minimos[i], maximos[i]);
		}

		return ret;
	}

	static private int tamGen(double precision, double min, double max) {
		return (int) Math.ceil((Math.log10(((max - min) / precision) + 1) / Math.log10(2)));
	}

	static private void init_poblacion() {
		poblacion = new Individuo[tam_poblacion];

		for (int i = 0; i < tam_poblacion; i++) {
			poblacion[i] = new Individuo(num_genes, tam_genes, maximos, minimos);
		}
		
	}

	static public double fitness(double[] nums) {
		return (Math.pow(nums[0], 2) + 2 * Math.pow(nums[1], 2));
	}
	
	static private void evaluacion_poblacion() {
		fitness_total = 0;
		prob_seleccion = new double[tam_poblacion];
		prob_seleccionAcum = new double[tam_poblacion];

		double mejor_generacion = Double.MIN_VALUE;

		for (int i = 0; i < tam_poblacion; i++) {
			poblacion[i].calcular_fenotipo(maximos, minimos);
		}		

		double fit;
		for (int i = 0; i < tam_poblacion; i++) {
			fit=fitness(poblacion[i].fenotipo);
			poblacion[i].fitness = fit;
			fitness_total += fit;			
			
			if(mejor_generacion<fit)mejor_generacion=fit;			
		}

		if(mejor_total<mejor_generacion)mejor_total=mejor_generacion;
		 

		double acum = 0;
		for (int i = 0; i < tam_poblacion; i++) {
			prob_seleccion[i] = poblacion[i].fitness/fitness_total;
			
			acum += prob_seleccion[i];
			prob_seleccionAcum[i] = acum;
		}
		

	}

	static int busquedaBinaria(double x, double[] prob_acumulada) {
		int i = 0, j = tam_poblacion - 1;
		int m = 0;
		while (i < j) {
			m = (j + i) / 2;

			if (x > prob_acumulada[m]) {
				i = m + 1;
			} else if (x < prob_acumulada[m]) {
				j = m;
			} else
				return m;
		}

		return i;
	}

	static public Individuo[] ruleta(Individuo[] poblacion, double[] prob_acumulada, int tam_seleccionados) {
		Individuo[] seleccionados = new Individuo[tam_seleccionados];

		double rand;
		for (int i = 0; i < tam_seleccionados; i++) {
			rand = Math.random();
			
			seleccionados[i] = new Individuo(poblacion[busquedaBinaria(rand, prob_acumulada)]);			
		}

		return seleccionados;
	}
	

	static private Individuo[] seleccion_poblacion(int tam_seleccionados, int k) {
		Individuo[] seleccionados = new Individuo[tam_seleccionados];

		/*double randomFitness;
		int indexMax;
		double max;
		for (int i = 0; i < tam_seleccionados; i++) {
			max = Double.NEGATIVE_INFINITY;
			indexMax = -1;
			for (int j = 0; j < k; j++) {
				int randomIndex = (int) (Math.random() * tam_poblacion);
				randomFitness = poblacion[randomIndex].fitness;
				if (randomFitness > max) {
					max = randomFitness;
					indexMax = randomIndex;
				} 
			}	
			 
			seleccionados[i] = new Individuo(poblacion[indexMax]);
		
		}

		return seleccionados;*/
		return ruleta(poblacion, prob_seleccionAcum,100);
		
	}

	static private Individuo[] cruce_poblacion(Individuo[] selec) {
		int n = selec.length;
		Individuo[] ret = new Individuo[n];
		
		if (n % 2 == 1) {
			ret[n - 1] = selec[n - 1];
			n--; // descarta al ultimo si es impar
		}
		

		int[] long_genes = new int[selec[0].genes.length];
		int corte_maximo = -1, cont = 0;
		for (Gen c : selec[0].genes) {
			corte_maximo += c.v.length;
			long_genes[cont++] = c.v.length;
		}
		// int l=corte_maximo+1;
		int i = 0, j = 0, k = 0;
		Individuo ind1, ind2;
		int corte, tmp;
		while (i < n) {
			ind1 = new Individuo(selec[i]);
			ind2 = new Individuo(selec[i + 1]);

			if (Math.random() < prob_cruce) {
				corte = (int) (Math.random() * (corte_maximo)) + 1; // [1,corte_maximo]
				cont = 0;
				j = 0;
				for (k = 0; k < corte; k++) {
					tmp = ind1.genes[cont].v[j];
					ind1.genes[cont].v[j] = ind2.genes[cont].v[j];
					ind2.genes[cont].v[j] = tmp;
					j++;
					if (j == long_genes[cont]) {
						cont++;
						j = 0;
					}
				}
			}
			ret[i++] = ind1;
			ret[i++] = ind2;
		}
		return ret;
	}

	static private Individuo[] mutacion_poblacion() {
		int tam_poblacion=poblacion.length;
		Individuo[] ret = new Individuo[tam_poblacion];
		
		
		Individuo act;
		for (int i=0;i<tam_poblacion;i++) {
			act= new Individuo(poblacion[i]);
			//act= poblacion[i];
			for(int c=0;c<poblacion[i].genes.length;c++){
				for(int j=0;j<poblacion[i].genes[c].v.length;j++) {					
					if(Math.random()<prob_mut) {
						act.genes[c].v[j]=(act.genes[c].v[j]+1)%2;
					}
				}
			}
			ret[i]=act;
		}
		return ret;
	}	
	
	public static void main(String[] args) {
		ejecuta();
		

	}

}
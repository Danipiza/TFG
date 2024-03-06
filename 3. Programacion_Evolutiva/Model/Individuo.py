import random


class Individuo:  
    def __init__(self, num, tam_genes, xMax, xMin):
        self.num = num              # Numero de genes (int)
        self.tam_genes = tam_genes  # Tamaño de cada gen (int[])
        self.genes = []             # Array de bits, con todos los genes
        self.fenotipos = []         # Valor real
        self.xMax=xMax              # Valores maximos de cada gen
        self.xMin=xMin              # Valores minimos de cada gen
        self.fitness=0              # Valor de aptitud del individuo

        # Inicializa de forma aleatoria el individuo
        for i in range(num):
            row = []
            for j in range(tam_genes[i]):
                row.append(random.randint(0, 1))  
            self.genes.append(row)
        
        # Calcula valor real
        self.calcular_fenotipos()
        
    # Convierte a decimal un array de bits
    def bin2dec(self, gen):
        ret=0
        cont=1
        for i in range(len(gen) - 1, -1, -1):
            if gen[i]==1:
                ret+=cont                       
            cont*=2

        return ret
	
    # Calcula los valores reales de cada gen del individuo
    def calcular_fenotipos(self):
        for i in range(self.num):
            self.fenotipos.append(self.calcular_fenotipo(i))
	
    # Calcula el valor real de un gen
    def calcular_fenotipo(self, i):
        return (self.xMin[i] + self.bin2dec(self.genes[i]) * ((self.xMax[i] - self.xMin[i]) / (pow(2, len(self.genes[i])) - 1)))
            
    # Imprime el individuo
    def print(self):
        for i in range(self.num):
            for j in range(self.tam_genes[i]): 
                print(self.genes[i][j], end=" ")
            if i!=self.num-1 : print(" | ", end="")
   
            
def print_poblacion(selec):      
    cont=1
    for ind in selec:    
        ind.print()
        print("Individuo:", cont, 
              "Fenotipo:", f"{ind.fenotipos[0]:.3f}", ",", f"{ind.fenotipos[1]:.3f}", 
              "Fitness:", f"{ind.fitness:.4f}")                     
        cont=cont+1
            

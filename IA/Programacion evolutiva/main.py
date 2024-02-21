import random
import time


"""
Ejemplo del laberinto

inicializar()
evaluar()
while()
    seleccionar()
    cruce()
    mutacion()
    evaluar()




"""
poblacion=[]
tam_poblacion=0
num_genes=0
tam_genes=[]

fitness_total = 0
prob_seleccion = [0.0] * tam_poblacion
prob_seleccionAcum = [0.0] * tam_poblacion

mejor_total=0

class Seleccion:
    def __init__(self, tam_poblacion, opt):
        self.tam_poblacion=tam_poblacion
        self.opt=opt
    
    def busquedaBinaria(self, x, prob_acumulada):
        i=0
        j=self.tam_poblacion-1
        m=0        

        while i<j :            
            m = int((j+i)/2)  
            if x > prob_acumulada[m] : 
                i=m+1
            elif x < prob_acumulada[m] : 
                j=m
            else : 
                return m 
        return i
    
    def ruleta(self, poblacion, prob_acumulada, tam_seleccionados):
        ret = []
        rand = 0.0
        #print_poblacion()
        for i in range(tam_seleccionados):
            rand=random.random()                       
            index = self.busquedaBinaria(rand, prob_acumulada)
            ret.append(poblacion[index]) 

        return ret
    
    def torneo_deterministico():
        # TODO
        return ""
    
    def torneo_probabilistico():
        # TODO
        return ""
    
    def estocastico_universal():
        # TODO
        return ""

     
class Cruce:
    def __init__(self, p):
        self.p=p
    
    def cruce_monopuntoBin(self, selec):
        ret=[]
        n=len(selec)
        if n%2==1:
            ret.append(selec[n-1])
            n-=1
        
        long_genes = []
        corte_max=-1
        for gen in selec[0].genes:
            long_genes.append(len(gen))
            corte_max+=len(gen)

        i=0
        while i<n:
            ind1=selec[i]
            ind2=selec[i+1]

            if random.random() < self.p :                
                corte=random.randint(0,corte_max)
                #print(i, "Cruzados en:",corte)
                cont=0
                j=0
                
                for k in range(corte+1):
                    #print("I1:", ind1.genes[cont][j],"I2:",ind2.genes[cont][j])                    
                    tmp=ind1.genes[cont][j]
                    ind1.genes[cont][j] = ind2.genes[cont][j]
                    ind2.genes[cont][j] = tmp
                    j+=1
                    if j == long_genes[cont]:
                        cont+=1
                        j = 0
            ret.append(ind1)
            ret.append(ind2)
            i+=2
					

        return ret
    
    def cruce_uniforme():
        # TODO
        return ""

class Mutacion:
    def __init__(self, p):
        self.p=p
    
    def mut_basicaBin(self, selec):
        ret=[]

        for ind in selec:            
            for i in range(ind.num):
                for j in range(len(ind.genes[i])):
                    if random.random() < self.p:                        
                        ind.genes[i][j]=(ind.genes[i][j]+1)%2

            ret.append(ind)

        return ret

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
            


def init_poblacion():   
    global poblacion, tam_poblacion, num_genes, tam_genes     
    poblacion = [Individuo(num_genes, tam_genes,[10,10],[-10,-10]) for _ in range(tam_poblacion)]


def fun1(nums):
    return (pow(nums[0], 2) + 2 * pow(nums[1], 2))

# funcion 
def evalua_poblacion():
    global tam_poblacion, poblacion
    global fitness_total, prob_seleccion, prob_seleccionAcum
    global mejor_total

    fitness_total = 0
    prob_seleccion = [0.0] * tam_poblacion
    prob_seleccionAcum = [0.0] * tam_poblacion
    
    mejor_generacion=0

    for i in range(tam_poblacion):
        poblacion[i].calcular_fenotipos()
        poblacion[i].fitness = fun1(poblacion[i].fenotipos)
        fitness_total += poblacion[i].fitness
        if mejor_generacion < poblacion[i].fitness:
            mejor_generacion=poblacion[i].fitness

    if mejor_total<mejor_generacion :
        mejor_total=mejor_generacion
    
    tmp=0.0
    acum=0.0
    for i in range(tam_poblacion):
        tmp = poblacion[i].fitness / fitness_total
        prob_seleccion[i] = tmp
        acum += tmp
        prob_seleccionAcum[i] = acum    


def selecciona_poblacion():
    global poblacion, tam_poblacion, prob_seleccionAcum
    seleccion = Seleccion(tam_poblacion, 0)    

    
    return seleccion.ruleta(poblacion, prob_seleccionAcum,tam_poblacion)

def cruza_poblacion(seleccion):    
    cruce=Cruce(0.6)    
    return cruce.cruce_monopuntoBin(seleccion)

def muta_poblacion():
    global poblacion
    mut=Mutacion(0.05)   
    return mut.mut_basicaBin(poblacion)


def ejecuta():    
    global poblacion, tam_poblacion, num_genes, tam_genes
    tam_poblacion=10000
    num_genes=2
    tam_genes=[1000,1000]
    

    
    start_time = time.time()
     
    init_poblacion()
    evalua_poblacion()

    
    for i in range(100):
        selec = selecciona_poblacion()    
        #print_poblacion(selec)
        poblacion = cruza_poblacion(selec)    
        #print_poblacion(poblacion)
        poblacion = muta_poblacion()
        #print_poblacion(poblacion)
        evalua_poblacion()
    
    end_time = time.time()

    print("Tiempo de ejecucion:",  end_time - start_time)
    #print_poblacion()
    

ejecuta()
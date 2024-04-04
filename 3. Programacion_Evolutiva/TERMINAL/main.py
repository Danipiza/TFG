from mpi4py import MPI
import sys
import os
import random
import math

from abc import ABC, abstractmethod 

# --------------------------------------------------------------------------------------------------------------
# -- MODEL -----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

class Individuo:
    def __init__(self, num, tam_genes, xMax, xMin, ind):
        self.genes=[]
        self.xMax=[]
        self.xMin=[]
        if ind is not None:
            self.genes=[(Gen(l=None,v=ind.genes[i].v)) for i in range(len(ind.genes))]
            
            self.xMax=ind.xMax
            self.xMin=ind.xMin
        else:
            self.genes = [(Gen(tam_genes[i],v=None)) for i in range(num)]            
            self.xMax=xMax
            self.xMin=xMin

        self.fitness=0
        self.fenotipo=[]
        self.calcular_fenotipo()

    def bin2dec(self, gen):
        ret=0
        cont=1
        for i in range(len(gen.v) - 1, -1, -1):
            if gen.v[i]==1:
                ret+=cont
            cont*=2
        
        return ret

    def calcular_fenotipo(self):
        self.fenotipo=[]    
        for i in range(len(self.genes)):
            self.fenotipo.append(self.calcular_fenotipo_cromosoma(i))
        

    def calcular_fenotipo_cromosoma(self, i):
        return self.xMin[i]+self.bin2dec(self.genes[i])*((self.xMax[i]-self.xMin[i])/((2**len(self.genes[i].v))-1))

    def print_individuo(self):
        for c in self.genes:
            for a in c.v:
                print(a, end=" ")
        print()
        #print("fenotipo x1:", self.fenotipo[0], "fenotipo x2:", self.fenotipo[1])

class Gen:
    def __init__(self, l, v):
        self.v = []

        if v is not None:
            self.v=[(v[i]) for i in range(len(v))]
        else:
            self.v=[(random.randint(0,1)) for i in range(l)]

# --------------------------------------------------------------------------------------------------------------
# -- FUNCION ---------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

class Funcion(ABC):
    xMax=[]      # double[]. Valores maximos de los elementos de los individuos
    xMin=[]      # double[]. Valores minimos
    opt=True        # booleano. maximizar: True, minimizar: False

    @abstractmethod
    def fitness(self,nums): 
        pass
    
    @abstractmethod
    def cmp(self,a,b): 
        pass
    @abstractmethod
    def cmpBool(self,a,b): 
        pass

    @abstractmethod
    def cmpPeor(self,a,b): 
        pass
    @abstractmethod
    def cmpPeorBool(self,a,b): 
        pass

class Funcion1(Funcion):

    def __init__(self):
        self.opt=True
        self.xMax=[10,10]
        self.xMin=[-10,-10]
    
    def fitness(self, nums):        
        return ((nums[0]**2)+2*(nums[1]**2))
    
    def cmp(self, a, b): 
        if a>b: return a
        else: return b

    def cmpBool(self, a, b): 
        if a>b: return True
        else: return False

    def cmpPeor(self, a, b): 
        if a<b: return a
        else: return b

    def cmpPeorBool(self, a, b): 
        if a<b: return True
        else: return False

class Funcion2(Funcion):

    def __init__(self):
        self.opt=False
        self.xMax=[0,0]
        self.xMin=[-10,-6.5]
    
    def fitness(self, nums):    
        #f(x,y)=sen(y)*exp()    
        return  math.sin(nums[1])*math.pow(math.exp(1-math.cos(nums[0])),2) + \
                math.cos(nums[0])*math.pow(math.exp(1-math.sin(nums[1])),2) + \
                ((nums[0]-nums[1])**2)
    
    def cmp(self, a, b): 
        if a<b: return a
        else: return b

    def cmpBool(self, a, b): 
        if a<b: return True
        else: return False

    def cmpPeor(self, a, b): 
        if a>b: return a
        else: return b

    def cmpPeorBool(self, a, b): 
        if a>b: return True
        else: return False

class Funcion3(Funcion):

    def __init__(self):
        self.opt=False
        self.xMax=[10,10]
        self.xMin=[-10,-10]
    
    def fitness(self, nums):        
        exp = abs(1-(math.sqrt(nums[0]**2+nums[1]**2))/math.pi)
        ret = math.sin(nums[0])*math.cos(nums[1])*math.exp(exp)
        return -abs(ret)
    
    def cmp(self, a, b): 
        if a<b: return a
        else: return b

    def cmpBool(self, a, b): 
        if a<b: return True
        else: return False

    def cmpPeor(self, a, b): 
        if a>b: return a
        else: return b

    def cmpPeorBool(self, a, b): 
        if a>b: return True
        else: return False

class Funcion4(Funcion):

    def __init__(self, num_genes):
        self.opt=False
        self.d=num_genes
        self.xMax=[]
        self.xMin=[]
        for i in range(num_genes):
            self.xMax.append(math.pi)
            self.xMin.append(0)
    
    def fitness(self, nums):        
        ret = 0.0        
        for i in range(1,self.d+1):		
            sin1=math.sin(nums[i-1])                           
            radians=(i*(nums[i-1]**2))/math.pi
            comp=math.sin(radians)
            ret+=sin1*(comp**20)

        return ret*-1
    
    def cmp(self, a, b): 
        if a<b: return a
        else: return b

    def cmpBool(self, a, b): 
        if a<b: return True
        else: return False

    def cmpPeor(self, a, b): 
        if a>b: return a
        else: return b

    def cmpPeorBool(self, a, b): 
        if a>b: return True
        else: return False


# --------------------------------------------------------------------------------------------------------------
# -- SELECCION -------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
        
class Pair():
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key = key

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return "(" + str(self.key) + ", " + str(self.value) + ")"

class Seleccion:
    def __init__(self, tam_poblacion, opt):        
        self.tam_poblacion=tam_poblacion    # int  
        self.opt=opt                        # Boolean
    
    
    def busquedaBinaria(self, x, prob_acumulada):
        i,j = 0,self.tam_poblacion-1
        while i<j:
            m=(j+i)//2
            if x>prob_acumulada[m]: i=m+1
            elif x<prob_acumulada[m]: j=m
            else: return m
        return i

    def ruleta(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados = []
        for _ in range(tam_seleccionados):
            rand = random.random()
            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
        return seleccionados
    
    # TODO
    def tornedoDeterministico(self, poblacion, tam_seleccionados, k):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max = float('-inf')
            min = float('+inf')
            indexMax = -1
            indexMin = -1
            for j in range(k):        
                randomIndex=random.randint(0,self.tam_poblacion-1)
                randomFitness=poblacion[randomIndex].fitness
                if randomFitness>max:
                    max=randomFitness
                    indexMax=randomIndex 
                if randomFitness<min:
                    min=randomFitness
                    indexMin=randomIndex                
            
            if self.opt==True: ind=indexMax
            else: ind=indexMin

            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=poblacion[ind]))

        return seleccionados



    # TODO
    def torneoProbabilistico(self, poblacion, k, p, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max = float('-inf')
            min = float('+inf')
            indexMax = -1
            indexMin = -1
            for j in range(k):        
                randomIndex=random.randint(0,self.tam_poblacion-1)
                randomFitness=poblacion[randomIndex].fitness
                if randomFitness>max:
                    max=randomFitness
                    indexMax=randomIndex 
                if randomFitness<min:
                    min=randomFitness
                    indexMin=randomIndex                
            
            if self.opt==True: 
                if random.random()<=p: ind=indexMax
                else: ind=indexMin
            else: 
                if random.random()<=p: ind=indexMin
                else: ind=indexMax

            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=poblacion[ind]))

        return seleccionados
    

    def estocasticoUniversal(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
		
        incr=1.0/tam_seleccionados
        rand=random.random()*incr
        for i in range(tam_seleccionados):       			
            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
			
            rand += incr		

        return seleccionados

    # TODO
    def truncamiento(self, poblacion, prob_seleccion, trunc, tam_seleccionados):
        seleccionados=[]

		#Pair<Individuo, Double>[] pairs = new Pair[tam_seleccionados];
        pairs=[]
        for i in range(tam_seleccionados): 
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))
		
        pairs = sorted(pairs, key=lambda x: x.value, reverse=False)
		#Arrays.sort(pairs, Comparator.comparingDouble(p -> p.getValue()));

        x=0
        num= int(1.0/trunc)
        n=len(pairs)-1
        for i in range(int((tam_seleccionados) * trunc)):		
            j=0
            while j<num and x<tam_seleccionados:            
                seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=pairs[n-i].get_key()))
                j+=1
                x+=1
			
		
		
        return seleccionados
    
    # TODO
    def restos(self, poblacion, prob_seleccion, prob_acumulada, tam_seleccionados):
            # TODO
            return ""
    # TODO
    def ranking(self):
            # TODO
            return ""

# --------------------------------------------------------------------------------------------------------------
# -- CRUCE -----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------


class Cruce:
    def __init__(self, p):
        self.p=p    # int
    
    def cruce_monopuntoBin(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)]
        if n%2==1:
            ret[n-1] = Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[n-1])
            n-=1
        
        long_genes=[len(selec[0].genes[i].v) for i in range(len(selec[0].genes))]
        corte_maximo=-1
        for l in long_genes:
            corte_maximo+=l
        i=0

        ind1=[]
        ind2=[]
        while i<n:
            ind1=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i])
            ind2=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i + 1])
            """print("  (ANTES): ", end="") 
            ind1.print_individuo()
            print("  (ANTES): ", end="") 
            ind2.print_individuo()"""
            
            rand=random.random()
            if rand<self.p:                                               
                corte=random.randint(1,corte_maximo)
                #print("({}) CORTA EN: {}".format(i,corte))
                cont=0
                j=0
                for k in range(corte):
                    tmp=ind1.genes[cont].v[j]
                    ind1.genes[cont].v[j]=ind2.genes[cont].v[j]
                    ind2.genes[cont].v[j]=tmp
                    j+=1
                    if j==long_genes[cont]:
                        cont+=1
                        j=0
            
            
            """print("(DESPUES): ", end="") 
            ind1.print_individuo()
            print("(DESPUES): ", end="") 
            ind2.print_individuo()"""
            
            """print("RET: (ANT)")
            #for ind in ret:
            for j in range(i):
                ret[j].print_individuo()
            print("\n\n")"""

            ret[i] = Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind1)
            ret[i+1] = Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind2)
            #ret.append(ind2)
            i += 2     
            """print("RET: (DESP)")
            #for ind in ret:
            for j in range(i):
                ret[j].print_individuo()
            print("\n\n")  """        
        
        """print("Cruce:")
        for ind in ret:
            ind.print_individuo()"""
        
        return ret
    
    def cruce_uniforme():
        # TODO
        return ""
    
    def PMX():
        # TODO
        return ""
    
    def OX():
        # TODO
        return ""
    
    def OX_PP():
        # TODO
        return ""
    
    def CX():
        # TODO
        return ""
    
    def CO():
        # TODO
        return ""
    


# --------------------------------------------------------------------------------------------------------------
# -- MUTACION --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------


class Mutacion:
    def __init__(self, p):
        self.p=p
    
    def mut_basicaBin(self, selec):
        ret=[]
        for ind in selec:
            act=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind)
            for c in range(len(ind.genes)):
                for j in range(len(ind.genes[c].v)):
                    if random.random()<self.p:
                        act.genes[c].v[j]=(act.genes[c].v[j]+1)%2
            ret.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=act))
        return ret

    def inversion():
        # TODO
        return ""

    def intercambio():
        # TODO
        return ""
    
    def insercion():
        # TODO
        return ""
    

    
    def heuristica():
        # TODO
        return ""    
    def dfs():
        # TODO
        return ""


# --------------------------------------------------------------------------------------------------------------
# -- ALGORITMO GENETICO ----------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------


class AlgoritmoGenetico():
    def __init__(self):               
        self.funcion=None           # Funcion
        self.seleccion=None         # Seleccion
        self.cruce=None             # Cruce
        self.mutacion=None          # Mutacion

        self.poblacion=[]           # Individuo[]
        self.tam_genes=[]           # int[]

        self.tam_poblacion=0        # int
        self.generaciones=0         # int
        self.num_genes=0            # int
        self.prob_cruce=0.0         # double (0.1)
        self.prob_mut=0.0           # double (0-1)

        self.precision=0.0          # double (1, 0.01, 0.001, ...)
        self.elitismo=0             # int (0-100%)

        self.mejor_total=0.0        # double
        self.mejor_ind=None         # Individuo
        self.fitness_total=0        # double
        self.prob_seleccion=[]      # double
        self.prob_seleccionAcum=[]  # double[]

           

    # Funcion que inicializa las variables a los valores seleccionados en la interfaz
    def set_valores(self,tam_poblacion, generaciones, seleccion_idx, cruce_idx, prob_cruce, mutacion_idx,
                    prob_mut, precision, funcion_idx, num_genes, elitismo):
        
        self.poblacion=[]
        self.tam_poblacion=tam_poblacion    
        self.generaciones=generaciones      
        self.prob_cruce = prob_cruce        
        self.prob_mut = prob_mut    

        self.num_genes=num_genes # 2
        
                

        self.funcion_idx=funcion_idx

        if funcion_idx==0: self.funcion=Funcion1()
        elif funcion_idx==1: self.funcion=Funcion2()
        elif funcion_idx==2: self.funcion=Funcion3()
        elif funcion_idx==3: self.funcion=Funcion4(self.num_genes)
        
        self.seleccion_idx=seleccion_idx
        self.seleccion=Seleccion(tam_poblacion, self.funcion.opt)
        
        self.cruce_idx=cruce_idx
        self.cruce=Cruce(prob_cruce)    
        
        self.mutacion_idx=mutacion_idx
        self.mutacion=Mutacion(prob_mut)

        self.tam_genes=self.tamGenes(precision)
        #self.mejor_total = float('-inf')
        if self.funcion.opt==True: self.mejor_total = float('-inf')
        else: self.mejor_total = float('+inf')

        self.elitismo=elitismo        
        

    def tamGenes(self, precision):   
        ret = []
        for i in range(self.num_genes):
            ret.append(self.tamGen(precision, self.funcion.xMin[i], self.funcion.xMax[i]))
        return ret

    def tamGen(self, precision, min, max):
        return math.ceil((math.log10(((max-min)/precision)+1)/math.log10(2)))

    def ejecuta(self):
        selec=[]

        self.init_poblacion()    
        self.evaluacion_poblacion()
                
        
        while self.generaciones > 0:
            selec = self.seleccion_poblacion(self.tam_poblacion, 5)
            
            self.poblacion = self.cruce_poblacion(selec)
            self.poblacion = self.mutacion_poblacion(self.poblacion)
            
            self.evaluacion_poblacion()            
            
            self.generaciones-=1
        
                
        return self.mejor_total


    def init_poblacion(self):
        self.poblacion = [Individuo(self.num_genes, self.tam_genes, self.funcion.xMax, self.funcion.xMin, ind=None) for _ in range(self.tam_poblacion)]


    # TODO 
        # PRESION SELECTIVA
    def evaluacion_poblacion(self):
        
        self.fitness_total=0
        self.prob_seleccion = [(0) for _ in range(self.tam_poblacion)]
        self.prob_seleccionAcum = [(0) for _ in range(self.tam_poblacion)]
        if self.funcion.opt==True: 
            mejor_generacion = float('-inf')
            peor_generacion = float('+inf')
        else: 
            mejor_generacion = float('+inf')
            peor_generacion = float('-inf')
        mejor_generacionInd=None


        for i in range(self.tam_poblacion):            
            self.poblacion[i].calcular_fenotipo()
			
		

        fit=0.0
        #fitnessTotalAdaptado = 0.0
        for i in range(self.tam_poblacion):
            fit=self.funcion.fitness(self.poblacion[i].fenotipo)
            self.poblacion[i].fitness=fit
            self.fitness_total+=fit

            #if fit>mejor_generacion: mejor_generacion=fit
            if(self.funcion.cmpBool(fit, mejor_generacion)) :
                mejor_generacion=fit;	
                mejor_generacionInd=self.poblacion[i]
            peor_generacion=self.funcion.cmpPeor(peor_generacion,fit)
			

        #if mejor_generacion>self.mejor_total: self.mejor_total=mejor_generacion
        if(self.funcion.cmpBool(mejor_generacion, self.mejor_total)):
            self.mejor_total=mejor_generacion;	
            self.mejor_ind=mejor_generacionInd
		


        """self.progreso_generaciones[0].append(self.mejor_total)
        self.progreso_generaciones[1].append(mejor_generacion)
        self.progreso_generaciones[2].append((self.fitness_total/self.tam_poblacion))"""
        

        acum=0.0
        if peor_generacion < 0: peor_generacion *= -1

        if self.funcion.opt==False:
            self.fitness_total = self.tam_poblacion * 1.05 * peor_generacion - self.fitness_total
            for i in range(self.tam_poblacion):
                self.prob_seleccion[i] = 1.05 * peor_generacion - self.poblacion[i].fitness
                self.prob_seleccion[i] /= self.fitness_total
                acum += self.prob_seleccion[i]
                self.prob_seleccionAcum[i] = acum			
        else:
            self.fitness_total = self.tam_poblacion * 1.05 * peor_generacion + self.fitness_total
            for i in range(self.tam_poblacion):
                self.prob_seleccion[i] = 1.05 * peor_generacion + self.poblacion[i].fitness
                self.prob_seleccion[i] /= self.fitness_total
                acum += self.prob_seleccion[i]
                self.prob_seleccionAcum[i] = acum
			
		

        """for i in range(self.tam_poblacion):
            self.prob_seleccion[i] = self.poblacion[i].fitness/self.fitness_total
            acum+=self.prob_seleccion[i]
            self.prob_seleccionAcum[i]=acum
        """

    
    def seleccion_poblacion(self, tam_seleccionados, k):         
        ret=[]
        if self.seleccion_idx==0: ret=self.seleccion.ruleta(self.poblacion, self.prob_seleccionAcum, tam_seleccionados)
        elif self.seleccion_idx==1: ret= self.seleccion.tornedoDeterministico(self.poblacion, tam_seleccionados, k)
        elif self.seleccion_idx==2: ret= self.seleccion.torneoProbabilistico(self.poblacion, k, 0.9, tam_seleccionados)
        elif self.seleccion_idx==3: ret= self.seleccion.estocasticoUniversal(self.poblacion,self.prob_seleccionAcum,tam_seleccionados)
        elif self.seleccion_idx==4: ret= self.seleccion.truncamiento(self.poblacion,self.prob_seleccion, 0.5, tam_seleccionados)
        elif self.seleccion_idx==5: ret= self.seleccion.restos(self.poblacion,self.prob_seleccion, self.prob_seleccionAcum, tam_seleccionados)
        else: ret=[] # TODO RANKING
        return ret

    def cruce_poblacion(self, selec):
        ret=[]
        if self.cruce_idx==0: ret=self.cruce.cruce_monopuntoBin(selec)
        return ret
        

    def mutacion_poblacion(self, selec):
        ret=[]    
        ret = self.mutacion.mut_basicaBin(selec)
        return ret

# --------------------------------------------------------------------------------------------------------------
# -- MAIN ------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

def main():
    AG=AlgoritmoGenetico()
    
    seleccion_opt = ["Ruleta", 
                         "Torneo Determinista", 
                         "Torneo Probabilístico", 
                         "Estocástico Universal",
                         "Truncamiento",
                         "Restos",
                         "Ranking"]
        
    cruce_opt = ["Básica", 
                    "Uniforme"]
    
    mutacion_opt = ["Básica"]

    funcion_opt = ["F1: Calibracion y Prueba",
                    "F2: Mishra Bird",
                    "F3: Holder table",
                    "F4: Michalewicz (Binaria)"]
        
    tam_poblacion=100
    generaciones=100

    # 0: Ruleta | 1: Torneo Determinista  | 2: Torneo Probabilístico | 3: Estocástico Universal 
    #           | 4: Truncamiento  | 5: Restos | 6: Ranking
    seleccion_idx=0
    # 0: Basica  | 1:  Uniforme
    cruce_idx=0
    prob_cruce=0.6
    mut_idx=0 # Solo hay una (por ahora)
    prob_mut=0.05
    precision=0.01
    funcion_idx=1
    d=2
    elitismo=0

    AG.set_valores( tam_poblacion, 
                    generaciones, 
                    seleccion_idx,
                    cruce_idx, 
                    prob_cruce,
                    mut_idx, 
                    prob_mut,
                    precision, 
                    funcion_idx, 
                    d, 
                    elitismo)               

    print("\nFuncion: {}\tSeleccion: {}\tCruce: {}\tMutacion:{}\t".format(funcion_opt[funcion_idx],
                                                                      seleccion_opt[seleccion_idx],
                                                                      cruce_opt[cruce_idx],
                                                                      mutacion_opt[0]))
    totalTimeStart = MPI.Wtime()
    val=AG.ejecuta()
    totalTimeEnd = MPI.Wtime()
    print("Valor Optimo: {}\n".format(val))
    print("Tiempo de ejecucion total: {}\n".format(totalTimeEnd-totalTimeStart))


main()
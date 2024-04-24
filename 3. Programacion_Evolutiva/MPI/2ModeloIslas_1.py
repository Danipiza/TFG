from mpi4py import MPI # UCM NO FUNCIONA (NO ESTA LA BIBLIOTECA, TAMPOCO MATPLOT)
import sys
import os
import random
import math
import queue

from abc import ABC, abstractmethod 
from collections import deque
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import re

#mpiexec -np 5 python 2ModeloIslas_1.py


"""
Metodo 2. Modelo de islas. (Sin conectar, solo envian al master sus mejores individuos)

El MASTER envia los parametros a los WORKERS.
Cada WORKER se encarga de su poblacion.
"""



def GUI(fits):    
    # Create figure and axes
    #fig, axs = plt.subplots(2, 2, figsize=(18, 12), gridspec_kw={'width_ratios': [1, 2]})
    n=len(fits)
    # Define data for the first plot
    x1 = [i for i in range(1, n + 1)]  
    # Define data for the second plot       

    # Crear la figura y GridSpec
    fig = plt.figure(figsize=(10, 6))
    gs = GridSpec(1, 1, figure=fig)

    # Grafico 1 (arriba a la izquierda)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(x1, fits, color='b', linestyle='-')    
    ax1.set_xlabel('Generaciones Master')
    ax1.set_ylabel('Fitness')
    ax1.set_title('2D-Plot"')
    ax1.grid(True)

    
    
    
    plt.tight_layout() # Ajustar la disposición de los subplots    
    plt.show() # Mostrar los gráficos

# -----------------------------------------------------------------------------------------------
# --- INDIVIDUO ---------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------



class Gen:
    def __init__(self, l, v):
        self.v = []

        if v is not None: self.v=[(v[i]) for i in range(len(v))]
        else: self.v=[(random.randint(0,1)) for i in range(l)]

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
        for i in range(len(gen.v)-1,-1,-1):
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

class IndividuoReal:
    def __init__(self, aviones, vInd):
        self.v=[]
        self.fitness=0.0

        if vInd is not None:  
            self.fitness=vInd.fitness
            for x in vInd.v:
                self.v.append(x)
        else:
            self.init(aviones)

    
          

    def init(self, aviones):
        self.v=[]
        for i in range(aviones):		
            self.v.append(i)
		
        # shuffle
        for i in range(aviones-1,0,-1):
            j=random.randint(0, i)  
            temp=self.v[i]
            self.v[i]=self.v[j]
            self.v[j]=temp

# PADRE DE LOS NODOS DE LOS ARBOLES
class Exp(ABC):
    def __init__(self):
        self.x=0
        self.y=0
        self.tam=0
        self.operacion=""
        self.repeat=0    
    
    def putX(self, x):
        self.x = x

    def getX(self):
        return self.x

    def putY(self, y):
        self.y=y

    def getY(self):
        return self.y

    def putTam(self, tam):
        self.tam=tam

    def getTam(self):
        return self.tam

    def putOperacion(self, op):
        self.operacion=op

    def getOperacion(self):
        return self.operacion

    def getOp(self):
        if self.operacion=="Salta":
            return str(self.operacion[0])+str(self.x)+str(self.y)
        else: return str(self.operacion[0])

    @abstractmethod
    def setHijo(self, i, hijo):
        pass
    
    @abstractmethod
    def getHijo(self, i):
        pass

    @abstractmethod
    def duplica(self):
        pass

# NO TERMINALES
class Suma(Exp):
    def __init__(self, ops=None):
        super().__init__()
        self.ops=[None, None]
        self.putTam(2)             # Numero de hijos
        self.putOperacion("Suma")  # Nombre de la operacion

        if ops is None:
            self.ops[0]=None        # Hijo 1
            self.ops[1]=None        # Hijo 2
        else:
            self.ops[0]=ops[0]
            self.ops[1]=ops[1]
            self.putX((self.ops[0].getX()+self.ops[1].getX())%8) # Posicion X
            self.putY((self.ops[0].getY()+self.ops[1].getY())%8) # Posicion Y

    # toString()
    def __str__(self):
        return "SUMA(("+str(self.ops[0])+"), ("+str(self.ops[1])+"))"

    def setHijo(self, i, hijo):    # Pone un hijo i es izquierda o derecha
        self.ops[i]=hijo
        self.putX((self.getX() + hijo.getX()) % 8)   
        self.putY((self.getY() + hijo.getY()) % 8)   

    def getHijo(self, i):
        return self.ops[i]

    def duplica(self):
        return Suma()

class Salta(Exp):
    def __init__(self, ops=None):
        super().__init__()
        self.ops=[None]             
        self.putTam(1)                     # Numero de hijos (solo 1)
        self.putOperacion("Salta")         # Nombre de la operacion

        if ops is None: self.ops[0]=None    # Solo tiene uno
        else:
            self.ops[0]=ops[0]              # Solo tiene uno
            self.putX(self.ops[0].getX()) # Posicion X
            self.putY(self.ops[0].getY()) # Posicion Y

    # toString()
    def __str__(self):
        return "SALTA("+str(self.ops[0])+")"

    def setHijo(self, i, hijo):  # Pone un hijo i es izquierda o derecha
        self.ops[i]=hijo
        self.putX(hijo.getX())
        self.putY(hijo.getY())

    def getHijo(self, i):
        return self.ops[i]

    def duplica(self):
        return Salta()

class Progn(Exp):
    def __init__(self, ops=None):
        super().__init__()
        self.ops = [None, None]
        self.putTam(2)  # Number of children
        self.putOperacion("Progn")  # Operation name

        if ops is None:
            self.ops[0] = None  
            self.ops[1] = None  
        else:
            self.ops[0] = ops[0]  # Hijo 1
            self.ops[1] = ops[1]  # Hijo 2
            self.putX(self.ops[1].getX())  # X position
            self.putY(self.ops[1].getY())  # Y position

    def __str__(self):
        return "PROGN(("+str(self.ops[0])+"), ("+str(self.ops[1])+"))"

    def setHijo(self, i, hijo):  # Pone un hijo i es izquierda o derecha
        self.ops[i] = hijo
        self.putX(hijo.getX())
        self.putY(hijo.getY())

    def getHijo(self, i):
        return self.ops[i]

    def duplica(self):
        return Progn()

# TERMINALES
class Izquierda(Exp):
    def __init__(self):
        super().__init__()
        self.putTam(0)                 # No tiene hijos
        self.putOperacion("Izquierda") # Nombre de la operacion
        self.putX(0)                   # Siempre devuelve (0, 0)
        self.putY(0)

    # toString()
    def __str__(self):
        return "IZQUIERDA"

    def setHijo(self, i, hijo):
        pass

    def getHijo(self, i):
        return None

    def duplica(self):
        return Izquierda()

class Avanza(Exp):
    def __init__(self):
        super().__init__()
        self.putTam(0)                 # No tiene hijos
        self.putOperacion("Avanza")    # Nombre de la operacion
        self.putX(0)                   # Siempre devuelve (0, 0)
        self.putY(0)

    # toString()
    def __str__(self):
        return "AVANZA"

    def setHijo(self, i, hijo):
        pass

    def getHijo(self, i):
        return None

    def duplica(self):
        return Avanza()
    
class Constante(Exp):
    def __init__(self, filas, columnas, constante):
        super().__init__()
        
        self.filas=filas
        self.columnas=columnas

        self.putTam(0)                          # No tiene hijos
        self.putOperacion("Constante")          # Nombre de la operacion
        # Devuelve el su valor (X,Y)
        if constante==None: 
            self.putX(random.randint(0,filas-1))    
            self.putY(random.randint(0,columnas-1))
        else:
            self.putX(constante.getX())    
            self.putY(constante.getY())

    def __str__(self):
        return str(self.getX()) + "," + str(self.getY())

    def setHijo(self, i, hijo):
        pass

    def getHijo(self, i):
        return None

    def duplica(self):
        return Constante(self.filas, self.columnas, constante=None)


class Arbol:
    def __init__(self, modo, profundidad, filas, columnas):
        self.raiz=None # Exp
        self.profMax=profundidad
        self.filas=filas
        self.columnas=columnas
        self.nodos=0

        self.init_raiz()
        self.inicializa_arbol(self.raiz, modo)

    def inicializa_arbol(self, exp, modo):
        if modo==0: self.completo(exp, 0)
        else: self.creciente(exp, 0)

    def init_raiz(self):
        self.nodos+=1
        func=random.randint(0, 2)
        
        if func==0: self.raiz=Progn()
        elif func==1: self.raiz=Salta()
        elif func==2: self.raiz=Suma()

    def creciente(self, nodo, profundidad):
        if profundidad+1<self.profMax:
            hijos=nodo.getTam()
            
            for i in range(hijos):
                self.nodos+=1
                func=random.randint(0, 5)
                if func==0: hijo=Progn()
                elif func==1: hijo=Salta()
                elif func==2: hijo=Suma()
                elif func==3: hijo=Avanza()
                elif func==4: hijo=Constante(self.filas, self.columnas,constante=None)
                else: hijo=Izquierda()

                nodo.setHijo(i, self.completo(hijo, profundidad+1))
        else:
            hijos=nodo.getTam()
            for i in range(hijos):
                self.nodos+=1
                func=random.randint(0, 2)
                if func==0: hijo=Avanza()
                elif func==1: hijo=Constante(self.filas, self.columnas,constante=None)
                else: hijo=Izquierda()
                
                nodo.setHijo(i, hijo)
        return nodo

    def completo(self, nodo, profundidad):
        if profundidad+1<self.profMax:
            hijos=nodo.getTam()
            for i in range(hijos):
                self.nodos+=1
                func=random.randint(0, 2)
                if func==0: hijo=Progn()
                elif func==1: hijo=Salta()
                else: hijo=Suma()

                nodo.setHijo(i, self.completo(hijo, profundidad+1))
        else:
            hijos=nodo.getTam()
            for i in range(hijos):
                self.nodos+=1
                func=random.randint(0, 2)
                if func==0: hijo=Avanza()
                elif func==1: hijo=Constante(self.filas, self.columnas,constante=None)
                else: hijo=Izquierda()
                
                nodo.setHijo(i, hijo)
        return nodo

    def get_nodos(self):
        return self.nodos

    def __str__(self):
        return str(self.raiz)


class IndividuoArbol:

    def __init__(self, modo, profundidad, filas, columnas, ind):
        self.gen=None   # Arbol
        self.profundidad=0        
        self.filas=0
        self.columnas=0
        
        
        if ind is not None:  
            self.profundidad=ind.profundidad
            self.filas=ind.filas
            self.columnas=ind.columnas

            self.gen=Arbol(modo,self.profundidad,self.filas, self.columnas)      
            self.gen.raiz=self.duplicaArbol(ind.gen.raiz)
        else: 
            self.gen=Arbol(modo,profundidad,filas, columnas)   
            
            self.profundidad=profundidad
            self.filas=filas
            self.columnas=columnas

        self.fitness=0.0        

        #A: avanza, I: izquierda, SXY: salto x y
        self.operaciones=[]     # List<String>       
	
        self.funcionales=[]     # List<Pair<Exp,Integer>>
        
        invisible = Salta()
        invisible.setHijo(0, self.gen.raiz)
        self.funcionales.append((invisible, 0)) # PADRE DE LA RAIZ       
        self.terminales=[]      # List<Pair<Exp,Integer>> 
        
        self.nodos=0            # Numero de nodos para el control de bloating	
        self.recorreArbol(self.gen.raiz)
        #self.nodos=self.gen.getNodos()            
    
    def duplicaArbol(self, original):
        """
        original: Exp
        
        (return Exp)
        """
        nuevo=original.duplica()
        n=original.getTam()
        for i in range(n):
            nuevo.setHijo(i, self.duplicaArbol(original.getHijo(i)))
        return nuevo

    def reiniciaListas(self, nodo):  
        """
        nodo: Exp
        """      
        self.nodos=0
        
        self.operaciones=[]
        self.funcionales=[]
        invisible=Salta()
        invisible.setHijo(0, self.gen.raiz)
        self.funcionales.append((invisible, 0))
        self.terminales=[]

        self.recorreArbol(nodo)

    def recorreArbol(self, nodo):   
        """
        nodo: Exp
        """     
        self.nodos += 1
        n=nodo.getTam()
        for i in range(n):
            self.recorreArbol(nodo.getHijo(i))
            if nodo.getHijo(i).getTam()==0:
                self.terminales.append((nodo, i))
            else: self.funcionales.append((nodo, i))
        
        if nodo.getOperacion()=="Avanza": self.operaciones.append("A")
        elif nodo.getOperacion()=="Izquierda": self.operaciones.append("I")
        elif nodo.getOperacion()=="Salta": 
            self.operaciones.append("S" + str(nodo.getX()) + str(nodo.getY()))

    # toString()
    def __str__(self):
        return str(self.gen)

class IndividuoGramatica:
    class Coord:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    """
    GRAMATICA SIN NO TERMINALES NI TERMINALES OPCIONALES
	<start> := progn(<op>, <op>) | salta(<op>) | suma(<op>, <op>)
	
	<op> := progn(<op>, <op>) | salta(<op>) | suma(<op>, <op>) 
		  	| avanza | constante(<num>, <num>) | izquierda
		  	
  	<num> := 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 // O PONER RANDOM Y ASI NO USAR CODONES
  	
  	NUEVO FUNCIONA PEOR:
  	<start> := <op>
	
	<op> := <no_terminal> | <terminal>
	
	<no_terminal> := progn(<op>, <op>) | salta(<op>) | suma(<op>, <op>) 
		  	
  	<terminal> := avanza | constante(<num>, <num>) | izquierda
	
	
	CON OPCIONALES:
	<start> := progn(<op>, <op>) | salta(<op>) | suma(<op>, <op>) | salta_a(<op>)
	
	<op> := progn(<op>, <op>) | salta(<op>) | suma(<op>, <op>) | salta_a(<op>)
		  	| avanza | constante(<num>, <num>) | izquierda | derecha | retrocede | mueve
		  	
  	<num> := 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 // O PONER RANDOM Y ASI NO USAR CODONES
    
    """

    def __init__(self, tam_cromosoma, filas, columnas, cromosoma, ind):
        self.tam_cromosoma=0
        self.filas=0
        self.columnas=0
        self.fitness=0
        self.nodos=0

        self.cont=0
        self.gramatica=""
        
        self.cromosoma=[]
        self.operaciones=[]

        if ind is not None:
            self.tam_cromosoma=ind.tam_cromosoma
            self.filas=ind.filas
            self.columnas=ind.columnas
            self.fitness=ind.fitness
            self.nodos=ind.nodos


            self.gramatica=ind.gramatica
            for x in ind.cromosoma:
                self.cromosoma.append(x)
            for x in ind.operaciones:
                self.operaciones.append(x)

        else:
            self.tam_cromosoma=tam_cromosoma
            self.filas=filas
            self.columnas=columnas
            if cromosoma is not None:
                for x in cromosoma:
                    self.cromosoma.append(x)
            else:
                self.cromosoma=[]
                for i in range(self.tam_cromosoma):
                    self.cromosoma.append(random.randint(0, 255))

            self.init()
            

      


    

    def init(self):
        self.cont=0
        self.gramatica=""
        self.operaciones=[]


        try:
            self.start()
        except Exception as e:
            self.cromosoma=[]
            for i in range(self.tam_cromosoma):
                self.cromosoma.append(random.randint(0, 255))
            self.init()

    def start(self):
        act=""
        tamHijos=2

        x=self.cromosoma[0]%3
        if x==0: act="PROGN"
        elif x==1:
            act="SALTA"
            tamHijos=1
        else: act="SUMA"
        self.cont=1

        self.op(act, tamHijos)

    def op(self, act, tam):
        self.gramatica+=act
        self.nodos+=1

        if tam==0:
            if act=="AVANZA": return self.Coord(0, 0)
            elif act=="IZQUIERDA": return self.Coord(0, 0)
            else:
                match=re.search(r'\d+', act)
                number1=match.group()
                match.find()
                number2=match.group()

                return self.Coord(int(number1), int(number2))

        self.gramatica+="("
        coordsH=[]

        for i in range(tam):
            hijo=""
            tamHijos=2
            c=self.cromosoma[self.cont] % 6
            if c==0: hijo="PROGN"
            elif c==1:
                hijo="SALTA"
                tamHijos=1
            elif c==2: hijo="SUMA"
            elif c==3:
                hijo="AVANZA"
                tamHijos=0
                self.operaciones.append("A")
            elif c==4:
                tmpX=random.randint(0, self.filas-1)
                tmpY=random.randint(0, self.columnas-1)
                hijo="CONSTANTE("+str(tmpX)+","+str(tmpY)+")"
                tamHijos = 0
            else:
                hijo="IZQUIERDA"
                tamHijos=0
                self.operaciones.append("I")

            coordsH.append(self.op(hijo, tamHijos))
            if tam==2 and i==0:
                self.gramatica+=", "

        self.gramatica+=")"

        if act=="PROGN": return coordsH[1]
        elif act=="SALTA":
            self.operaciones.append("S"+str(coordsH[0].x)+str(coordsH[0].y))
            return coordsH[0]
        else:
            return self.Coord((coordsH[0].x+coordsH[1].x)%self.filas,
                              (coordsH[0].y+coordsH[1].y)%self.columnas)

    # TODO?
    def __str__(self):
        aux=""
        for x in self.operaciones:
            aux+=x+", "
        return self.gramatica
  

# -----------------------------------------------------------------------------------------------
# --- FUNCION -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------



class Funcion(ABC):
    xMax=[]      # double[]. Valores maximos de los elementos de los individuos
    xMin=[]      # double[]. Valores minimos
    opt=False        # booleano. maximizar: True, minimizar: False

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
        exp=abs(1-(math.sqrt(nums[0]**2+nums[1]**2))/math.pi)
        ret=math.sin(nums[0])*math.cos(nums[1])*math.exp(exp)
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
        ret=0.0        
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


class FuncionA(Funcion):

    def __init__(self, aviones, pistas, tipo_avion, TEL):
        self.sep = [[1, 1.5, 2],
                    [1, 1.5, 1.5],
            		[1, 1, 1]]
        
        self.aviones=aviones
        self.pistas=pistas
		
        self.tipo_avion=tipo_avion
        self.TEL=TEL
    
    # TODO COMPROBAR
    def fitness(self, avion):
        """
        avion: List[int]
        """
        # -10 es el tiempo inicial para que el primer avion en llegar no tenga separacion 
        tla=[deque([(2, -10.0)]) for _ in range(self.pistas)]

        fitness=0.0
        n=len(avion)
        for i in range(n):
            new_tla=0 
            menor_tla=24.0
            index_pista=0
            
            for j in range(self.pistas):
                # Tiempo de Llegada Asignado (TLA) para la pista j + la separacion de esta pista (SEP)
                # o el Tiempo Estimada de Llegada (TEL)
                new_tla=max(tla[j][-1][1]+self.sep[tla[j][-1][0]][self.tipo_avion[avion[i]]], 
                            self.TEL[j][avion[i]])
               
                if new_tla<menor_tla:
                    menor_tla=new_tla
                    index_pista=j

            tla[index_pista].append((self.tipo_avion[avion[i]], menor_tla))

            menor_tel=24.0
            for j in range(self.pistas):
                if self.TEL[j][avion[i]]<menor_tel:
                    menor_tel=self.TEL[j][avion[i]]

            fitness+=(menor_tla-menor_tel)**2

        return fitness
    
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

class FuncionArbol:
    def __init__(self, filas, columnas, ticks, obstaculos):
        self.opt=True
        self.filas=filas
        self.columnas=columnas
        self.ticks=ticks

        self.direccionAvanza=[[-1,0],[0,-1],[1,0],[0,1]]
        self.direccionSalta=[[-1,1],[-1,-1],[1,-1],[1,1]]

        self.tablero=[[0 for _ in range(columnas)] for _ in range(filas)]
        self.obstaculos=obstaculos
        if obstaculos:
            for i in range(filas):
                for j in range(columnas):
                    if random.random()<0.05:
                        self.tablero[i][j]=-1

    def fitness(self, ind):
        fitness=0.0
        
        if len(ind.operaciones)==0: return 0.0
        
        M = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        if self.obstaculos:
            for i in range(self.filas):
                for j in range(self.columnas):
                    if self.tablero[i][j] == -1:
                        M[i][j] = -1
        
        x=4
        y=4

        dir=0
        cont=0
        n=len(ind.operaciones)
        ops=[tmp[0] for tmp in ind.operaciones]
        
        tick=0
        while tick<self.ticks:
            if ops[cont]=='I': dir=(dir+1)%4
            elif ops[cont]=='A':
                tmpX=(x+self.direccionAvanza[dir][0])%self.filas
                tmpY=(y+self.direccionAvanza[dir][1])%self.columnas
                
                if tmpX<0: tmpX=self.filas+tmpX
                if tmpY<0: tmpY=self.columnas+tmpY
                if M[tmpX][tmpY]!=-1:
                    x=tmpX
                    y=tmpY
                    if M[x][y]==0:
                        fitness+=1
                        M[x][y]=1
            else:                
                tmpX=(x+self.direccionSalta[dir][0]*int(ind.operaciones[cont][1]))%self.filas
                tmpY=(y+self.direccionSalta[dir][1]*int(ind.operaciones[cont][2]))%self.columnas
                if tmpX<0: tmpX=self.filas+tmpX
                if tmpY<0: tmpY=self.columnas+tmpY
                if M[tmpX][tmpY]!=-1:
                    x=tmpX
                    y=tmpY
                    if M[x][y]==0:
                        fitness+=1
                        M[x][y]=1
            
            tick+=1
            cont=(cont+1)%n
        
        return fitness

    def matrix(self, ind):
        M=[[0 for _ in range(self.columnas)]  for _ in range(self.filas)]
        x=4
        y=4

        dir=0
        cont=0
        n=len(ind.operaciones)
        ops=[list(tmp) for tmp in ind.operaciones]
        
        ticks=0
        while ticks<self.ticks:
            if ops[cont][0]=='I': dir=(dir+1)%4
            elif ops[cont][0]=='A':
                tmpX=(x+self.direccionAvanza[dir][0])%self.filas
                tmpY=(y+self.direccionAvanza[dir][1])%self.columnas
                if tmpX<0: tmpX=self.filas+tmpX
                if tmpY<0: tmpY=self.columnas+tmpY
                if M[tmpX][tmpY]!=-1:
                    x=tmpX
                    y=tmpY
                    if M[x][y]==0:
                        M[x][y]=1
            else:
                tmpX=(x+self.direccionSalta[dir][0]*int(ind.operaciones[cont][1]))%self.filas
                tmpY=(y+self.direccionSalta[dir][1]*int(ind.operaciones[cont][2]))%self.columnas
                if tmpX<0: tmpX=self.filas+tmpX
                if tmpY<0: tmpY=self.columnas+tmpY
                if M[tmpX][tmpY]!=-1:
                    x=tmpX
                    y=tmpY
                    if M[x][y]==0: M[x][y]=1
            
            ticks+=1
            cont=(cont+1)%n
        
        return M
    
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

# -----------------------------------------------------------------------------------------------
# --- SELECCION ---------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------

class Pair():
    def __init__(self, key, value):
        self.key=key
        self.value=value

    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key=key

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value=value

    def __str__(self):
        return "(" + str(self.key) + ", " + str(self.value) + ")"

class Seleccion:
    def __init__(self, tam_poblacion, opt):        
        self.tam_poblacion=tam_poblacion    # int  
        self.opt=opt                        # Boolean
    
    
    def busquedaBinaria(self, x, prob_acumulada):
        i=0
        j=self.tam_poblacion-1
        while i<j:
            m=(j+i)//2
            if x>prob_acumulada[m]: i=m+1
            elif x<prob_acumulada[m]: j=m
            else: return m
        return i

    def ruletaBin(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        for _ in range(tam_seleccionados):
            rand=random.random()
            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                     ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
        return seleccionados

    def ruletaReal(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        for _ in range(tam_seleccionados):
            rand=random.random()
            seleccionados.append(IndividuoReal(aviones=None,
                                           vInd=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
        return seleccionados
    
    def ruletaArbol(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        for _ in range(tam_seleccionados):
            rand=random.random()
            seleccionados.append(IndividuoArbol(modo=None, profundidad=None, filas=None, columnas=None,
                                           ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
        return seleccionados
    
    def ruletaGramatica(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        for _ in range(tam_seleccionados):
            rand=random.random()
            seleccionados.append(IndividuoGramatica(tam_cromosoma=None, filas=None, columnas=None, 
                                    cromosoma=None, ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
        return seleccionados
    

    def torneoDeterministicoBin(self, poblacion, k, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
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

            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                     ind=poblacion[ind]))

        return seleccionados
        
    def torneoDeterministicoReal(self, poblacion, k, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
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

            seleccionados.append(IndividuoReal(aviones=None,
                                               vInd=poblacion[ind]))

        return seleccionados

    def torneoDeterministicoArbol(self, poblacion, k, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
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

            seleccionados.append(IndividuoArbol(modo=None, profundidad=None, filas=None, columnas=None,
                                           ind=poblacion[ind]))

        return seleccionados
    
    def torneoDeterministicoGramatica(self, poblacion, k, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
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

            seleccionados.append(IndividuoGramatica(tam_cromosoma=None, filas=None, columnas=None, 
                                    cromosoma=None, ind=poblacion[ind]))

        return seleccionados
    
    


    def torneoProbabilisticoBin(self, poblacion, k, p, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
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

            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                     ind=poblacion[ind]))

        return seleccionados
    
    def torneoProbabilisticoReal(self, poblacion, k, p, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
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

            seleccionados.append(IndividuoReal(aviones=None,
                                               vInd=poblacion[ind]))

        return seleccionados
    
    def torneoProbabilisticoArbol(self, poblacion, k, p, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
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

            seleccionados.append(IndividuoArbol(modo=None, profundidad=None, filas=None, columnas=None,
                                           ind=poblacion[ind]))

        return seleccionados
    
    def torneoProbabilisticoGramatica(self, poblacion, k, p, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
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

            seleccionados.append(IndividuoGramatica(tam_cromosoma=None, filas=None, columnas=None, 
                                    cromosoma=None, ind=poblacion[ind]))

        return seleccionados
    

    

    def estocasticoUniversalBin(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
		
        incr=1.0/tam_seleccionados
        rand=random.random()*incr
        for i in range(tam_seleccionados):       			
            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                     ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
			
            rand+=incr		

        return seleccionados
    
    def estocasticoUniversalReal(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
		
        incr=1.0/tam_seleccionados
        rand=random.random()*incr
        for i in range(tam_seleccionados):       			
            seleccionados.append(IndividuoReal(aviones=None,
                                               vInd=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
			
            rand+=incr		

        return seleccionados
    
    def estocasticoUniversalArbol(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
		
        incr=1.0/tam_seleccionados
        rand=random.random()*incr
        for i in range(tam_seleccionados):       			            
            seleccionados.append(IndividuoArbol(modo=None, profundidad=None, filas=None, columnas=None,
                                           ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
			
            rand+=incr		

        return seleccionados
    
    def estocasticoUniversalGramatica(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
		
        incr=1.0/tam_seleccionados
        rand=random.random()*incr
        for i in range(tam_seleccionados):       
            seleccionados.append(IndividuoGramatica(tam_cromosoma=None, filas=None, columnas=None, 
                                    cromosoma=None, ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
			
            rand+=incr		

        return seleccionados

    

    def truncamientoBin(self, poblacion, prob_seleccion, trunc, tam_seleccionados):
        seleccionados=[]
        
        pairs=[]
        for i in range(tam_seleccionados): 
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))
		
        pairs=sorted(pairs, key=lambda x: x.value, reverse=False)
        x=0
        num=int(1.0/trunc)
        n=len(pairs)-1
        for i in range(int((tam_seleccionados)*trunc)+1):		
            j=0
            while j<num and x<tam_seleccionados:            
                seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                         ind=pairs[n-i].get_key()))
                j+=1
                x+=1
			
		
        return seleccionados
    
    def truncamientoReal(self, poblacion, prob_seleccion, trunc, tam_seleccionados):
        seleccionados=[]
        
        pairs=[]
        for i in range(tam_seleccionados): 
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))
		
        pairs=sorted(pairs, key=lambda x: x.value, reverse=False)
        x=0
        num=int(1.0/trunc)
        n=len(pairs)-1
        for i in range(int((tam_seleccionados)*trunc)+1):		
            j=0
            while j<num and x<tam_seleccionados:            
                seleccionados.append(IndividuoReal(aviones=None,
                                                   vInd=pairs[n-i].get_key()))
                j+=1
                x+=1
			
		
        return seleccionados
    
    def truncamientoArbol(self, poblacion, prob_seleccion, trunc, tam_seleccionados):
        seleccionados=[]
        
        pairs=[]
        for i in range(tam_seleccionados): 
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))
		
        pairs=sorted(pairs, key=lambda x: x.value, reverse=False)
        x=0
        num=int(1.0/trunc)
        n=len(pairs)-1
        for i in range(int((tam_seleccionados)*trunc)+1):		
            j=0
            while j<num and x<tam_seleccionados:           
                seleccionados.append(IndividuoArbol(modo=None, profundidad=None, filas=None, columnas=None,
                                           ind=pairs[n-i].get_key()))
                j+=1
                x+=1
			
		
        return seleccionados
    
    def truncamientoGramatica(self, poblacion, prob_seleccion, trunc, tam_seleccionados):
        seleccionados=[]
        
        pairs=[]
        for i in range(tam_seleccionados): 
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))
		
        pairs=sorted(pairs, key=lambda x: x.value, reverse=False)
        x=0
        num=int(1.0/trunc)
        n=len(pairs)-1
        for i in range(int((tam_seleccionados)*trunc)+1):		
            j=0
            while j<num and x<tam_seleccionados:           
                seleccionados.append(IndividuoGramatica(tam_cromosoma=None, filas=None, columnas=None, 
                                    cromosoma=None, ind=pairs[n-i].get_key()))
                j+=1
                x+=1
			
		
        return seleccionados
   

    

    def restosBin(self, poblacion, prob_seleccion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        
        x=0
        num=0
        aux=0.0		
        for i in range(tam_seleccionados):		
            aux=prob_seleccion[i]*(tam_seleccionados)
            num=int(aux)
			
            for j in range(num):
                seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                               ind=poblacion[i]))
                x+=1
				
		
        resto=[]
        func=random.randint(0,4) # Cambiar
        # SE SUMA LA PARTE DE elitismo PORQUE SINO SE RESTA 2 VECES, 
        # EN LA PARTE DE restos() Y LA FUNCION RANDOM
        if func==0: resto=self.ruletaBin(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==1: resto=self.torneoDeterministicoBin(poblacion, 3, tam_seleccionados-x)	
        elif func==2: resto=self.torneoProbabilisticoBin(poblacion, 3, 0.9, tam_seleccionados-x)
        elif func==3: resto=self.estocasticoUniversalBin(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==4: resto=self.truncamientoBin(poblacion, prob_acumulada, 0.5, tam_seleccionados-x) 
        else: resto=self.rankingBin(poblacion, prob_seleccion, 2, tam_seleccionados-x)
        
        for ind in resto:
            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                           ind=ind))
		

        return seleccionados
    
    def restosReal(self, poblacion, prob_seleccion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        
        x=0
        num=0
        aux=0.0		
        for i in range(tam_seleccionados):		
            aux=prob_seleccion[i]*(tam_seleccionados)
            num=int(aux)
			
            for j in range(num):
                seleccionados.append(IndividuoReal(aviones=None,
                                                   vInd=poblacion[i]))
                x+=1
				
			
        resto=[]
        func=random.randint(0,4) # Cambiar
        # SE SUMA LA PARTE DE elitismo PORQUE SINO SE RESTA 2 VECES, 
        # EN LA PARTE DE restos() Y LA FUNCION RANDOM
        if func==0: resto=self.ruletaReal(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==1: resto=self.torneoDeterministicoReal(poblacion, 3, tam_seleccionados-x)	
        elif func==2: resto=self.torneoProbabilisticoReal(poblacion, 3, 0.9, tam_seleccionados-x)
        elif func==3: resto=self.estocasticoUniversalReal(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==4: resto=self.truncamientoReal(poblacion, prob_acumulada, 0.5, tam_seleccionados-x) 
        else: resto=self.rankingReal(poblacion, prob_seleccion, 2, tam_seleccionados-x)
        
        for ind in resto:
            seleccionados.append(IndividuoReal(aviones=None,
                                               vInd=ind))
		

        return seleccionados

    def restosArbol(self, poblacion, prob_seleccion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        
        x=0
        num=0
        aux=0.0		
        for i in range(tam_seleccionados):		
            aux=prob_seleccion[i]*(tam_seleccionados)
            num=int(aux)
			
            for j in range(num):
                seleccionados.append(IndividuoArbol(modo=None, profundidad=None, filas=None, columnas=None,
                                           ind=poblacion[i]))
                x+=1
				
			
        resto=[]
        func=random.randint(0,4) # Cambiar
        # SE SUMA LA PARTE DE elitismo PORQUE SINO SE RESTA 2 VECES, 
        # EN LA PARTE DE restos() Y LA FUNCION RANDOM
        if func==0: resto=self.ruletaArbol(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==1: resto=self.torneoDeterministicoArbol(poblacion, 3, tam_seleccionados-x)	
        elif func==2: resto=self.torneoProbabilisticoArbol(poblacion, 3, 0.9, tam_seleccionados-x)
        elif func==3: resto=self.estocasticoUniversalArbol(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==4: resto=self.truncamientoArbol(poblacion, prob_acumulada, 0.5, tam_seleccionados-x) 
        else: resto=self.rankingArbol(poblacion, prob_seleccion, 2, tam_seleccionados-x)
        
        for ind in resto:            
            seleccionados.append(ind)
		

        return seleccionados

    def restosGramatica(self, poblacion, prob_seleccion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        
        x=0
        num=0
        aux=0.0		
        for i in range(tam_seleccionados):		
            aux=prob_seleccion[i]*(tam_seleccionados)
            num=int(aux)
			
            for j in range(num):
                seleccionados.append(IndividuoGramatica(tam_cromosoma=None, filas=None, columnas=None, 
                                    cromosoma=None, ind=poblacion[i]))
                x+=1
				
			
        resto=[]
        func=random.randint(0,4) # Cambiar
        # SE SUMA LA PARTE DE elitismo PORQUE SINO SE RESTA 2 VECES, 
        # EN LA PARTE DE restos() Y LA FUNCION RANDOM
        if func==0: resto=self.ruletaGramatica(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==1: resto=self.torneoDeterministicoGramatica(poblacion, 3, tam_seleccionados-x)	
        elif func==2: resto=self.torneoProbabilisticoGramatica(poblacion, 3, 0.9, tam_seleccionados-x)
        elif func==3: resto=self.estocasticoUniversalGramatica(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==4: resto=self.truncamientoGramatica(poblacion, prob_acumulada, 0.5, tam_seleccionados-x) 
        else: resto=self.rankingGramatica(poblacion, prob_seleccion, 2, tam_seleccionados-x)
        
        for ind in resto:            
            seleccionados.append(ind)
		

        return seleccionados

    
    
    def rankingBin(self, poblacion, prob_seleccion, beta, tam_seleccionados):
        seleccionados=[]

        pairs=[]
		
        for i in range(tam_seleccionados):
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))

        pairs.sort(key=lambda p: p.value, reverse=True)

        val=0.0
        acum=0.0
        prob_acumulada=[] # tam_selec

        for i in range(1,tam_seleccionados+1):		
            val=(beta-(2*(beta-1)*((i-1)/(tam_seleccionados-1.0))))/tam_seleccionados
            acum+=val
            prob_acumulada.append(acum)
				
		
        rand=0.0
        for i in range(tam_seleccionados):        
            rand = random.random()
            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                           ind=pairs[self.busquedaBinaria(rand, prob_acumulada)].get_key()))		
		
        return seleccionados
    
    def rankingReal(self, poblacion, prob_seleccion, beta, tam_seleccionados):
        seleccionados=[]

        pairs=[]
		
        for i in range(tam_seleccionados):
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))

        pairs.sort(key=lambda p: p.value, reverse=True)

        val=0.0
        acum=0.0
        prob_acumulada=[] # tam_selec

        for i in range(1,tam_seleccionados+1):		
            val=(beta-(2*(beta-1)*((i-1)/(tam_seleccionados-1.0))))/tam_seleccionados
            acum+=val
            prob_acumulada.append(acum)
				
		
        rand=0.0
        for i in range(tam_seleccionados):        
            rand = random.random()
            seleccionados.append(IndividuoReal(aviones=None,
                                               vInd=pairs[self.busquedaBinaria(rand, prob_acumulada)].get_key()))		
		
        return seleccionados

    def rankingArbol(self, poblacion, prob_seleccion, beta, tam_seleccionados):
        seleccionados=[]

        pairs=[]
		
        for i in range(tam_seleccionados):
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))

        pairs.sort(key=lambda p: p.value, reverse=True)

        val=0.0
        acum=0.0
        prob_acumulada=[] # tam_selec

        for i in range(1,tam_seleccionados+1):		
            val=(beta-(2*(beta-1)*((i-1)/(tam_seleccionados-1.0))))/tam_seleccionados
            acum+=val
            prob_acumulada.append(acum)
				
		
        rand=0.0
        for i in range(tam_seleccionados):        
            rand = random.random()		
            seleccionados.append(IndividuoArbol(modo=None, profundidad=None, filas=None, columnas=None,
                                           ind=pairs[self.busquedaBinaria(rand, prob_acumulada)].get_key()))
		
        return seleccionados

    def rankingGramatica(self, poblacion, prob_seleccion, beta, tam_seleccionados):
        seleccionados=[]

        pairs=[]
		
        for i in range(tam_seleccionados):
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))

        pairs.sort(key=lambda p: p.value, reverse=True)

        val=0.0
        acum=0.0
        prob_acumulada=[] # tam_selec

        for i in range(1,tam_seleccionados+1):		
            val=(beta-(2*(beta-1)*((i-1)/(tam_seleccionados-1.0))))/tam_seleccionados
            acum+=val
            prob_acumulada.append(acum)
				
		
        rand=0.0
        for i in range(tam_seleccionados):        
            rand = random.random()		
            seleccionados.append(IndividuoGramatica(tam_cromosoma=None, filas=None, columnas=None, 
                                    cromosoma=None, ind=pairs[self.busquedaBinaria(rand, prob_acumulada)].get_key()))
		
        return seleccionados

# -----------------------------------------------------------------------------------------------
# --- CRUCE -------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------

class Cruce:
    def __init__(self, p, tam_elite, aviones):
        self.p=p    # int
        self.tam_elite=tam_elite
        self.aviones=aviones
    
    def cruce_monopuntoBin(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)]
        if n%2==1:
            ret[n-1]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[n-1])
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
            ind2=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i+1])
            
            rand=random.random()
            if rand<self.p:                                               
                corte=random.randint(1,corte_maximo)
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
                        
            
            ret[i]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind1)
            ret[i+1]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind2)            
            i += 2     
               
        
        
        return ret
    
    def cruce_uniformeBin(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)]
        if n%2==1:
            ret[n-1]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[n-1])
            n-=1
        
        long_genes=[len(selec[0].genes[i].v) for i in range(len(selec[0].genes))]
        corte_maximo=-1
        for l in long_genes:
            corte_maximo+=l
        i=0

        long_genes=[len(selec[0].genes[i].v) for i in range(len(selec[0].genes))]
        cont=0 
        l=0
        for c in long_genes:
            l+=c
            long_genes[cont]=c
            cont+=1
        
        i=0      
        j=0
        k=0
        ind1=None
        ind2=None
        tmp=0
        while i<n:
            ind1=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i])
            ind2=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i+1])

            
            if random.random()>self.p:
                cont=0
                j=0

                for k in range(l):				
                    if random.random()<0.5:
                        tmp=ind1.genes[cont].v[j]
                        ind1.genes[cont].v[j]=ind2.genes[cont].v[j]
                        ind2.genes[cont].v[j]=tmp
                    
                    j+=1
                    if j==long_genes[cont]:
                        cont+=1
                        j=0

					
				
            
			
            ret[i]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind1)
            ret[i+1]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind2)            
            i+=2     
               
        
        
        return ret
    
    def PMX(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal(aviones=None,
                                   vInd=selec[n-1]) 
            n-=1 # Descarta al ultimo si es impar
		
		
		 
        i=0
        k=0
        ind1=None
        ind2=None
        """
        Se intercambian desde [corte1, corte2)
        """
        corte1=0
        corte2=0
        while i<n:
            ind1=IndividuoReal(aviones=None,
                               vInd=selec[i])
            ind2=IndividuoReal(aviones=None,
                               vInd=selec[i+1])
            if random.random()<self.p:                
                pareja1={} # {int, int}
                pareja2={} 

                corte1=int(random.random()*(self.aviones-2))
                corte2=corte1+int(random.random()*(self.aviones-corte1))
				
                # Se intercambia el intervalo a cortar
                # y se añade a un diccionario para hacer PMX
                for j in range(corte1,corte2):				
                    temp=ind1.v[j]
                    ind1.v[j] = ind2.v[j];					
                    ind2.v[j] = temp;		
					
                    pareja1[ind1.v[j]]=ind2.v[j]
                    pareja2[ind2.v[j]]=ind1.v[j]
				
                # Recorre los individuos por el final del intervalo a cortar
                for j in range(self.aviones-(corte2-corte1)):
                    # Si el elemento del Padre1 no esta en el intervalo copiado
                    # del Padre2 se deja como esta y avanza al siguiente.
                    # Si esta en el intervalo, se busca 
                    # el elemento correspondiente con los diccionarios
                    if ind1.v[(corte2+j)%self.aviones] in pareja1:                    
                        p=pareja1[ind1.v[(corte2+j)%self.aviones]]

                        while p in pareja1:                        
                            p=pareja1[p]						
                        ind1.v[(corte2+j)%self.aviones]=p

                    if ind2.v[(corte2+j)%self.aviones] in pareja2:
                        p=pareja2[ind2.v[(corte2+j)%self.aviones]]

                        while p in pareja2:                        
                            p=pareja2[p]						
                        ind2.v[(corte2+j)%self.aviones]=p

				
			
            ret[i]=IndividuoReal(aviones=None,
                               vInd=ind1)
            ret[i+1]=IndividuoReal(aviones=None,
                               vInd=ind2)
            i+=2
			
		
        return ret
    
    def OX(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal(aviones=None,
                                   vInd=selec[n-1]) 
            n-=1 # Descarta al ultimo si es impar

        i=0
        k=0
        ind1=None
        ind2=None
        """
        Se intercambian desde [corte1, corte2)
        """
        corte1=0
        corte2=0
        while i<n:
            ind1=IndividuoReal(aviones=None,
                               vInd=selec[i])
            ind2=IndividuoReal(aviones=None,
                               vInd=selec[i+1])

            if random.random()<self.p:
                corte1 = (int) (random.random() * (self.aviones - 2))
                corte2 = corte1 + (int) (random.random() * (self.aviones - corte1))
                set1={""}
                set2={""}
                
                # Se añaden los elementos del padre opuesto
                for j in range(corte1,corte2):                
                    set1.add(ind2.v[j])
                    set2.add(ind1.v[j])
                

                # Hijo 1
                j=corte2
                cont=j
                while j%self.aviones!=corte1:
                    if ind1.v[cont] not in set1:
                        ind1.v[j]=ind1.v[cont]
                        j=(j+1)%self.aviones
                    
                    cont=(cont+1)%self.aviones

                # Hijo 2
                j=corte2
                cont=j
                while j%self.aviones!=corte1:
                    if ind2.v[cont] not in set2:
                        ind2.v[j]=ind2.v[cont]
                        j=(j+1)%self.aviones
                    
                    cont=(cont+1)%self.aviones
                
                
                # Se intercambian la zona del intervalo
                for j in range(corte1,corte2):                
                    temp=ind1.v[j]
                    ind1.v[j]=ind2.v[j]
                    ind2.v[j]=temp
                
                

                

            
            ret[i]=IndividuoReal(aviones=None,
                               vInd=ind1)
            ret[i+1]=IndividuoReal(aviones=None,
                               vInd=ind2)
            i+=2
        
        return ret
    
    # TODO REVISAR
    def OX_PP(self, selec, pp):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal(aviones=None,
                                   vInd=selec[n-1]) 
            n-=1 # Descarta al ultimo si es impar

        i=0
        k=0
        ppi=0
        ind1=None
        ind2=None
        validos=[0 for _ in range(self.aviones-pp)]
        while i<n:
            ind1=IndividuoReal(aviones=None,
                               vInd=selec[i])
            ind2=IndividuoReal(aviones=None,
                               vInd=selec[i+1])

            if random.random()<self.p:    

                puntos={""}                
                puntosList=[0 for _ in range(pp)]
                set1={""}
                set2={""}
                
                # Se eligen "pp" puntos al azar
                punto=0
                for j in range(pp):                
                    punto = int(random.random()*(self.aviones-1))
                    while punto in puntos:
                        punto=int(random.random()*(self.aviones-1))
                    
                    puntos.add(punto)
                    puntosList[j]=punto

                    set1.add(ind2.v[punto])
                    set2.add(ind1.v[punto])
                

                # Hijo 1
                k=0
                for j in range(self.aviones):                
                    if ind1.v[j] not in set1:                    
                        validos[k]=ind1.v[j]
                        k+=1
                    
                ppi=0
                k=0
                for j in range(self.aviones):                
                    if j not in puntos:                    
                        ind1.v[j]=validos[k]
                        k+=1               


                # Hijo 2
                k=0
                for j in range(self.aviones):
                    if ind2.v[j] not in set2:                    
                        validos[k]=ind2.v[j]
                        k+=1
                    
                ppi=0
                k=0
                for j in range(self.aviones):
                    if j not in puntos:                    
                        ind2.v[j]=validos[k]
                        k+=1
                
                for j in range(pp):                    
                    temp=ind1.v[puntosList[j]]
                    ind1.v[puntosList[j]]=ind2.v[puntosList[j]]
                    ind2.v[puntosList[j]]=temp

                
                
                

            
            ret[i]=IndividuoReal(aviones=None,
                               vInd=ind1)
            ret[i+1]=IndividuoReal(aviones=None,
                               vInd=ind2)
            i+=2
        
        return ret
    
    def CX(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal(aviones=None,
                                   vInd=selec[n-1]) 
            n-=1 # Descarta al ultimo si es impar
		
		
		 
        i=0
        ind1=None
        ind2=None
        while i<n:
            ind1=IndividuoReal(aviones=None,
                               vInd=selec[i])
            ind2=IndividuoReal(aviones=None,
                               vInd=selec[i+1])

            if random.random()<self.p:
                pareja1={}
                for j in range(self.aviones):                
                    pareja1[ind1.v[j]]=ind2.v[j]
                
                set={""}

                # Añade al Set los elementos del ciclo
                a=ind1.v[0]
                set.add(a)
                a=pareja1.get(a)
                while a not in set:                
                    set.add(a)
                    a=pareja1.get(a)
                
                # Intercambio de los que no estan en el set
                for j in range(self.aviones):
                    if ind1.v[j] not in set:                    
                        temp=ind1.v[j]
                        ind1.v[j]=ind2.v[j]
                        ind2.v[j]=temp
                
                    
                
                
				
			
            ret[i]=IndividuoReal(aviones=None,
                               vInd=ind1)
            ret[i+1]=IndividuoReal(aviones=None,
                               vInd=ind2)
            i+=2
			
		
        return ret
    
    def CO(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] 

        if n%2==1 :
            ret[n-1]=IndividuoReal(aviones=None,
                                   vInd=selec[n-1]) 
            n-=1 # Descarta al ultimo si es impar
		
		
        i=0
        k=0
        e=0
        ind1=None
        ind2=None
        corte1=0
        while i<n:
            ind1=IndividuoReal(aviones=None,
                               vInd=selec[i])
            ind2=IndividuoReal(aviones=None,
                               vInd=selec[i+1])

            if random.random()<self.p:
                listaDinamica=[i for i in range(0,self.aviones)]

                # Codificacion ind1                
                for j in range(self.aviones):                
                    k=0
                    e=1
                    while (listaDinamica[k]!=ind1.v[j]):
                        if listaDinamica[k]!=-1: e+=1
                        k+=1
                    
                    ind1.v[j]=e
                    listaDinamica[k]=-1
                

                # Codificacion ind2
                listaDinamica=[i for i in range(0,self.aviones)]
                for j in range(self.aviones):                
                    k=0
                    e=1
                    while listaDinamica[k]!=ind2.v[j]:
                        if listaDinamica[k]!=-1: e+=1
                        k+=1
                    
                    ind2.v[j]=e
                    listaDinamica[k]=-1
                

                corte1=int(random.random()*self.aviones)

                for j in range(corte1):                
                    temp=ind1.v[j]
                    ind1.v[j]=ind2.v[j]
                    ind2.v[j]=temp
                

                # Descodificacion ind1
                listaDinamica=[i for i in range(0,self.aviones)]
                for j in range(self.aviones):                
                    k=-1
                    e=0
                    while e<ind1.v[j]:
                        k+=1
                        if listaDinamica[k]!=-1: e+=1
                    
                    ind1.v[j]=listaDinamica[k]
                    listaDinamica[k]=-1
                

                # Descodificacion ind2
                listaDinamica=[i for i in range(0,self.aviones)]
                for j in range(self.aviones):                
                    k=-1
                    e=0
                    while e<ind2.v[j]:
                        k+=1
                        if listaDinamica[k]!=-1: e+=1
                    
                    ind2.v[j]=listaDinamica[k]
                    listaDinamica[k]=-1
                
				
			
            ret[i]=IndividuoReal(aviones=None,
                               vInd=ind1)
            ret[i+1]=IndividuoReal(aviones=None,
                               vInd=ind2)
            i+=2
			
		
        return ret

    
    def intercambioArbol(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] 

        if n%2==1 :
            """ret[n-1]=IndividuoArbol() """
            ret[n-1]= selec[n-1]
            n-=1 # Descarta al ultimo si es impar
               

        i=0
        while i<n:
            """ind1=IndividuoArbol()
            ind2=IndividuoArbol()"""
            ind1=selec[i]
            ind2=selec[i+1]

            if random.random()<self.p:
                if random.random()<0.9:  # Funcional
                    rand1=random.randint(0, len(ind1.funcionales)-1)
                    rand2=random.randint(0, len(ind2.funcionales)-1)

                    hijo1=ind1.funcionales[rand1][0].getHijo(ind1.funcionales[rand1][1])
                    hijo2=ind2.funcionales[rand2][0].getHijo(ind2.funcionales[rand2][1])

                    ind1.funcionales[rand1][0].setHijo(ind1.funcionales[rand1][1], hijo2)
                    ind2.funcionales[rand2][0].setHijo(ind2.funcionales[rand2][1], hijo1)

                    ind1.gen.raiz=ind1.funcionales[0][0].getHijo(0)
                    ind2.gen.raiz=ind2.funcionales[0][0].getHijo(0)
                else:  # Terminal
                    rand1=random.randint(0, len(ind1.terminales)-1)
                    rand2=random.randint(0, len(ind2.terminales)-1)

                    hijo1=ind1.terminales[rand1][0].getHijo(ind1.terminales[rand1][1])
                    hijo2=ind2.terminales[rand2][0].getHijo(ind2.terminales[rand2][1])

                    ind1.terminales[rand1][0].setHijo(ind1.terminales[rand1][1], hijo2)
                    ind2.terminales[rand2][0].setHijo(ind2.terminales[rand2][1], hijo1)

            # Reinicia los punteros para añadirlos a la poblacion
            ind1.reiniciaListas(ind1.gen.raiz)
            ind2.reiniciaListas(ind2.gen.raiz)

            ret[i]=ind1
            ret[i+1]=ind2
            i+=2
            

        return ret

# -----------------------------------------------------------------------------------------------
# --- MUTACION ----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------


class Mutacion:
    def __init__(self, p, aviones, tam_elite, heur, filas,columnas, funcion):
        self.p=p
        self.aviones=aviones
        self.tam_elite=tam_elite
        
        # Reales (Aviones)
        self.permutaciones=[]
        self.heur=heur
        self.dfs(heur,0,[],[0 for i in range(heur)])
        #print(self.permutaciones)
        
        # Arboles
        self.filas=filas
        self.columnas=columnas
        
        self.funcion=funcion
    

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
    

    def inversion(self, poblacion):
        tam_poblacion=len(poblacion)
        ret=[] # = new Individuo[tam_poblacion];
		
		
        act=None
        for i in range(tam_poblacion):                                
            act=IndividuoReal(aviones=None,
                              vInd=poblacion[i]);	
            			
            if random.random()<self.p:
                corte1=int(random.random()*(len(act.v)-2))
                corte2=corte1+int(random.random()*(len(act.v)-corte1))
                separacion=(corte2-corte1+1)
                for k in range(separacion//2):
                    temp=act.v[corte1+k]
                    act.v[corte1+k]=act.v[corte2-k]
                    act.v[corte2-k]=temp
			
            ret.append(IndividuoReal(aviones=None,
                                     vInd=act))
		
        return ret


    def intercambio(self, poblacion):
        tam_poblacion=len(poblacion)
        ret=[] # = new Individuo[tam_poblacion];
		
		
        act=None
        for i in range(tam_poblacion):                                
            act=IndividuoReal(aviones=None,
                              vInd=poblacion[i]);	
            			
            if random.random()<self.p:
                punto1=int(random.random()*(len(act.v)-2))
                punto2=punto1+int(random.random()*(len(act.v)-1-punto1))
                
                temp=act.v[punto1]
                act.v[punto1]=act.v[punto2]
                act.v[punto2]=temp
                
			
            ret.append(IndividuoReal(aviones=None,
                                     vInd=act))
		
        return ret
    

    def insercion(self, poblacion):
        tam_poblacion=len(poblacion)
        ret=[] # = new Individuo[tam_poblacion];
		
        
        act=None
        for i in range(tam_poblacion):                                
            act=IndividuoReal(aviones=None,
                              vInd=poblacion[i].v);	
            
            if random.random()<self.p:
                antiguaPosicion=int(random.random()*(len(act.v)-1))
                nuevaPosicion=antiguaPosicion
                while nuevaPosicion==antiguaPosicion:
                    nuevaPosicion = int(random.random()*(len(act.v)-1))

                    
				
                if nuevaPosicion>antiguaPosicion:
                    tmp=act.v[antiguaPosicion]
                    for k in range(antiguaPosicion,nuevaPosicion):
                        act.v[k]=act.v[k+1]
					
                    act.v[nuevaPosicion]=tmp				
                else:
                    tmp=act.v[antiguaPosicion]
                    #for (int k = antiguaPosicion; k > nuevaPosicion ; k--) {
                    for k in range(antiguaPosicion, nuevaPosicion,-1):					
                        act.v[k]=act.v[k-1]
					
                    act.v[nuevaPosicion]=tmp
					
			
            ret.append(IndividuoReal(aviones=None,
                                     vInd=act))
		
        return ret
    
    # TODO
    def heuristica(self, poblacion):
        tam_poblacion=len(poblacion)
        ret=[] # = new Individuo[tam_poblacion];
		
        rand=0
		
        cont=0
		
        elegidos_indx=[0 for _ in range(self.heur)]
        elegidos_vals=[0 for _ in range(self.heur)]	
		
        set_elegidos={""}
		
        mejor_fit=float("inf")
        mejor=[0 for _ in range(self.aviones)]
        tmp=[0 for _ in range(self.aviones)]
        

        act=None
        for i in range(tam_poblacion):                                
            act=IndividuoReal(aviones=None,
                              vInd=poblacion[i]);	
            
            if random.random()<self.p:
                cont=0
                set_elegidos.clear()
                mejor_fit=float("inf")

                while cont<self.heur:
                    numero = random.randint(0,self.aviones-1)
                    if numero not in set_elegidos:
                        set_elegidos.add(numero)
                        elegidos_indx[cont]=numero
                        elegidos_vals[cont]=act.v[numero]
                        cont+=1
                    

                cont=0
                tmp=act.v
                # Recorre las permutaciones
                for l in self.permutaciones:                
                    # Cambia los valores
                    for x in l: 
                        tmp[elegidos_indx[x]]=elegidos_vals[x]
                    
                    
                    fit=self.funcion.fitness(tmp);		
                    cont+=1
                    if fit<mejor_fit:
                        mejor_fit=fit
                        mejor=tmp
                
                

                ret.append(IndividuoReal(aviones=None,
                                        vInd=mejor))
            else: 
                ret.append(IndividuoReal(aviones=None,
                                        vInd=act))
            
					
			
            
		
        return ret  
        
    def dfs(self, n, k, act, visitados):
        if k==n:
            aux=[]            
            for x in act:
                aux.append(x)
            
            self.permutaciones.append(aux)
            return

        for i in range(n):            
            if visitados[i]==1: continue
            
            visitados[i]=1
            act.append(i)
            self.dfs(n,k+1,act,visitados)
            act.pop(len(act)-1)
            visitados[i]=0
  

    def terminal(self, poblacion):   
        """
        poblacion: IndividuoArbol[]
        
        (return IndividuoArbol[])
        """     

        tam_poblacion = len(poblacion)
        ret=[None for _ in range(tam_poblacion)]        
        
        
        for i in range(tam_poblacion):
            act=poblacion[i]
            if random.random()<self.p:
                rand=random.randint(0, 3)
                if rand==0: new_terminal=Avanza()
                elif rand==1: 
                    new_terminal=Constante(self.filas, self.columnas,constante=None)
                else: new_terminal=Izquierda()                
                    
                tmp=random.randint(0,len(act.terminales)-1)
                act.terminales[tmp][0].setHijo(act.terminales[tmp][1], new_terminal)
            
            ret[i]=act
        
        return ret

    def funcional(self, poblacion):
        """
        poblacion: IndividuoArbol[]
        
        (return IndividuoArbol[])
        """     

        tam_poblacion = len(poblacion)
        ret=[None for _ in range(tam_poblacion)]    

        act=None
        for i in range(tam_poblacion):
            act=poblacion[i]
            if random.random()<self.p:
                tmp=random.randint(0, len(act.funcionales)-1)
                funcional=act.funcionales[tmp][0].getHijo(act.funcionales[tmp][1])

                newFuncional=None
                if funcional.getOperacion()=="Suma": newFuncional = Progn()
                elif funcional.getOperacion()=="Progn": newFuncional = Suma()

                if newFuncional is not None:
                    newFuncional.setHijo(0, funcional.getHijo(0))
                    newFuncional.setHijo(1, funcional.getHijo(1))
                    act.funcionales[tmp][0].setHijo(act.funcionales[tmp][1], newFuncional)
                    act.gen.raiz=act.funcionales[0][0].getHijo(0)

            ret[i]=act

        return ret


    def arbol(self, poblacion):
        """
        poblacion: IndividuoArbol[]
        
        (return IndividuoArbol[])
        """ 
        tam_poblacion = len(poblacion)
        ret=[None for _ in range(tam_poblacion)]

        for i in range(tam_poblacion):
            act = poblacion[i]
            if random.random()<self.p:
                tmp=random.randint(0, len(act.funcionales) - 1)
                newArbol=Arbol(random.randint(0, 1), random.randint(2, 3), self.filas, self.columnas)  
                act.funcionales[tmp][0].setHijo(act.funcionales[tmp][1], newArbol.raiz)
                act.gen.raiz=act.funcionales[0][0].getHijo(0)

            ret[i] = act

        return ret
    
    def permutacion(self, poblacion):
        """
        poblacion: IndividuoArbol[]
        
        (return IndividuoArbol[])
        """ 
        tam_poblacion=len(poblacion)
        ret=[None for _ in range(tam_poblacion)]
        
        for i in range(tam_poblacion):
            act=poblacion[i]
            if random.random()<self.p:
                tmp=random.randint(0, len(act.funcionales)-1)
                funcional=act.funcionales[tmp][0].getHijo(act.funcionales[tmp][1])
                if funcional.getOperacion()=="Progn" or funcional.getOperacion()=="Suma":
                    temp=funcional.getHijo(0)
                    funcional.setHijo(0, funcional.getHijo(1))
                    funcional.setHijo(1, temp)

            ret[i] = act

        return ret

    def hoist(self, poblacion):
        """
        poblacion: IndividuoArbol[]
        
        (return IndividuoArbol[])
        """ 
        tam_poblacion = len(poblacion)
        ret=[None for _ in range(tam_poblacion)]

        for i in range(tam_poblacion):
            act=poblacion[i]
            if random.random()<self.p:
                tmp=random.randint(0, len(act.funcionales)-1)
                act.gen.raiz=act.funcionales[tmp][0].getHijo(act.funcionales[tmp][1])

            ret[i] = act

        return ret

    def contraccion(self, poblacion):
        """
        poblacion: IndividuoArbol[]
        
        (return IndividuoArbol[])
        """ 
        tam_poblacion=len(poblacion)
        ret=[None for _ in range(tam_poblacion)]

        for i in range(tam_poblacion):
            act=poblacion[i]
            if random.random()<self.p:
                rand=random.randint(0, 2)
                if rand==0: newExp=Avanza()
                elif rand==1: newExp=Constante(self.filas, self.columnas,constante=None)
                else: newExp=Izquierda()

                tmp=random.randint(0, len(act.funcionales)-1)
                act.funcionales[tmp][0].setHijo(act.funcionales[tmp][1], newExp)

            ret[i] = act

        return ret

    def expansion(self, poblacion):
        """
        poblacion: IndividuoArbol[]
        
        (return IndividuoArbol[])
        """ 
        tam_poblacion = len(poblacion)
        ret=[None for _ in range(tam_poblacion)]

        for i in range(tam_poblacion):
            act = poblacion[i]
            if random.random()<self.p:
                tmp=random.randint(0, len(act.terminales)-1)
                newArbol=Arbol(random.randint(0, 1), random.randint(2, 3), self.filas, self.columnas)
                act.terminales[tmp][0].setHijo(act.terminales[tmp][1], newArbol.raiz)
                act.gen.raiz=act.funcionales[0][0].getHijo(0)

            ret[i] = act

        return ret
      

# -----------------------------------------------------------------------------------------------
# --- ALGORITMO GENETICO ------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------

# value=1 Max, cualquier otro valor => Min
class PQ(queue.PriorityQueue):
    def __init__(self, value):
        super().__init__()
        self.value=1
        if value==1: self.value=-1

    def push(self, id, fit):
        super().put((self.value*fit, id))

    def top_fit(self):
        fit, _ = self.queue[0]  
        return self.value*fit
    
    def top_id(self):
        _, id = self.queue[0]  
        return id
    
    def pop(self):
        _, id = super().get()
        return id
    
    def size(self):
        return self.qsize()

class AlgoritmoGenetico():
    def __init__(self,MW):
        self.MW=MW                  # Class: MainWindow
        
        
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

        self.elitQ=None   

        # AEROPUERTO
        self.aviones=0
        self.pistas=0
        self.vuelos_id=[]
        self.TEL=[] # 2D array
        self.tipo_avion=[]


        self.progreso_generaciones=[[] for _ in range(4)]

    # Funcion que inicializa las variables a los valores seleccionados en la interfaz
    def set_valores(self,tam_poblacion, generaciones, seleccion_idx, cruce_idx, prob_cruce, mutacion_idx,
                    prob_mut, precision, funcion_idx, num_genes, elitismo,
                    modo, profundidad, long_cromosoma, filas, columnas, bloating_idx,ticks):
        
        self.poblacion=[]
        self.tam_poblacion=tam_poblacion    
        self.generaciones=generaciones      
        self.prob_cruce=prob_cruce        
        self.prob_mut=prob_mut    

        self.num_genes=num_genes # 2
        
        self.elitismo=elitismo  
        self.tam_elite=int((tam_poblacion*(elitismo/100.0)))  

        self.aviones=0

        self.funcion_idx=funcion_idx

        self.ini_idx=modo
        self.profundidad=profundidad
        self.long_cromosoma=long_cromosoma
        self.filas=filas
        self.columnas=columnas
        self.bloating_idx=bloating_idx
        self.ticks=ticks


        if funcion_idx==0: self.funcion=Funcion1()
        elif funcion_idx==1: self.funcion=Funcion2()
        elif funcion_idx==2: self.funcion=Funcion3()
        elif funcion_idx==3: self.funcion=Funcion4(self.num_genes)
        elif funcion_idx<7:            
            self.lee_archivos()
        elif funcion_idx>=7: self.funcion=FuncionArbol(self.filas, self.columnas, self.ticks, obstaculos=False)
        #else: self.funcion=None # TODO GRAMATICA
        
        self.seleccion_idx=seleccion_idx
        self.seleccion=Seleccion(tam_poblacion, self.funcion.opt)
        
        self.cruce_idx=cruce_idx
        self.cruce=Cruce(prob_cruce,self.tam_elite, self.aviones)    
        
        self.mutacion_idx=mutacion_idx        
        self.mutacion=Mutacion(prob_mut, 
                               self.aviones, 
                               self.tam_elite, 3, 
                               self.filas, self.columnas, 
                               self.funcion)

        if funcion_idx!=-1: self.elitQ=PQ(0) # 
        else: self.elitQ=PQ(1) # Cola prioritaria de maximos para almacenar los menores y asi comparar rapidamente
        self.selec_elite=[]

        if funcion_idx<4: self.tam_genes=self.tamGenes(precision)
        
        self.mejor_total=float('+inf')
        if self.funcion_idx<4:
            if self.funcion.opt==True: self.mejor_total=float('-inf')
            else: self.mejor_total=float('+inf')
        elif self.funcion_idx>6:            
            self.mejor_total=float('-inf')
        

    def lee_archivos(self):
        vuelos_txt="data/"
        TEL_txt="data/"

        # LEE DE LOS TXT
        if self.funcion_idx==4:
            self.aviones=12
            self.pistas=3
            vuelos_txt+="vuelos1.txt"
            TEL_txt+="TEL1.txt"
        elif self.funcion_idx==5:
            self.aviones=25
            self.pistas=5
            vuelos_txt+="vuelos2.txt"
            TEL_txt+="TEL2.txt"
        elif self.funcion_idx==6:
            self.aviones=100
            self.pistas=10
            vuelos_txt+="vuelos3.txt"
            TEL_txt+="TEL3.txt"
        
        i=0
        self.vuelos_id=[None for _ in range(self.aviones)]
        self.tipo_avion = [0 for _ in range(self.aviones)]
        self.TEL = [[0 for _ in range(self.aviones)] for _ in range(self.pistas)]
        
        try:
            # Open the file
            with open(vuelos_txt, 'r') as vuelos_reader, open(TEL_txt, 'r') as TEL_reader:
                for line in vuelos_reader:
                    tokens=line.split()
                    self.vuelos_id[i]=tokens[0]
                    if tokens[1]=="W": self.tipo_avion[i]=0
                    elif tokens[1]=="G": self.tipo_avion[i]=1
                    else: self.tipo_avion[i]=2
                    
                    i+=1

                i=0
                for line in TEL_reader:
                    tokens=line.split("\t")
                    j=0
                    for t in tokens:
                        self.TEL[i][j]=int(t)
                        j+=1
                    
                    i+=1
        except IOError as e:
            print("Error al leer archivos:", e)
        
        self.funcion = FuncionA(self.aviones, self.pistas, self.tipo_avion, self.TEL)    
        
        

    def tamGenes(self, precision):   
        ret = []
        for i in range(self.num_genes):
            ret.append(self.tamGen(precision, self.funcion.xMin[i], self.funcion.xMax[i]))
        return ret

    def tamGen(self, precision, min, max):
        return math.ceil((math.log10(((max-min)/precision)+1)/math.log10(2)))

    def ejecuta(self):
        if self.funcion_idx<4: return self.ejecutaBin()
        elif self.funcion_idx<7: return self.ejecutaReal()
        elif self.funcion_idx==7: return self.ejecutaArbol()
        else: return self.ejecutaGramatica()

    def ejecutaBin(self):
        selec=[]

        self.init_poblacion()    
        self.evaluacion_poblacionBin()                
        
        while self.generaciones > 0:
            selec=self.seleccion_poblacionBin(5)
            
            self.poblacion=self.cruce_poblacionBin(selec)
            self.poblacion=self.mutacion_poblacionBin(self.poblacion)

            for i in range(self.tam_elite):                
                self.poblacion.append(self.selec_elite[i])
            
            self.evaluacion_poblacionBin()            
            
            self.generaciones-=1
		
        #GUI(self.progreso_generaciones[0],self.progreso_generaciones[1],self.progreso_generaciones[2])

        return self.mejor_total

    def ejecutaReal(self):
        selec=[]

        self.init_poblacion()    
        self.evaluacion_poblacionReal()                
        
        while self.generaciones > 0:
            selec=self.seleccion_poblacionReal(5)
            
            self.poblacion=self.cruce_poblacionReal(selec)
            self.poblacion=self.mutacion_poblacionReal(self.poblacion)

            for i in range(self.tam_elite):
                self.poblacion.append(self.selec_elite[i])
            
            self.evaluacion_poblacionReal()            
            
            self.generaciones-=1
		
        #GUI(self.progreso_generaciones[0],self.progreso_generaciones[1],self.progreso_generaciones[2])

        return self.mejor_total

    def ejecutaArbol(self):
        selec=[]

        self.init_poblacionArbol(0)            
        self.evaluacion_poblacionArbol()                
        
        while self.generaciones > 0:
            selec=self.seleccion_poblacionArbol(5)           
            
            self.poblacion=self.cruce_poblacionArbol(selec)              
            self.poblacion=self.mutacion_poblacionArbol(self.poblacion)  

            for i in range(self.tam_elite):                
                self.poblacion.append(self.selec_elite[i])
            
            self.evaluacion_poblacionArbol()    
                   
            
            self.generaciones-=1
		
        #GUI(self.progreso_generaciones[0],self.progreso_generaciones[1],self.progreso_generaciones[2])

        return self.mejor_total
    
    def ejecutaGramatica(self):
        selec=[]
        
        self.init_poblacionGramatica(0)       
        for x in self.poblacion:
            print(x)     
        self.evaluacion_poblacionGramatica()                
        
        while self.generaciones > 0:
            selec=self.seleccion_poblacionGramatica(5)           
            
            self.poblacion=self.cruce_poblacionGramatica(selec, self.long_cromosoma)              
            self.poblacion=self.mutacion_poblacionGramatica(self.poblacion)  

            for i in range(self.tam_elite):                
                self.poblacion.append(self.selec_elite[i])
            
            self.evaluacion_poblacionGramatica()    
                   
            
            self.generaciones-=1
		
        #GUI(self.progreso_generaciones[0],self.progreso_generaciones[1],self.progreso_generaciones[2])

        return self.mejor_total


    def init_poblacion(self):
        if self.funcion_idx<4:             
            self.poblacion=[Individuo(self.num_genes, self.tam_genes, self.funcion.xMax, self.funcion.xMin, 
                                                ind=None) for _ in range(self.tam_poblacion)]
        else: 
            self.poblacion=[IndividuoReal(aviones=self.aviones,vInd=None) for _ in range(self.tam_poblacion)]

    def init_poblacionArbol(self, x):
        self.poblacion=[]

        if self.ini_idx==2:  # RAMPED & HALF
            D=self.profundidad-1
            tam=(self.tam_poblacion-x)//D
            mod=(self.tam_poblacion-x)%D
            mod2=tam % 2

            if mod!=0:
                mod2=(tam+1)%2
                for d in range(self.profundidad, self.profundidad - mod, -1):
                    for i in range((tam+1)//2):
                        self.poblacion.append(IndividuoArbol(0, d, self.filas, self.columnas, ind=None))
                        self.poblacion.append(IndividuoArbol(1, d, self.filas, self.columnas, ind=None))
                    if mod2==1:
                        self.poblacion.append(IndividuoArbol(1, d, self.filas, self.columnas, ind=None))
                mod2=tam%2
                for d in range(self.profundidad-mod,1,-1):
                    for i in range(tam//2):
                        self.poblacion.append(IndividuoArbol(0, d, self.filas, self.columnas, ind=None))
                        self.poblacion.append(IndividuoArbol(1, d, self.filas, self.columnas, ind=None))
                    if mod2==1:
                        self.poblacion.append(IndividuoArbol(1, d, self.filas, self.columnas, ind=None))
            else:
                for d in range(2,self.profundidad+1):
                    for i in range(tam//2):
                        self.poblacion.append(IndividuoArbol(0, d, self.filas, self.columnas, ind=None))
                        self.poblacion.append(IndividuoArbol(1, d, self.filas, self.columnas, ind=None))
                    if mod2==1:
                        self.poblacion.append(IndividuoArbol(1, d, self.filas, self.columnas, ind=None))

        else:  # COMPLETO o CRECIENTE
            for i in range(self.tam_poblacion-x):
                self.poblacion.append(IndividuoArbol(self.ini_idx,self.profundidad, 
                                                     self.filas, self.columnas,ind=None))

        if x!=0:
            while len(self.elitQ)!=0:
                self.poblacion.append(IndividuoArbol(self.ini_idx,self.profundidad, 
                                                     self.filas, self.columnas, 
                                                     self.elitQ.pop().getId()))
    
    def init_poblacionGramatica(self, x):
        self.poblacion=[]

        for i in range(self.tam_poblacion-x):
            self.poblacion.append(IndividuoGramatica(self.long_cromosoma, self.filas, self.columnas,
                                    cromosoma=None, ind=None))

        if x != 0:
            while len(self.elitQ) != 0:
                self.poblacion.append(IndividuoGramatica(tam_cromosoma=None, filas=None, columnas=None,
                    cromosoma=None,ind=self.elitQ.pop().getId()))




    def evaluacion_poblacionBin(self):                
        self.fitness_total=0
        self.prob_seleccion=[0 for _ in range(self.tam_poblacion)]
        self.prob_seleccionAcum=[0 for _ in range(self.tam_poblacion)]
        if self.funcion.opt==True: 
            mejor_generacion = float('-inf')
            peor_generacion = float('+inf')
        else: 
            mejor_generacion = float('+inf')
            peor_generacion = float('-inf')


        
        for i in range(self.tam_poblacion):            
            self.poblacion[i].calcular_fenotipo()
			
		
        fit=0.0
        indexMG=0        
        for i in range(self.tam_poblacion):
            fit=self.funcion.fitness(self.poblacion[i].fenotipo)
            self.poblacion[i].fitness=fit
            self.fitness_total+=fit

            if self.elitQ.size()<self.tam_elite: self.elitQ.push(i, fit)
            elif(self.tam_elite!=0 and self.funcion.cmpBool(fit, self.elitQ.top_fit())):
                self.elitQ.pop()
                self.elitQ.push(i, fit)
			
            

            #if fit>mejor_generacion: mejor_generacion=fit
            if(self.funcion.cmpBool(fit, mejor_generacion)) :
                mejor_generacion=fit;	                
                indexMG=i
            peor_generacion=self.funcion.cmpPeor(peor_generacion, fit)
			
        self.selec_elite=[]
        for _ in range(self.tam_elite):
            self.selec_elite.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                        ind=self.poblacion[self.elitQ.pop()]))
            

        #if mejor_generacion>self.mejor_total: self.mejor_total=mejor_generacion
        if(self.funcion.cmpBool(mejor_generacion, self.mejor_total)):
            self.mejor_total=mejor_generacion;	
            self.mejor_ind=self.poblacion[indexMG]
		


        self.progreso_generaciones[0].append(self.mejor_total)
        self.progreso_generaciones[1].append(mejor_generacion)
        self.progreso_generaciones[2].append((self.fitness_total/self.tam_poblacion))
        
        
        

        acum=0.0
        if peor_generacion<0: peor_generacion*=-1

        if self.funcion.opt==False:
            self.fitness_total=self.tam_poblacion*1.05*peor_generacion-self.fitness_total
            for i in range(self.tam_poblacion):
                self.prob_seleccion[i]=1.05*peor_generacion-self.poblacion[i].fitness
                self.prob_seleccion[i]/=self.fitness_total
                acum += self.prob_seleccion[i]
                self.prob_seleccionAcum[i]=acum			
        else:
            self.fitness_total = self.tam_poblacion*1.05*peor_generacion+self.fitness_total
            for i in range(self.tam_poblacion):
                self.prob_seleccion[i]=1.05*peor_generacion+self.poblacion[i].fitness
                self.prob_seleccion[i]/=self.fitness_total
                acum+=self.prob_seleccion[i]
                self.prob_seleccionAcum[i]=acum
        
        # Whitley recomienda valores próximos a 1.5
            # Valores mayores ocasionarían superindividuos
            # Valores menores frenarían la búsqueda sin ningún beneficio
        self.progreso_generaciones[3].append(self.tam_poblacion*self.prob_seleccion[indexMG])

    def evaluacion_poblacionReal(self):        
        self.fitness_total=0
        self.prob_seleccion=[0 for _ in range(self.tam_poblacion)]
        self.prob_seleccionAcum=[0 for _ in range(self.tam_poblacion)]

        
        mejor_generacion=float('+inf')
        peor_generacion=float('-inf')

		
        fit=0.0
        indexMG=0        
        for i in range(self.tam_poblacion):
            fit=self.funcion.fitness(self.poblacion[i].v)
            self.poblacion[i].fitness=fit
            self.fitness_total+=fit

            if self.elitQ.size()<self.tam_elite: self.elitQ.push(i, fit)
            elif(self.tam_elite!=0 and self.funcion.cmpBool(fit, self.elitQ.top_fit())):
                self.elitQ.pop()
                self.elitQ.push(i, fit)
			
            

            #if fit>mejor_generacion: mejor_generacion=fit
            if(self.funcion.cmpBool(fit, mejor_generacion)) :
                mejor_generacion=fit;	                
                indexMG=i
            peor_generacion=self.funcion.cmpPeor(peor_generacion, fit)
			
        self.selec_elite=[]
        for _ in range(self.tam_elite):
            self.selec_elite.append(IndividuoReal(aviones=None,
                                                  vInd=self.poblacion[self.elitQ.pop()].v))
            

        #if mejor_generacion>self.mejor_total: self.mejor_total=mejor_generacion
        if(self.funcion.cmpBool(mejor_generacion, self.mejor_total)):
            self.mejor_total=mejor_generacion;	
            self.mejor_ind=self.poblacion[indexMG]
		


        self.progreso_generaciones[0].append(self.mejor_total)
        self.progreso_generaciones[1].append(mejor_generacion)
        self.progreso_generaciones[2].append((self.fitness_total/self.tam_poblacion))
        
        
        
        acum=0.0
        if peor_generacion<0: peor_generacion*=-1

        self.fitness_total=self.tam_poblacion*1.05*peor_generacion-self.fitness_total
        for i in range(self.tam_poblacion):
            self.prob_seleccion[i]=1.05*peor_generacion-self.poblacion[i].fitness
            self.prob_seleccion[i]/=self.fitness_total
            acum += self.prob_seleccion[i]
            self.prob_seleccionAcum[i]=acum	
        
        # Whitley recomienda valores próximos a 1.5
            # Valores mayores ocasionarían superindividuos
            # Valores menores frenarían la búsqueda sin ningún beneficio
        self.progreso_generaciones[3].append(self.tam_poblacion*self.prob_seleccion[indexMG])
    
    def evaluacion_poblacionArbol(self):        
        self.fitness_total=0
        self.prob_seleccion=[0 for _ in range(self.tam_poblacion)]
        self.prob_seleccionAcum=[0 for _ in range(self.tam_poblacion)]

        
        mejor_generacion=float('-inf')
        peor_generacion=float('+inf')

		
        fit=0.0
        indexMG=0        
        for i in range(self.tam_poblacion):
            fit=self.funcion.fitness(self.poblacion[i])
            self.poblacion[i].fitness=fit
            self.fitness_total+=fit

            if self.elitQ.size()<self.tam_elite: self.elitQ.push(i, fit)
            elif(self.tam_elite!=0 and self.funcion.cmpBool(fit, self.elitQ.top_fit())):
                self.elitQ.pop()
                self.elitQ.push(i, fit)
			
            

            #if fit>mejor_generacion: mejor_generacion=fit
            if(self.funcion.cmpBool(fit, mejor_generacion)) :
                mejor_generacion=fit;	                
                indexMG=i
            peor_generacion=self.funcion.cmpPeor(peor_generacion, fit)
			
        self.selec_elite=[]
        for _ in range(self.tam_elite):            
            self.selec_elite.append(IndividuoArbol(modo=None, profundidad=None, filas=None, columnas=None, 
                                                  ind=self.poblacion[self.elitQ.pop()]))
            

        #if mejor_generacion>self.mejor_total: self.mejor_total=mejor_generacion
        if(self.funcion.cmpBool(mejor_generacion, self.mejor_total)):
            self.mejor_total=mejor_generacion;	
            self.mejor_ind=self.poblacion[indexMG]
		


        self.progreso_generaciones[0].append(self.mejor_total)
        self.progreso_generaciones[1].append(mejor_generacion)
        self.progreso_generaciones[2].append((self.fitness_total/self.tam_poblacion))
        
        
        
        acum=0.0
        if peor_generacion<0: peor_generacion*=-1

        self.fitness_total=self.tam_poblacion*1.05*peor_generacion-self.fitness_total
        for i in range(self.tam_poblacion):
            self.prob_seleccion[i]=1.05*peor_generacion-self.poblacion[i].fitness
            self.prob_seleccion[i]/=self.fitness_total
            acum += self.prob_seleccion[i]
            self.prob_seleccionAcum[i]=acum	
        
        # Whitley recomienda valores próximos a 1.5
            # Valores mayores ocasionarían superindividuos
            # Valores menores frenarían la búsqueda sin ningún beneficio
        self.progreso_generaciones[3].append(self.tam_poblacion*self.prob_seleccion[indexMG])

    def evaluacion_poblacionGramatica(self):        
        self.fitness_total=0
        self.prob_seleccion=[0 for _ in range(self.tam_poblacion)]
        self.prob_seleccionAcum=[0 for _ in range(self.tam_poblacion)]

        
        mejor_generacion=float('-inf')
        peor_generacion=float('+inf')

		
        fit=0.0
        indexMG=0        
        for i in range(self.tam_poblacion):
            fit=self.funcion.fitness(self.poblacion[i])
            self.poblacion[i].fitness=fit
            self.fitness_total+=fit

            if self.elitQ.size()<self.tam_elite: self.elitQ.push(i, fit)
            elif(self.tam_elite!=0 and self.funcion.cmpBool(fit, self.elitQ.top_fit())):
                self.elitQ.pop()
                self.elitQ.push(i, fit)
			
            

            #if fit>mejor_generacion: mejor_generacion=fit
            if(self.funcion.cmpBool(fit, mejor_generacion)) :
                mejor_generacion=fit;	                
                indexMG=i
            peor_generacion=self.funcion.cmpPeor(peor_generacion, fit)
			
        self.selec_elite=[]
        for _ in range(self.tam_elite):            
            self.selec_elite.append(IndividuoArbol(modo=None, profundidad=None, filas=None, columnas=None, 
                                                  ind=self.poblacion[self.elitQ.pop()]))
            

        #if mejor_generacion>self.mejor_total: self.mejor_total=mejor_generacion
        if(self.funcion.cmpBool(mejor_generacion, self.mejor_total)):
            self.mejor_total=mejor_generacion;	
            self.mejor_ind=self.poblacion[indexMG]
		


        self.progreso_generaciones[0].append(self.mejor_total)
        self.progreso_generaciones[1].append(mejor_generacion)
        self.progreso_generaciones[2].append((self.fitness_total/self.tam_poblacion))
        
        
        
        acum=0.0
        if peor_generacion<0: peor_generacion*=-1

        self.fitness_total=self.tam_poblacion*1.05*peor_generacion-self.fitness_total
        for i in range(self.tam_poblacion):
            self.prob_seleccion[i]=1.05*peor_generacion-self.poblacion[i].fitness
            self.prob_seleccion[i]/=self.fitness_total
            acum += self.prob_seleccion[i]
            self.prob_seleccionAcum[i]=acum	
        
        # Whitley recomienda valores próximos a 1.5
            # Valores mayores ocasionarían superindividuos
            # Valores menores frenarían la búsqueda sin ningún beneficio
        self.progreso_generaciones[3].append(self.tam_poblacion*self.prob_seleccion[indexMG])



    def seleccion_poblacionBin(self, k):         
        ret=[]
        
        if self.seleccion_idx==0: 
            ret=self.seleccion.ruletaBin(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==1: 
            ret=self.seleccion.torneoDeterministicoBin(self.poblacion, k, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==2: 
            ret=self.seleccion.torneoProbabilisticoBin(self.poblacion, k, 0.9, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==3: 
            ret=self.seleccion.estocasticoUniversalBin(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==4: 
            ret=self.seleccion.truncamientoBin(self.poblacion, self.prob_seleccion, 0.5, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==5: 
            ret=self.seleccion.restosBin(self.poblacion, self.prob_seleccion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        else: 
            ret=self.seleccion.rankingBin(self.poblacion, self.prob_seleccion, 2, self.tam_poblacion-self.tam_elite)
        return ret

    def seleccion_poblacionReal(self, k):         
        ret=[]
        
        if self.seleccion_idx==0: 
            ret=self.seleccion.ruletaReal(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==1: 
            ret=self.seleccion.torneoDeterministicoReal(self.poblacion, k, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==2: 
            ret=self.seleccion.torneoProbabilisticoReal(self.poblacion, k, 0.9, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==3: 
            ret=self.seleccion.estocasticoUniversalReal(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==4: 
            ret=self.seleccion.truncamientoReal(self.poblacion, self.prob_seleccion, 0.5, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==5: 
            ret=self.seleccion.restosReal(self.poblacion, self.prob_seleccion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        else: 
            ret=self.seleccion.rankingReal(self.poblacion, self.prob_seleccion, 2, self.tam_poblacion-self.tam_elite)
        return ret
    
    def seleccion_poblacionArbol(self, k):         
        ret=[]
        
        if self.seleccion_idx==0: 
            ret=self.seleccion.ruletaArbol(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==1: 
            ret=self.seleccion.torneoDeterministicoArbol(self.poblacion, k, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==2: 
            ret=self.seleccion.torneoProbabilisticoArbol(self.poblacion, k, 0.9, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==3: 
            ret=self.seleccion.estocasticoUniversalArbol(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==4: 
            ret=self.seleccion.truncamientoArbol(self.poblacion, self.prob_seleccion, 0.5, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==5: 
            ret=self.seleccion.restosArbol(self.poblacion, self.prob_seleccion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        else: 
            ret=self.seleccion.rankingArbol(self.poblacion, self.prob_seleccion, 2, self.tam_poblacion-self.tam_elite)
        return ret
    
    def seleccion_poblacionGramatica(self, k):         
        ret=[]
        
        if self.seleccion_idx==0: 
            ret=self.seleccion.ruletaGramatica(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==1: 
            ret=self.seleccion.torneoDeterministicoGramatica(self.poblacion, k, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==2: 
            ret=self.seleccion.torneoProbabilisticoGramatica(self.poblacion, k, 0.9, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==3: 
            ret=self.seleccion.estocasticoUniversalGramatica(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==4: 
            ret=self.seleccion.truncamientoGramatica(self.poblacion, self.prob_seleccion, 0.5, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==5: 
            ret=self.seleccion.restosGramatica(self.poblacion, self.prob_seleccion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        else: 
            ret=self.seleccion.rankingGramatica(self.poblacion, self.prob_seleccion, 2, self.tam_poblacion-self.tam_elite)
        return ret

      
    def cruce_poblacionBin(self, selec):
        ret=[]
        if self.cruce_idx==0: return self.cruce.cruce_monopuntoBin(selec)
        elif self.cruce_idx==1: return self.cruce.cruce_uniformeBin(selec)
        else:
            print("Cruce Binario, Solo hay cruce Mono-Punto y Uniforme")
            exit(1)
    
    # TODO
    def cruce_poblacionReal(self, selec):
        ret=[]
        
        if self.cruce_idx==2: return self.cruce.PMX(selec) # PMX
        elif self.cruce_idx==3: return self.cruce.OX(selec) # OX
        elif self.cruce_idx==4: return self.cruce.OX_PP(selec,3)
        elif self.cruce_idx==5: return self.cruce.CX(selec)
        elif self.cruce_idx==6: return self.cruce.CO(selec)      
        else:
            print("Cruce Real, No tiene cruce Mono-Punto o Uniforme o Intercambio")
            exit(1)

    def cruce_poblacionArbol(self, selec):
        ret=[]
        
        if self.cruce_idx==7: return self.cruce.intercambioArbol(selec) # PMX     
        else:
            print("Cruce Arbol, Solo tiene intercambio (7)")
            exit(1)

    def cruce_poblacionGramatica(self, selec, d):
        n=len(selec)
        ret=[]

        if n%2==1:
            ret.append(selec[-1])
            n-=1  

        corte_maximo=d-1

        for i in range(0, n, 2):
            ind1 = selec[i]
            ind2 = selec[i+1]
            if random.random() < self.prob_cruce:
                corte = random.randint(1, corte_maximo)

                for j in range(corte):
                    ind1.cromosoma[j], ind2.cromosoma[j] = ind2.cromosoma[j], ind1.cromosoma[j]

            ret.append(IndividuoGramatica(ind1.tam_cromosoma, self.filas, self.columnas,
                                          cromosoma=ind1.cromosoma,ind=None))
            ret.append(IndividuoGramatica(ind2.tam_cromosoma, self.filas, self.columnas,
                                          cromosoma=ind2.cromosoma,ind=None))
            

        return ret     
        
        
    def mutacion_poblacionBin(self, selec):
        ret=[]    
        
        if self.mutacion_idx==0: return self.mutacion.mut_basicaBin(selec)
        else:
            print("Mutacion Binaria, Solo hay mutacion basica")
            exit(1)
    
    def mutacion_poblacionReal(self, selec):
        ret=[]    
        
        if self.mutacion_idx==1: return self.mutacion.insercion(selec)
        elif self.mutacion_idx==2: return self.mutacion.intercambio(selec) 
        elif self.mutacion_idx==3: return self.mutacion.inversion(selec) 
        elif self.mutacion_idx==4: return self.mutacion.heuristica(selec)
        else:
            print("Cruce Real, No hay Mutacion Basica")
            exit(1)

    def mutacion_poblacionArbol(self, selec):
        ret=[]   
        if self.mutacion_idx==5: return self.mutacion.terminal(selec) 
        elif self.mutacion_idx==6: return self.mutacion.funcional(selec) 
        elif self.mutacion_idx==7: return self.mutacion.arbol(selec)  
        elif self.mutacion_idx==8: return self.mutacion.permutacion(selec) 
        elif self.mutacion_idx==9: return self.mutacion.hoist(selec)  
        elif self.mutacion_idx==10: return self.mutacion.contraccion(selec) 
        elif self.mutacion_idx==11: return self.mutacion.expansion(selec)   
        else:
            print("Cruce Arbol, No hay Mutacion Basica o las reales")
            exit(1)

    def mutacion_poblacionGramatica(self, selec):
        ret=[]

        for ind in selec:
            if random.random()<self.prob_mut:
                rand=random.randint(0, self.long_cromosoma - 1)
                ind.cromosoma[rand]=random.randint(0, 255)
            
            ret.append(IndividuoGramatica(ind.tam_cromosoma, self.filas, self.columnas,
                                          cromosoma=ind.cromosoma,ind=None))
        return ret  
   

# -----------------------------------------------------------------------------------------------
# --- MAIN --------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------


def main():
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion

    
    
    seleccion_opt = ["Ruleta", 
                     "Torneo Determinista", 
                     "Torneo Probabilístico", 
                     "Estocástico Universal",
                     "Truncamiento",
                     "Restos",
                     "Ranking"]
        
    cruce_opt = ["Básica", 
                 "Uniforme",
                 
                 "PMX",
                 "OX",
                 "OX-PP",
                 "CX",
                 "CO",
                 
                 "Intercambio"]
    
    mutacion_opt = ["Básica",
                    
                    "Insercion",
                    "Intercambio",
                    "Inversion",
                    "Heuristica",
                    
                    "Terminal",
                    "Funcional",
                    "Arbol",
                    "Permutacion",
                    "Hoist",
                    "Contraccion",
                    "Expansion"]

    funcion_opt = ["F1: Calibracion y Prueba",
                   "F2: Mishra Bird",
                   "F3: Holder table",
                   "F4: Michalewicz (Binaria)",
                   "Aeropuerto 1",
                   "Aeropuerto 2",
                   "Aeropuerto 3",
                   "Arbol",
                   "Gramatica"]
    
    # DATOS A COMPARTIR
    tam_poblacion=0
    generaciones=0
    num_genes=0
    seleccion_idx=0
    cruce_idx=0
    prob_cruce=0.0
    mut_idx=0
    prob_mut=0.0 
    precision=0.00 
    funcion_idx=0
    elitismo=0 

    modo=0
    profundidad=0
    long_cromosoma=0
    filas=0
    columnas=0    
    bloating_idx=0
    ticks=0

    poblacion=[]           # Individuo[]
   

    mejor_total=0.0        

    # 
    tam_seleccionados=0
    num_torneo=5 

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    if myrank==MASTER:
        tam_poblacion=100
        generaciones=10

        # 0: Ruleta | 1: Torneo Determinista  | 2: Torneo Probabilístico | 3: Estocástico Universal 
        #           | 4: Truncamiento  | 5: Restos | 6: Ranking
        seleccion_idx=1
        # 0: Basica | 1: Uniforme | 
        # 2: PMX    | 3: OX       | 4: OX-PP | 5: CX | 6: CO
        # 7: Intercambio
        cruce_idx=0
        prob_cruce=0.6
        # 0: Basica    |     
        # 1: Insercion | 2: Intercambio | 3: Inversion    | 4: Heuristica
        # 5: Terminal  | 6: Funcional   | 7: Arbol        | 8: Permutacion
        #              | 9: Hoist       | 10: Contraccion | 11: Expansion
        mut_idx=0
        # Binario: 0.05 | Real: 0.3
        prob_mut=0.3 
        precision=0.01
        # 0: Funcion 1    | 1: Funcion 2    | 2: Funcion 3    | 3: Funcion 4
        # 4: Aeropuerto 1 | 5: Aeropuerto 2 | 6: Aeropuerto 3 | 
        # 7: Arbol        | 8: Gramatica
        funcion_idx=0
        num_genes=2
        elitismo=0

        # 0: Completa | 1: Creciente | 2: Ramped & Half 
        modo=0
        profundidad=4

        long_cromosoma=100

        filas=8
        columnas=8
        # 0: Sin | 1: Tarpeian | 2: Poli and McPhee
        bloating_idx=0
        ticks=100

        print("\nFuncion: {}\t Seleccion: {}\t Cruce: {} (p:{})\tMutacion:{} (p:{})".format(funcion_opt[funcion_idx],
                                                                      seleccion_opt[seleccion_idx],
                                                                      cruce_opt[cruce_idx],
                                                                      prob_cruce,
                                                                      mutacion_opt[mut_idx],
                                                                      prob_mut))
    
        print("Tam. Poblacion: {}\t Num. Generaciones: {}\t Elitismo: {}%".format(tam_poblacion*numWorkers,
                                                                             generaciones,
                                                                             elitismo))

    totalTimeStart = MPI.Wtime()

    tam_poblacion=comm.bcast(tam_poblacion, root=MASTER)
    generaciones=comm.bcast(generaciones, root=MASTER)
    seleccion_idx=comm.bcast(seleccion_idx, root=MASTER)
    cruce_idx=comm.bcast(cruce_idx, root=MASTER)
    prob_cruce=comm.bcast(prob_cruce, root=MASTER)
    mut_idx=comm.bcast(mut_idx, root=MASTER)
    prob_mut=comm.bcast(prob_mut, root=MASTER)
    precision=comm.bcast(precision, root=MASTER)
    funcion_idx=comm.bcast(funcion_idx, root=MASTER)
    num_genes=comm.bcast(num_genes, root=MASTER)
    elitismo=comm.bcast(elitismo, root=MASTER)      
    
    modo=comm.bcast(modo, root=MASTER)
    profundidad=comm.bcast(profundidad, root=MASTER)
    long_cromosoma=comm.bcast(long_cromosoma, root=MASTER)
    filas=comm.bcast(filas, root=MASTER)
    columnas=comm.bcast(columnas, root=MASTER)
    bloating_idx=comm.bcast(bloating_idx, root=MASTER)
    ticks=comm.bcast(ticks, root=MASTER)
    
    

    if myrank==MASTER:
        mejor_total=float("inf")
        progreso=[]
        while generaciones>0:
            
            
            for _ in range(numWorkers):
                # ENVIA EL MEJOR
                data=comm.recv(source=MPI.ANY_SOURCE) 
                if mejor_total>data: mejor_total=data 

            progreso.append(mejor_total)            
            generaciones-=1
        totalTimeEnd = MPI.Wtime()
        print("Valor Optimo: {}\n".format(progreso[-1]))
        print("Tiempo de ejecucion total: {}\n".format(totalTimeEnd-totalTimeStart))

        GUI(progreso)

        
        
    else: # WORKER
        AG=AlgoritmoGenetico(None)
        AG.set_valores( tam_poblacion, 
                        generaciones, 
                        seleccion_idx,
                        cruce_idx, 
                        prob_cruce,
                        mut_idx, 
                        prob_mut,
                        precision, 
                        funcion_idx, 
                        num_genes, 
                        elitismo,
                        modo,
                        profundidad,
                        long_cromosoma,
                        filas,
                        columnas,
                        bloating_idx,
                        ticks) 

        if AG.funcion_idx<4: 
            selec=[]

            AG.init_poblacion()    
            AG.evaluacion_poblacionBin()                
            
            while generaciones>0:
                selec=AG.seleccion_poblacionBin(5)
                
                AG.poblacion=AG.cruce_poblacionBin(selec)
                AG.poblacion=AG.mutacion_poblacionBin(AG.poblacion)

                for i in range(AG.tam_elite):
                    AG.poblacion.append(AG.selec_elite[i])
                
                AG.evaluacion_poblacionBin()

                # ENVIA EL MEJOR
                comm.send(AG.mejor_total, dest=MASTER)  

                          
                
                generaciones-=1
        else:     
            selec=[]
            poblacion=[]

            AG.init_poblacion()    
            AG.evaluacion_poblacionReal()                
            
            while generaciones>0:
                selec=AG.seleccion_poblacionReal(5)
                
                AG.poblacion=AG.cruce_poblacionReal(selec)
                AG.poblacion=AG.mutacion_poblacionReal(AG.poblacion)

                for i in range(AG.tam_elite):
                    AG.poblacion.append(AG.selec_elite[i])
                
                AG.evaluacion_poblacionReal()

                # ENVIA EL MEJOR
                comm.send(AG.mejor_total, dest=MASTER)  

                          
                
                generaciones-=1
            
            

            #return self.mejor_total

        

    
    
    
    


main()
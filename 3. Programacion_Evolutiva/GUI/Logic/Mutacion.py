import sys
import os
import random

sys.path.append(os.path.abspath("Model"))

from Model import Individuo
from Model import IndividuoReal

class Mutacion:
    def __init__(self, p, aviones, tam_elite, heur, funcion):
        self.p=p
        self.aviones=aviones
        self.tam_elite=tam_elite
        self.permutaciones=[]
        self.heur=heur
        self.dfs(heur,0,[],[0 for i in range(heur)])
        #print(self.permutaciones)
        self.funcion=funcion
    

    def mut_basicaBin(self, selec):
        ret=[]
        for ind in selec:
            act=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind)
            for c in range(len(ind.genes)):
                for j in range(len(ind.genes[c].v)):
                    if random.random()<self.p:
                        act.genes[c].v[j]=(act.genes[c].v[j]+1)%2
            ret.append(Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=act))
        return ret
    

    def inversion(self, poblacion):
        tam_poblacion=len(poblacion)
        ret=[] # = new Individuo[tam_poblacion];
		
		
        act=None
        for i in range(tam_poblacion):                                
            act=IndividuoReal.IndividuoReal(aviones=None,
                              vInd=poblacion[i].v);	
            			
            if random.random()<self.p:
                corte1=int(random.random()*(len(act.v)-2))
                corte2=corte1+int(random.random()*(len(act.v)-corte1))
                separacion=(corte2-corte1+1)
                for k in range(separacion//2):
                    temp=act.v[corte1+k]
                    act.v[corte1+k]=act.v[corte2-k]
                    act.v[corte2-k]=temp
			
            ret.append(IndividuoReal.IndividuoReal(aviones=None,
                                     vInd=act.v))
		
        return ret


    def intercambio(self, poblacion):
        tam_poblacion=len(poblacion)
        ret=[] # = new Individuo[tam_poblacion];
		
		
        act=None
        for i in range(tam_poblacion):                                
            act=IndividuoReal.IndividuoReal(aviones=None,
                              vInd=poblacion[i].v);	
            			
            if random.random()<self.p:
                punto1=int(random.random()*(len(act.v)-2))
                punto2=punto1+int(random.random()*(len(act.v)-1-punto1))
                
                temp=act.v[punto1]
                act.v[punto1]=act.v[punto2]
                act.v[punto2]=temp
                
			
            ret.append(IndividuoReal.IndividuoReal(aviones=None,
                                     vInd=act.v))
		
        return ret
    

    def insercion(self, poblacion):
        tam_poblacion=len(poblacion)
        ret=[] # = new Individuo[tam_poblacion];
		
        
        act=None
        for i in range(tam_poblacion):                                
            act=IndividuoReal.IndividuoReal(aviones=None,
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
					
			
            ret.append(IndividuoReal.IndividuoReal(aviones=None,
                                     vInd=act.v))
		
        return ret
    

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
            act=IndividuoReal.IndividuoReal(aviones=None,
                              vInd=poblacion[i].v);	
            
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
                
                

                #act=new Individuo.Individuo(mejor);
                ret.append(IndividuoReal.IndividuoReal(aviones=None,
                                        vInd=mejor))
            else: 
                ret.append(IndividuoReal.IndividuoReal(aviones=None,
                                        vInd=act.v))
            
					
			
            
		
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
        
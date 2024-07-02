import sys
import os
import random

sys.path.append(os.path.abspath("Model"))


from Model import Individuo
from Model import IndividuoReal


class Cruce:
    def __init__(self, p, tam_elite, aviones):
        self.p=p    # int
        self.tam_elite=tam_elite
        self.aviones=aviones
    
    def cruce_monopuntoBin(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)]
        if n%2==1:
            ret[n-1]=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[n-1])
            n-=1
        
        long_genes=[len(selec[0].genes[i].v) for i in range(len(selec[0].genes))]
        corte_maximo=-1
        for l in long_genes:
            corte_maximo+=l
        i=0

        ind1=[]
        ind2=[]
        while i<n:
            ind1=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i])
            ind2=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i+1])
            
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
                        
            
            ret[i]=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind1)
            ret[i+1]=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind2)            
            i += 2     
               
        
        
        return ret
    
    def cruce_uniformeBin(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)]
        if n%2==1:
            ret[n-1]=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[n-1])
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
            ind1=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i])
            ind2=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i+1])

            
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

					
				
            
			
            ret[i]=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind1)
            ret[i+1]=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind2)            
            i+=2     
               
        
        
        return ret
    
    def PMX(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal.IndividuoReal(aviones=None,
                                   vInd=selec[n-1].v) 
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
            ind1=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=selec[i].v)
            ind2=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=selec[i+1].v)
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

				
			
            ret[i]=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=ind1.v)
            ret[i+1]=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=ind2.v)
            i+=2
			
		
        return ret
    
    def OX(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal.IndividuoReal(aviones=None,
                                   vInd=selec[n-1].v) 
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
            ind1=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=selec[i].v)
            ind2=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=selec[i+1].v)

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
                
                

                

            
            ret[i]=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=ind1.v)
            ret[i+1]=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=ind2.v)
            i+=2
        
        return ret
    
    # TODO REVISAR
    def OX_PP(self, selec, pp):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal.IndividuoReal(aviones=None,
                                   vInd=selec[n-1].v) 
            n-=1 # Descarta al ultimo si es impar

        i=0
        k=0
        ppi=0
        ind1=None
        ind2=None
        validos=[0 for _ in range(self.aviones-pp)]
        while i<n:
            ind1=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=selec[i].v)
            ind2=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=selec[i+1].v)

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

                
                
                

            
            ret[i]=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=ind1.v)
            ret[i+1]=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=ind2.v)
            i+=2
        
        return ret
    
    def CX(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal.IndividuoReal(aviones=None,
                                   vInd=selec[n-1].v) 
            n-=1 # Descarta al ultimo si es impar
		
		
		 
        i=0
        ind1=None
        ind2=None
        while i<n:
            ind1=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=selec[i].v)
            ind2=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=selec[i+1].v)

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
                
                    
                
                
				
			
            ret[i]=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=ind1.v)
            ret[i+1]=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=ind2.v)
            i+=2
			
		
        return ret
    
    def CO(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] 

        if n%2==1 :
            ret[n-1]=IndividuoReal.IndividuoReal(aviones=None,
                                   vInd=selec[n-1].v) 
            n-=1 # Descarta al ultimo si es impar
		
		
        i=0
        k=0
        e=0
        ind1=None
        ind2=None
        corte1=0
        while i<n:
            ind1=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=selec[i].v)
            ind2=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=selec[i+1].v)

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
                
				
			
            ret[i]=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=ind1.v)
            ret[i+1]=IndividuoReal.IndividuoReal(aviones=None,
                               vInd=ind2.v)
            i+=2
			
		
        return ret
import random
import sys
import os
sys.path.append(os.path.abspath("Model"))
import Individuo

class Seleccion:
    def __init__(self, tam_poblacion, opt):        
        self.tam_poblacion=tam_poblacion    # int  
        self.opt=opt                        # Boolean
    
    def busquedaBinaria(self, x, prob_acumulada):
        """
        x: double
        prob_acumulada: double[]
        """
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
        """
        poblacion:          Individuo[]
        prob_acumulada:     double[]
        tam_seleccionados:  int
        """
        seleccionados = []  # Individuo[]
        rand = 0.0
        #print_poblacion()
        for i in range(tam_seleccionados):
            rand=random.random()                       
            index = self.busquedaBinaria(rand, prob_acumulada)
            seleccionados.append(poblacion[index]) 

        return seleccionados
    

    def torneo_deterministico(self, poblacion, k, tam_seleccionados) :
        """
        poblacion:          Individuo[] 
        k:                  int
        tam_seleccionados:  int
        """
		
        seleccionados=[]    # Individuo[]	
        randomFitness=0.0
        indexMax=0
        indexMin=0
        max=0.0
        min=0.0
        
        for i in range(tam_seleccionados):				    
            max=-1.79769E+308			
            min=1.79769E+308             			
            indexMax=-1			
            indexMin=-1
            for j in range(k):                                  				
                randomIndex=random.randint(0,self.tam_poblacion-1)                				
                randomFitness = poblacion[randomIndex].fitness
				
                if randomFitness > max :					
                    max = randomFitness					
                    indexMax = randomIndex				
			    
                if randomFitness < min :					
                    min = randomFitness					
                    indexMin = randomIndex			
			
			#Individuo.Individuo(poblacion[indexMin])
            if self.opt==True: seleccionados.append(poblacion[indexMax])
            else : seleccionados.append(poblacion[indexMin])	

		
        return seleccionados # Individuo[]
	


    
    def torneo_probabilistico():
        # TODO
        return ""
    
    def estocastico_universal():
        # TODO
        return ""

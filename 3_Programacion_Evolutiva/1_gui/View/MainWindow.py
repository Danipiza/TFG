import tkinter as tk
from tkinter import ttk
import sys
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sys.path.append(os.path.abspath("Logic"))

from Logic import Cruce
from Logic import AlgoritmoGenetico as AG

class MainWindow:
    def __init__(self) :
        self.poblacion_text=None
        self.generaciones_text=None
        self.seleccion_combo=None
        self.cruce_combo=None
        self.probCruce_text=None
        self.mutacion_combo=None
        self.probMutacion_text=None
        self.precision_text=None
        self.funcion_combo=None
        self.numGenes_text=None
        self.elitismo_text=None
        
        self.AG=AG.AlgoritmoGenetico(self)

        self.result_label=None
        
        self.initGUI()
            
    def initGUI(self):
        # Crea la ventana principal
        root = tk.Tk()
        root.title("Algoritmo Genetico")
        root.geometry("1000x700")

        
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
                     "CO"]
        
        mutacion_opt = ["Básica",
                        "Insercion",
                        "Intercambio",
                        "Inversion",
                        "Heuristica"]

        funcion_opt = ["F1: Calibracion y Prueba",
                       "F2: Mishra Bird",
                       "F3: Holder table",
                       "F4: Michalewicz (Binaria)",
                       "Aeropuerto 1",
                       "Aeropuerto 2",
                       "Aeropuerto 3"]
        


        # POBLACION - TEXT
        tk.Label(root, text="Poblacion:").grid(row=0, column=0, padx=7, pady=7, sticky="w")
        self.poblacion_text = tk.Entry(root,width=23)        
        self.poblacion_text.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.poblacion_text.insert(0, "100")  

        # GENERACIONES - TEXT
        tk.Label(root, text="Generaciones:").grid(row=1, column=0, padx=7, pady=7, sticky="w")
        self.generaciones_text = tk.Entry(root,width=23)
        self.generaciones_text.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.generaciones_text.insert(0, "100")   

        # Create combo boxes        
        tk.Label(root, text="Met. Seleccion:").grid(row=2, column=0, padx=7, pady=7, sticky="w")
        self.seleccion_combo = ttk.Combobox(root, values=seleccion_opt)
        self.seleccion_combo.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.seleccion_combo.current(0)
        
        tk.Label(root, text="Met. Cruce:").grid(row=3, column=0, padx=7, pady=7, sticky="w")
        self.cruce_combo = ttk.Combobox(root, values=cruce_opt)        
        self.cruce_combo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.cruce_combo.current(0)

        tk.Label(root, text="Prob. Cruce:").grid(row=4, column=0, padx=7, pady=7, sticky="w")
        self.probCruce_text = tk.Entry(root,width=23)        
        self.probCruce_text.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.probCruce_text.insert(0, "0.6")  

        tk.Label(root, text="Met. Mutación:").grid(row=5, column=0, padx=7, pady=7, sticky="w")
        self.mutacion_combo = ttk.Combobox(root, values=mutacion_opt)        
        self.mutacion_combo.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.mutacion_combo.current(0)

        tk.Label(root, text="Prob. Mutación:").grid(row=6, column=0, padx=7, pady=7, sticky="w")
        self.probMutacion_text = tk.Entry(root,width=23)
        self.probMutacion_text.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        self.probMutacion_text.insert(0, "0.05")  

        tk.Label(root, text="Precisión:").grid(row=7, column=0, padx=7, pady=7, sticky="w")
        self.precision_text = tk.Entry(root,width=23)
        self.precision_text.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        self.precision_text.insert(0, "0.001")  

        tk.Label(root, text="Función:").grid(row=8, column=0, padx=7, pady=7, sticky="w")
        self.funcion_combo = ttk.Combobox(root, values=funcion_opt)        
        self.funcion_combo.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        self.funcion_combo.current(0)

        tk.Label(root, text="Num. Genes:").grid(row=9, column=0, padx=7, pady=7, sticky="w")
        self.numGenes_text = tk.Entry(root,width=23)
        self.numGenes_text.grid(row=9, column=1, padx=5, pady=5, sticky="w")
        self.numGenes_text.insert(0, "2")  

        tk.Label(root, text="Elitismo (%):").grid(row=10, column=0, padx=7, pady=7, sticky="w")
        self.elitismo_text = tk.Entry(root,width=23)
        self.elitismo_text.grid(row=10, column=1, padx=5, pady=5, sticky="w")
        self.elitismo_text.insert(0, "0")      


       

        # BOTON
        calculate_button = tk.Button(root, text="Ejecuta", command=self.ejecuta)
        calculate_button.grid(row=11, column=1, columnspan=2, padx=5, pady=5)


        # PRINT
        self.result_label = tk.Label(root, text="Optimo:")
        self.result_label.grid(row=12, column=1, columnspan=2, padx=5, pady=5)

        
        # Canvas 
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=2, rowspan=11, padx=10, pady=10) # TODO CAMBIAR POSICION -> AQUI?

        # Para poder cerrar
        root.protocol("WM_DELETE_WINDOW", self.cierra)
        
        # Start 
        root.mainloop()

    def ejecuta(self):
        try:
            self.AG=AG.AlgoritmoGenetico(self)
            
            seleccion_idx=self.seleccion_combo.current()
            precision=float(self.precision_text.get())

            tam_poblacion=int(self.poblacion_text.get())
            if tam_poblacion<1: raise ValueError("tam. poblacion > 0")

            generaciones=int(self.generaciones_text.get())
            if generaciones<0: raise ValueError("num. generaciones >= 0")
            
            prob_cruce=float(self.probCruce_text.get())
            if prob_cruce<0 or prob_cruce>1: raise ValueError("prob. cruce => [0-1]")
            prob_mut=float(self.probMutacion_text.get())
            if prob_mut<0 or prob_mut>1: raise ValueError("prob. mutacion => [0-1]")
            
            elitismo=float(self.elitismo_text.get())
            if elitismo<0 or elitismo>100: raise ValueError("Elitismo es un porcentaje de 0-100")
            
            numGenes=int(self.numGenes_text.get())
            if numGenes<0: raise ValueError("num. genes es un numero natural positivo")
            
            funcion_idx=self.funcion_combo.current()
            cruce_idx=self.cruce_combo.current()            
            mutacion_idx=self.mutacion_combo.current()

            if(funcion_idx<4):
                if funcion_idx!=3 and numGenes!=2: raise ValueError("num. genes=2")
                if cruce_idx>1: raise ValueError("Cruce Binario: solo tiene cruce Mono-Punto y Uniforme")
                if mutacion_idx>0: raise ValueError("Mutacion Binaria: solo tiene Mutacion Basica")
            else:                
                if cruce_idx<2: raise ValueError("Cruce Real: no tiene cruce Mono-Punto ni Uniforme")
                if mutacion_idx==0: raise ValueError("Mutacion Real: no tiene Mutacion Basica")
            
                      
            
            

            
            
            self.AG.set_valores(tam_poblacion,
                                generaciones,
                                seleccion_idx,
                                cruce_idx,
                                prob_cruce,
                                mutacion_idx,
                                prob_mut,
                                precision,
                                funcion_idx,
                                numGenes,
                                elitismo) 

            
            
            self.AG.ejecuta()
            
        except ValueError as e:
            self.result_label.config(text="{}".format(e))
    
    def Plot2D(self, vals, ind, aviones):       
        self.ax.clear()

        x=[(i) for i in range(len(vals[0]))]
        
        y1=vals[0]
        y2=vals[1]
        y3=vals[2]
        y4=vals[3]
        
        self.ax.plot(x, y1, color='b', label='Mejor Absoluto')
        self.ax.plot(x, y2, color='r', label='Mejor de la Generacion')
        self.ax.plot(x, y3, color='g', label='Media')
        self.ax.plot(x, y4, color='black', label='Presion Selectiva')
        self.ax.set_xlabel('Generaciones')
        self.ax.set_ylabel('Fitness')
        self.ax.legend()
        
        
        # Draw plot
        self.canvas.draw()
        texto="Optimo: {}\n".format(ind.fitness)
        if self.funcion_combo.current()<4:
            for i in range(len(ind.genes)):
                texto+="Variable {}: {}\n".format(i+1,ind.fenotipo[i])
        elif self.funcion_combo.current()<6:
            for i in range(aviones):
                texto+="{} ".format(ind.v[i])            
        else:
            texto+="{} ".format(ind.v[0])  
            for i in range(1,aviones):
                if i%25==0: texto+="\n"
                texto+="{} ".format(ind.v[i])  
        texto+="\nPresion Selectiva final: {}\n".format(y4[-1])
        self.result_label.config(text=texto)
        
    

    def cierra(self):
        plt.close()
        sys.exit()
    



    
        
mW=MainWindow()




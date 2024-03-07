import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.append(os.path.abspath("Logic"))

from Logic import AlgoritmoGenetico as AG
""" pip install matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg"""

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
        
        self.AG=AG.AlgoritmoGenetico()

        self.options_label=None
        self.result_label=None
        
        self.initGUI()
        
    
    def initGUI(self):
        # Crea la ventana principal
        # Create the main window
        root = tk.Tk()
        root.title("Algoritmo Genetico")
        root.geometry("600x500")

        

        seleccion_opt = ["Ruleta", 
                         "Torneo Determinista", 
                         "Torneo Probabilístico", 
                         "Estocástico Universal1",
                         "Estocástico Universal2",
                         "Truncamiento",
                         "Restos"]
        
        cruce_opt = ["Básica", 
                     "Uniforme",
                     "Aritmetica",
                     "BLX"]
        
        mutacion_opt = ["Básica"]

        funcion_opt = ["F1: Calibracion y Prueba",
                       "F2: Mishra Bird",
                       "F3: Holder table",
                       "F4: Michalewicz (Binaria)",
                       "F5: Michalewicz (Real)"]
        


        
       

      

        # POBLACION - TEXT
        tk.Label(root, text="Poblacion:").grid(row=0, column=0, padx=7, pady=7, sticky="w")
        self.poblacion_text = tk.Entry(root,width=23)        
        self.poblacion_text.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.poblacion_text.insert(0, "100")  # Por defecto

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
        self.probCruce_text.insert(0, "0.5")  

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
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=12, column=1, columnspan=2, padx=5, pady=5)

        self.options_label = tk.Label(root, text="")
        self.options_label.grid(row=13, column=1, columnspan=2, padx=5, pady=5)

        # Start 
        root.mainloop()


    def ejecuta(self):
        try:
            AG.set_valores(self.poblacion_text.get(),
               self.generaciones_text.get(),
               self.seleccion_combo.get(),
               self.cruce_combo.get(),
               self.probCruce_text.get(),
               self.mutacion_combo.get(),
               self.probMutacion_text.get(),
               self.precision_text.get(),
               self.funcion_combo.get(),
               self.numGenes_text.get(),
               self.elitismo_text.get())
            self.AG.ejecuta()
            self.AG.printMejor()
            
            """v_poblacion = float(self.poblacion_text.get())
            v_generaciones = float(self.generaciones_text.get())
            self.result_label.config(text=f"Sum: {value1 + value2}")

            selected_option1 = self.seleccion_combo.get()
            selected_option2 = self.cruce_combo.get()
            self.options_label.config(text=f"Selected options: {selected_option1}, {selected_option2}")"""
        except ValueError:
            self.result_label.config(text="Datos inválidos")

    """def Plot2D():
        # Sample plot data
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 5, 7, 11]

        # Create a figure and axis
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_title('Sample Plot')

        # Create a canvas for plotting
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=2, rowspan=11, padx=10, pady=10)"""

    
        
mW=MainWindow()




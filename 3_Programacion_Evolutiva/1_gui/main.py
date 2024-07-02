import sys
import os

sys.path.append(os.path.abspath("Logic"))
sys.path.append(os.path.abspath("View"))

from View import MainWindow 
from Logic import AlgoritmoGenetico as AGe

# TODO Truncamiento no funciona muy bien para la F4


GUI=True

if GUI==False:
    AG=AGe.AlgoritmoGenetico(None)
    
        
        
    tam_poblacion=100
    generaciones=100
    
    # 0: Ruleta | 1: Torneo Determinista  | 2: Torneo Probabilístico | 3: Estocástico Universal | 4: Truncamiento  | 5: Restos | 6: Ranking
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
    
    val=AG.ejecuta()
    print(val)
else :MainWindow()
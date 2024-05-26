import matplotlib.pyplot as plt
import os

# Lee datos de un archivo de texto (.txt) 
def leeArchivo(archivo):
    """
    archivo (str): nombre del archivo a leer
    
    
    return array : float[]
    """
    archivo+=".txt"
    array=[]
    
    with open(archivo, 'r') as file:        
        for line in file:            
            array.extend(map(float, line.strip().split(',')))
    
    return array

# Crea un grafico con varias funciones.
def GUI(x, funciones, labels):
    """           
    x: int[]                Eje X
    funciones: float[][]    Lista de Funciones. 
    labels:                 Lista de Etiquetas 
    """
    #colores = ['black','blue', 'green', 'red', 'yellow','cyan', 'magenta', 'white']
    colores = ['blue', 'red', 'green', 'black',  'magenta', 'brown', 'darkgreen', 'pink', 'yellow','gray', 'fuchsia',
            'violet', 'salmon', 'darkturquoise', 'forestgreen', 'firebrick', 'darkblue', 'lavender', 'palegoldenrod',
            'navy']

    fig, ax = plt.subplots(figsize=(12,8))

    # Poner las funciones  
    for i, func in enumerate(funciones):
        ax.plot(x, func, label=labels[i], color=colores[i])

    
    ax.text(0.95, 0.05, "", verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes)    
    ax.set_xlabel("Tam. Población (N)")    # Eje X
    ax.set_ylabel("Tiempo (s)")     # Eje Y
    ax.legend()                     # Leyenda
    
    plt.show()

def main():
    labels=["pevP"]

    # Ordenaciones
    # N2
    #labels = ["BubbleSort","InsertionSort","SelectionSort","SequentialSort","SequentialSort_MPI(5)"]
    #labels = ["SequentialSort_1MPI(5)","SequentialSort_2MPI(5)"]
    # NlogN
    #labels = ["MergeSort","MergeSort_MPI(4)","MergeSort_MPI(8)","MergeSort_MPI(16)","MergeSort_MPI(32)",]

    # Aglomerativo      
    #labels=["ESimple_Euclidea","ESimple_Manhattan","Centroide_Euclidea","Centroide_Manhattan"]
    #labels=["Secuencial","1MPI(4)","2MPI(4)"]#,"MPI(20)"]


    # RL
    #labels=["Normal", "Preprocesado"]
    

    # KMedias
    #labels=["Euclidea","Manhattan","Euclidea_MPI(4)","Manhattan_MPI(4)"]
    
    
    # PEV
        # BIN
    # labels=["P2","P10"]
    #labels=["P2","P10","P2_3MPI(7)","P10_3MPI(7)"]
        
        # REAL
    #labels=["AER1","AER2","AER3"]
    #labels=["AER1","AER2","AER3","AER1_MPI(4)","AER2_MPI(4)","AER3_MPI(4)"]
    #labels=["AER1","AER2","AER1_3MPI(4)","AER2_3MPI(4)"]
    #labels=["AER3","AER3_3MPI(6)", "AER3_3MPI(10)"]
    
     
        # ARBOL
    #labels = ["M8X8", "M100X100"]
    #labels = ["M8X8", "M8X8_1MPI(4)"]
    #labels=["M100X100","M100X100_1MPI(4)"]

    # Real
    # 1
    """labels = ["RealRuleta_Aer1", "Real1MPI4_Ruleta_Aer1", "Real2MPI4_Ruleta_Aer1"]"""
    # 2
    #labels = ["RealRuleta_Aer2", "Real1MPI4_Ruleta_Aer2", "Real2MPI4_Ruleta_Aer2"]
    # 3
    #labels = ["RealRuleta_Aer3", "Real1MPI4_Ruleta_Aer3", "Real2MPI4_Ruleta_Aer3"]

    # Arbol
    #labels = ["RedNeuronal1x5", "RedNeuronal_MPI2_1x5", "RedNeuronal_MPI4_1x5",]



    # KNN
    # Basico
    #labels=["Euclidea_Act","Euclidea_sinAct","Manhattan_Act","Manhattan_sinAct"]
    # Comparacion
    #labels=["Secuencial","1.1_MPI(4)","1.2_MPI(4)","2_MPI(4)"]


    # REDES NEURONALES
    # 10x10
    #labels=["Secuencial","2MPI(2)","2MPI(4)","2MPI(10)"]

    funciones=[leeArchivo(labels[i]) for i in range(len(labels))]  
  
    tam=float("inf")
    for f in funciones:
        tam=min(tam,len(f))
        print(len(f))
    # GENERAL
    #x=leeArchivo("TamDatos") 
    # PEV
    #x=[25,50,100,200,500,1000,2000]
    x=[10*i for i in range(1,1000)]
    if tam>len(x): tam=len(x)
    x=x[0:tam] 

    

    for i in range(len(labels)):
        funciones[i]=funciones[i][0:tam]
    
    
    #funciones.append([1 for _ in range(len(x))])
    #labels.append("") 

    GUI(x, funciones, labels)


main()

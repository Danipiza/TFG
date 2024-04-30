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

    fig, ax = plt.subplots()

    # Poner las funciones  
    for i, func in enumerate(funciones):
        ax.plot(x, func, label=labels[i], color=colores[i])

    
    ax.text(0.95, 0.05, "", verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes)    
    ax.set_xlabel("Espacio (N)")    # Eje X
    ax.set_ylabel("Tiempo (s)")     # Eje Y
    ax.legend()                     # Leyenda
    
    plt.show()

def main():
    # Aglomerativo
    #labels = ["Aglomerative_C_E", "Aglomerative_C_E_MPI4", "Aglomerative_C_E_MPI10", "Aglomerative_C_E_MPI15", "Aglomerative_C_E_MPI20"]
    
    # KMedias
    
    #labels = ["KMedias3M", "KMedias3M_MPI4", "KMedias3M_MPI10"]#,"KMedias3M_MPI15"]
    #labels = ["KMedias3E", "KMedias3E_MPI4", "KMedias3E_MPI10"]#,"KMedias3E_MPI15"]
    
    # KNN
    # act
    #labels = ["KNN_Act_k2_E", "KNN_1MPI4_Act_k2_E", "KNN_2MPI4_Act_k2_E"]
    #labels = ["KNN_Act_k2_M", "KNN_1MPI4_Act_k2_M", "KNN_2MPI4_Act_k2_M"]
    # no act
    #labels = ["KNN_NoAct_k2_E", "KNN_1MPI4_NoAct_k2_E", "KNN_2MPI4_NoAct_k2_E"]
    #labels = ["KNN_NoAct_k2_M", "KNN_1MPI4_NoAct_k2_M", "KNN_2MPI4_NoAct_k2_M"]


    # REDES NEURONALES
    # 1x5
    labels = ["RedNeuronal1x5", "RedNeuronal_MPI2_1x5", "RedNeuronal_MPI4_1x5","RedNeuronal_MPI10_1x5"]
    # 2x10
    #labels = ["RedNeuronal2x10", "RedNeuronal_MPI2_2x10", "RedNeuronal_MPI4_2x10","RedNeuronal_MPI10_2x10"]
    # 10x10
    #labels = ["RedNeuronal10x10", "RedNeuronal_MPI2_10x10", "RedNeuronal_MPI4_10x10","RedNeuronal_MPI10_10x10"]


    funciones=[leeArchivo(labels[i]) for i in range(len(labels))]  
    tam=float("inf")
    for f in funciones:
        tam=min(tam,len(f))
    
    x=leeArchivo("TamDatos")    
    if tam>len(x): tam=len(x)
    x=x[0:tam]  

    for i in range(len(labels)):
        funciones[i]=funciones[i][0:tam]
    
    
    #funciones.append([1 for _ in range(len(x))])
    #labels.append("") 

    GUI(x, funciones, labels)


main()

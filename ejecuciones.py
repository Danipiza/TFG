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
    colores = ['black','blue', 'green', 'red', 'yellow','cyan', 'magenta', 'white']

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
    labels = ["BubbleSort", "InsertionSort", "SelectionSort", "SequentialSort", "MergeSort"]
    
    x=leeArchivo("TamArray")
    funciones=[leeArchivo(labels[i]) for i in range(len(labels))]  
    funciones[4]=funciones[4][0:len(x)]
    funciones.append([1 for _ in range(len(x))])
    labels.append("")

    GUI(x, funciones, labels)


main()

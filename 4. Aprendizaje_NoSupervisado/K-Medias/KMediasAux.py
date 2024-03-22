
"""
def davies_bouldin_y_mejor(k, mejores, poblacion, asignacion):
    import matplotlib.pyplot as plt
    # Crear figura y ejes
    fig, axs = plt.subplots(1,2, figsize=(12, 6))
    
    # Definir los datos grafico 1
    x1 = [i for i in range(2, k + 1)]    
    #y2=mejores    

    # Graficar primer diagrama
    axs[0].plot(x1, mejores, 'ro', linestyle='-')
    axs[0].set_xlabel('Clusters')
    axs[0].set_ylabel('Coeficiente')
    axs[0].set_title('Davies Bouldin')
    axs[0].grid(True)


     # Definir los datos grafico 2
    colors = ['blue', 'red', 'green', 'black', 'pink', 'yellow', 'magenta', 'brown', 'darkgreen', 'gray', 'fuchsia',
            'violet', 'salmon', 'darkturquoise', 'forestgreen', 'firebrick', 'darkblue', 'lavender', 'palegoldenrod',
            'navy']
    n=len(poblacion)

    x2=[[]for _ in range(k)]
    y2=[[]for _ in range(k)]
    for i in range(n):
        x2[asignacion[i]].append(poblacion[i][0])
        y2[asignacion[i]].append(poblacion[i][1])
           


    # Graficar segundo diagrama
    for i in range(k):
        axs[1].scatter(x2[i], y2[i], color=colors[i])
    
    
    axs[1].set_xlabel('X')
    axs[1].set_ylabel('Y')
    axs[1].set_title('2D-Plot')



    # Mostrar la figura con ambos gráficos
    plt.tight_layout()
    plt.show()

def diagrama_codo_y_mejor(k, fits, poblacion,asignacion):    
    # Crear figura y ejes
    fig, axs = plt.subplots(1,2, figsize=(12, 6))
    
    # Definir los datos grafico 1
    x1 = [i for i in range(1, k + 1)]    
    #y2=mejores    

    # Graficar primer diagrama
    axs[0].plot(x1, fits, 'ro', linestyle='-')
    axs[0].set_xlabel('Clusters')
    axs[0].set_ylabel('Fitness')
    axs[0].set_title('Diagrama de codo')
    axs[0].grid(True)


    
    # Definir los datos grafico 2
    colors = ['blue', 'red', 'green', 'black', 'pink', 'yellow', 'magenta', 'brown', 'darkgreen', 'gray', 'fuchsia',
            'violet', 'salmon', 'darkturquoise', 'forestgreen', 'firebrick', 'darkblue', 'lavender', 'palegoldenrod',
            'navy']
    n=len(poblacion)

    x2=[[]for _ in range(k)]
    y2=[[]for _ in range(k)]
    for i in range(n):
        x2[asignacion[i]].append(poblacion[i][0])
        y2[asignacion[i]].append(poblacion[i][1])
           


    # Graficar segundo diagrama
    for i in range(k):
        axs[1].scatter(x2[i], y2[i], color=colors[i])
    
    
    axs[1].set_xlabel('X')
    axs[1].set_ylabel('Y')
    axs[1].set_title('2D-Plot')
    


    # Mostrar la figura con ambos gráficos
    plt.tight_layout()
    plt.show()

def diagrama_codo(k, mejores):
    x = [i for i in range(1,k+1)]
   
    plt.figure(figsize=(8, 6))  # Definir el tamaño del gráfico 
    plt.plot(x, mejores, 'ro')  # 'ro' indica que los puntos se representarán como círculos rojos
    plt.xlabel('Clusters')  
    plt.ylabel('Fitness')  
    plt.title('Diagrama de codo') 
    
    plt.plot(x, mejores, linestyle='-', color='blue')  # '-' indica una línea sólida, color='blue' para azul

    plt.grid(True)  # Mostrar cuadrícula 
    plt.show()  
"""
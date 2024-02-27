import numpy as np

"""

SE PUEDE HACER CON workers
1. CADA worker PROCESA UNA INSTANCIA
2. CADA worker PROCESA MUCHAS INSTANCIAS PASADAS POR UN ARRAY

USAR BARRERAS PARA QUE CADA worker VAYAN AL MISMO TIEMPO
Y ASI REDUCIR LOS POSIBLES FALLOS DE CLASIFICACION

TODO K-MEDIAS...

TODO Algoritmos de clustering jerárquico aglomerativo

DISTANCIAS ENTRE INDIVIDUOS
    Manhattan
    Euclidea 
    Chebychev

CAMBIAR DISTANCIAS ENTRE CLUSTERS
    Centroide
    Enlace simple (single linkage) 
    Enlace completo (complete linkage):

ELECCION DE NUMERO DE CLUSTERS

REGIONES VORONOI

INDICES QUE MIDEN LO "COMPACTO" DE LA SOLUCION
    Dunn
    Davies-Bouldin 
    Coeficiente de silueta:

DIAGRAMAS DE CODO

VALIDACION CRUZADA

DENDOGRAMAS
"""



def distancia_euclidea(x1, x2):
    return np.sqrt(np.sum((x1 - x2)**2))

def knn_clasificador(datos_entrenamiento, etiquetas, instancia_prueba, k):

    distancias=[distancia_euclidea(instancia_prueba, x) for x in datos_entrenamiento]
	
	# Ordena por menor distancia y coge las k mas cercanas
    k_indices=np.argsort(distancias)[:k]
	#print(k_indices)    
    # array con las etiquetas de los mas cercanos
    k_etiquetas=etiquetas[k_indices]
    c1=0
    c2=0
    for et in k_etiquetas:
        if et==0: c1+=1
        else : c2+=1

    ret=0
    if c1<c2: ret=1
    return ret


def ejecuta():

    """
    INIT: Definir los datos
    0-esimo, duracion
    1-esimo, intensidad
    2-esimo, cantante    
    """ 
    datos_entrenamiento = np.array([[3, 4, 2],  # Cancion que me gusta (etiqueda de mas abajo)
                            [1, 2, 1],  # Cancino que no me gusta
                            [4, 3, 2],  
                            [2, 1, 2]])

    # Etiquetas de las canciones (0: No me gusta, 1: Me gusta)
    etiquetas = np.array([1, 0, 1, 0])



    
    instancia_prueba = np.array([3, 2, 1])  # Valor a probar
    k = 3                                   # Número de vecinos

    # Clasificar la instancia de prueba
    prediccion = knn_clasificador(datos_entrenamiento, etiquetas, instancia_prueba, k)
    #prediccion = knn_clasificador(instancia_prueba, k)

    if prediccion == 1: print("La canción es similar a las que te gustan.")
    else: print("La canción es similar a las que no te gustan.")


ejecuta()
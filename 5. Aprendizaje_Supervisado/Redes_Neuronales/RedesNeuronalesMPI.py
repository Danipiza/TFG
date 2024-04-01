# FUNCIONA PERO NO MUY BIEN, ESTA CON poblacion*100 y sin append 

from mpi4py import MPI
import random
import os
import math

# EJECUTAR
# mpiexec -np 3 python RedesNeuronalesMPI.py

def lee(archivo):
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".Otros","ficheros","RedNeu", archivo+".txt")

    with open(path, 'r') as file:
        content = file.read()

    array = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')      
    for i in range(0, len(datos), 3):
        altura=float(datos[i])
        peso=float(datos[i+1])
        IMC=float(datos[i+2])

        array.append([altura,peso,IMC])

    #print("\n",array)        
    
    return array


# Normalizar los datos de altura y peso
def normalizar_dato(val,m,M):
    return (val-m)/(M-m)
# Desnormalizar el IMC
def desnormalizar_dato(val,m,M):
    return val*(M-m)+m

"""# Normalizar los datos de altura y peso
def normalizar_muchos_datos(vals,m,M):
    n=len(vals)
    return [(vals[i]-m[i])/(M[i]-m[i]) for i in range(n)]
# Desnormalizar el IMC
def normalizar_muchos_datos(vals,m,M):
    n=len(vals)
    return [vals[i]*(M[i]-m[i])+m[i] for i in range(n)]"""


# Funcion de activacion
def sigmoide(x):
    return 1/(1+math.exp(-x))
#Derivada (para el entrenamiento)
def sigmoide_derivado(x):
    return x*(1-x)

def main():
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    # DATOS A COMPARTIR 
    tam_entrada=0
    tam_oculta=0
    tam_salida=0
    
    
    
    
    # MASTER
    entrada=[]          # Valores de altura y peso, de los datos de entrenamiento/prediccion
    # Ultimo worker
    etiquetas=[]        # Etiquetas para ver el error, y actualizar con backpropagation.

    # TODOS
    capas=[]            # Numero de nodos de cada capa.
    capa_siguiente=0    # Numero de nodos de la siguiente capa.
    numCapas=0          # Numero de capas de cada proceso
    
    pesos=[]            # Peso de cada capa, nodo, siguiente nodo. peso[capa][act][sig] (menos el ultimo worker)
    salidas=[]          # salida de cada capa, nodo de la entrada que recibe. salida[capa][nodo]
    errores=[]          # Errores para actualizar cada capa

    learning_rate=0     # Aprendizaje.
    tam_entrenamiento=0      # tam_entrenamiento
    repeticiones=0
    entrada_prueba_tam=0
    
        
    

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    
    
    if myrank==MASTER:        
        #poblacion=lee("datos2042")
        poblacion=lee("datos80")
        poblacion=poblacion
        

        
        poblacion_prueba = [[1.72, 68],
                            [1.90, 85],
                            [1.60, 50]]        
        entrada_prueba_tam=len(poblacion_prueba)
        # peso[Kg]/altura^2[m]
        entrada_prueba_IMC=[(poblacion_prueba[i][1]/poblacion_prueba[i][0]**2) for i in range(entrada_prueba_tam)]

        # ----------------------------------------------------------------------------------------
        # --- Normalizar los datos ---------------------------------------------------------------
        # ----------------------------------------------------------------------------------------

        alturasD=[data[0] for data in poblacion]
        pesosD=[data[1] for data in poblacion]
        imcsD=[data[2] for data in poblacion]

        alturaD_min=min(alturasD)
        alturaD_max=max(alturasD)
        pesoD_min=min(pesosD)
        pesoD_max=max(pesosD)
        imcD_min=min(imcsD)
        imcD_max=max(imcsD)

        entrada=[[normalizar_dato(data[0], alturaD_min, alturaD_max), 
                  normalizar_dato(data[1], pesoD_min, pesoD_max), 
                  normalizar_dato(data[2], imcD_min, imcD_max)] for data in poblacion]
        

        entrada_prueba=[[normalizar_dato(data[0], alturaD_min, alturaD_max), 
                         normalizar_dato(data[1], pesoD_min, pesoD_max)] for data in poblacion_prueba]
        
        
        # ----------------------------------------------------------------------------------------
        # --- Definir la red neuronal ------------------------------------------------------------
        # ----------------------------------------------------------------------------------------
        
        tam_entrada=2
        tam_salida=1
        learning_rate=0.1
        tam_entrenamiento=80
        repeticiones=1#00
                
        """ Reparte capas TODO cambiar 
        tam_capas_ocultas=[10 for _ in range(2)] # 2 capas con 10 nodos
        """
        
        capas=[2]
        comm.send([5],dest=1)
        comm.send([1],dest=2)
        
        capa_siguiente=5
        comm.send(1,dest=1)
        
        # Etiquetas para el ultimo worker
        comm.send(tam_salida, dest=numWorkers)
        etiquetas=[]
        for x in entrada:
            etiquetas.append(x[2])               
        comm.send(etiquetas, dest=numWorkers)
        
        comm.send(entrada_prueba_IMC,dest=numWorkers)
        comm.send(imcD_min,dest=numWorkers)
        comm.send(imcD_max,dest=numWorkers)
    else: # Reciben capas
        capas=comm.recv(source=MASTER)
        if myrank!=numWorkers: capa_siguiente=comm.recv(source=MASTER)
        else: capa_siguiente=None

    
    learning_rate=comm.bcast(learning_rate,root=MASTER)
    tam_entrenamiento=comm.bcast(tam_entrenamiento,root=MASTER)
    repeticiones=comm.bcast(repeticiones,root=MASTER)
    entrada_prueba_tam=comm.bcast(entrada_prueba_tam,root=MASTER)
    
    numCapas=len(capas)

    # INICIALIZAR PESOS (el ultimo worker no tiene siguiente capa)
    pesos=[]
    """if myrank!=numWorkers:        
        for i in range(numCapas-1): # Capas intermedias
            pesos_capa = [[random.uniform(-1, 1) for _ in range(capas[i+1])] for _ in range(capas[i])]
            pesos.append(pesos_capa)
        # Ultima capa del proceso con la capa siguiente
        pesos_capa = [[random.uniform(-1, 1) for _ in range(capa_siguiente)] for _ in range(capas[numCapas-1])]
        pesos.append(pesos_capa)"""
    
    if myrank==0: pesos=[[[0.009291877242879387, -0.9951147922523249, 0.08905839012024352, -0.15405719243715832, 0.9174549957969651], [-0.8001749047430002, 0.6196351179863628, 0.4978160737825592, -0.6339024012446859, 0.6613399652927408]]]
    elif myrank==1:pesos=[[[0.6036843685017934], [-0.4981216808767255], [0.9150399216812313], [0.10772396548746266], [0.8819651957740591]]]
    

    if myrank!=numWorkers:
        print("(ANTES) ID: {}. pesos={}".format(myrank,pesos))
    
    timeStart = MPI.Wtime()

    for cont in range(repeticiones):
        salidas=[[] for _ in range(tam_entrenamiento)]
        
        
        
       
        # ENTRENAR
        if myrank==MASTER: # MASTER (ENTRADA)
            # En todo el entrenamiento se pierde espacio*2 de todas las tam_entrenamiento
            espacio=(numWorkers*2)-1  
                       

            # FORWARD
            for ind in range(espacio):                                             
                #salidas.append([entrada[ind][0:2]])      
                salidas[ind]=[entrada[ind][0:2]]
                
                # Capas intermedias del MASTER
                for i in range(numCapas-1):
                    entradas_capa=salidas[ind][-1]
                    salidas_capa=[0 for _ in range(capas[i+1])]                
                    # Recorre todos los nodos de la capa actual
                    for j in range(capas[i+1]):    
                        suma=0 # Suma todos los nodos de la capa anterior
                        for k in range(capas[i]):            
                            suma+=entradas_capa[k]*pesos[i][k][j]
                        salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                    
                    salidas[ind].append(salidas_capa)

                # Capa que conecta con el siguiente
                indice=numCapas-1
                entradas_capa=salidas[ind][-1]
                salidas_capa=[0 for _ in range(capa_siguiente)]
                # Recorre todos los nodos de la primera capa del siguiente procesp
                for j in range(capa_siguiente):    
                    suma=0 # Suma todos los nodos de la capa actual
                    for k in range(capas[indice]):            
                        suma+=entradas_capa[k]*pesos[indice][k][j]
                    salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                    
                salidas[ind].append(salidas_capa)
                
                # Devuelve el ultimo elemento
                comm.send(salidas[ind][-1],dest=1)
            
            # BACKPROPAGATION Y FORWARD
            for ind in range(espacio,tam_entrenamiento):            
                errores=comm.recv(source=1)
                
                # ACTUALIZA
                indice=numCapas-1
                # PROCESO ACTUAL CON EL QUE HACE BORDE
                nuevos_errores=[0 for _ in range(capas[indice])]            
                for j in range(capas[indice]): # Recorre todos los nodos de la capa que hace borde
                    suma=0 # Suma todos los nodos de la capa siguiente (del otro proceso)
                    for k in range(capa_siguiente):            
                        suma+=errores[k]*pesos[indice][j][k]
                    nuevos_errores[j]=suma*sigmoide_derivado(salidas[ind-espacio][indice][j])

                    # Actualiza los nodos
                    for k in range(capa_siguiente):
                        pesos[indice][j][k]+=learning_rate*errores[k]*salidas[ind-espacio][indice][j]
                errores=nuevos_errores
                
                # OTRAS CAPAS DEL PROCESO 
                for i in range(numCapas-2,-1,-1):
                    nuevos_errores=[0 for _ in range(capas[i])]
                    # Recorre todos los nodos de la capa actual
                    for j in range(capas[i]):
                        suma=0 # Suma todos los nodos de la capa siguiente 
                        for k in range(capas[i+1]):            
                            suma+=errores[k]*pesos[i][j][k]
                        nuevos_errores[j]=suma*sigmoide_derivado(salidas[ind-espacio][i][j])

                        # Actualiza los nodos
                        for k in range(capas[i+1]):
                            pesos[i][j][k]+=learning_rate*errores[k]*salidas[ind-espacio][i][j]

                    errores = nuevos_errores

                # ENVIA FORWARD                                             
                #salidas.append([entrada[ind][0:2]]) 
                salidas[ind]=[entrada[ind][0:2]]  
                # Capas intermedias del MASTER
                for i in range(numCapas-1):
                    entradas_capa=salidas[ind][-1]
                    salidas_capa=[0 for _ in range(capas[i+1])]
                    # Recorre todos los nodos de la capa actual
                    for j in range(capas[i+1]):    
                        suma=0
                        # Suma todos los nodos de la capa anterior
                        for k in range(capas[i]):            
                            suma+=entradas_capa[k]*pesos[i][k][j]
                        salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                    
                    salidas[ind].append(salidas_capa)
                # Capa que conecta con el siguiente
                indice=numCapas-1
                entradas_capa=salidas[ind][-1]
                salidas_capa=[0 for _ in range(capa_siguiente)]
                # Recorre todos los nodos de la capa actual
                for j in range(capa_siguiente):    
                    suma=0 # Suma todos los nodos de la capa anterior
                    for k in range(capas[indice]):            
                        suma+=entradas_capa[k]*pesos[indice][k][j]
                    salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                    
                salidas[ind].append(salidas_capa)
                
                # Devuelve el ultimo elemento
                comm.send(salidas[ind][-1],dest=1)

            

            # BACKPROPAGATION ACTUALIZA 
            for ind in range(espacio):
                errores=comm.recv(source=1)

                # ACTUALIZA
                indice=numCapas-1
                # PROCESO ACTUAL CON EL QUE HACE BORDE
                nuevos_errores=[0 for _ in range(capas[indice])]            
                for j in range(capas[indice]): # Recorre todos los nodos de la capa que hace borde
                    suma=0 # Suma todos los nodos de la capa siguiente (del otro proceso)
                    for k in range(capa_siguiente):            
                        suma+=errores[k]*pesos[indice][j][k]
                    nuevos_errores[j]=suma*sigmoide_derivado(salidas[tam_entrenamiento+ind-espacio][indice][j])

                    # Actualiza los nodos
                    for k in range(capa_siguiente):
                        pesos[indice][j][k]+=learning_rate*errores[k]*salidas[tam_entrenamiento+ind-espacio][indice][j]
                errores=nuevos_errores            
                        
                
                # OTRAS CAPAS DEL PROCESO 
                for i in range(numCapas-2,-1,-1):
                    nuevos_errores=[0 for _ in range(capas[i])]
                    # Recorre todos los nodos de la capa actual
                    for j in range(capas[i]):
                        suma=0 # Suma todos los nodos de la capa siguiente 
                        for k in range(capas[i+1]):            
                            suma+=errores[k]*pesos[i][j][k]
                        nuevos_errores[j]=suma*sigmoide_derivado(salidas[tam_entrenamiento+ind-espacio][i][j])

                        # Actualiza los nodos
                        for k in range(capas[i+1]):
                            pesos[i][j][k]+=learning_rate*errores[k]*salidas[tam_entrenamiento+ind-espacio][i][j]

                    errores = nuevos_errores
            timeEntrEnd = MPI.Wtime()
            print("Tiempo de Entrenamiento: {}s\n".format(timeEntrEnd-timeStart))
        elif myrank!=numProc-1: # Worker1 (OCULTA)
            # FORWARD
            entrada=comm.recv(source=myrank-1) # Recibe                         
            #salidas.append([entrada]) 
            salidas[0]=[entrada]
            # Capas INTERMEDIAS del PROCESO
            for i in range(numCapas-1):
                entradas_capa=salidas[0][-1]
                salidas_capa=[0 for _ in range(capas[i+1])]
                # Recorre todos los nodos de la capa actual
                for j in range(capas[i+1]):    
                    suma=0 # Suma todos los nodos de la capa anterior
                    for k in range(capas[i]):            
                        suma+=entradas_capa[k]*pesos[i][k][j]
                    salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                
                salidas[0].append(salidas_capa)
            # Capa que CONECTA con el SIGUIENTE
            indice=numCapas-1
            entradas_capa=salidas[0][-1]  
            
            salidas_capa=[0 for _ in range(capa_siguiente)]
            # Recorre todos los nodos de la primera capa del siguiente proceso
            for j in range(capa_siguiente):    
                suma=0 # Suma todos los nodos de la capa actual
                for k in range(capas[indice]):             
                    suma+=entradas_capa[k]*pesos[indice][k][j]
                salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                
            salidas[0].append(salidas_capa)
            
            # Devuelve el ultimo elemento                
            comm.send(salidas[0][-1],dest=myrank+1)

            # BACKPROPAGATION Y FORWARD
            for ind in range(tam_entrenamiento-1):                              
                errores=comm.recv(source=myrank+1)            
                
                # ACTUALIZA
                indice=numCapas-1
                # PROCESO ACTUAL CON EL QUE HACE BORDE
                nuevos_errores=[0 for _ in range(capas[indice])]            
                for j in range(capas[indice]): # Recorre todos los nodos de la capa que hace borde
                    suma=0 # Suma todos los nodos de la capa siguiente (del otro proceso)
                    for k in range(capa_siguiente):            
                        suma+=errores[k]*pesos[indice][j][k]
                    nuevos_errores[j]=suma*sigmoide_derivado(salidas[ind][indice][j])

                    # Actualiza los nodos
                    for k in range(capa_siguiente):
                        pesos[indice][j][k]+=learning_rate*errores[k]*salidas[ind][indice][j]
                errores=nuevos_errores
                
                
                # OTRAS CAPAS DEL PROCESO 
                for i in range(numCapas-2,-1,-1):
                    nuevos_errores=[0 for _ in range(capas[i])]
                    # Recorre todos los nodos de la capa actual
                    for j in range(capas[i]):
                        suma=0 # Suma todos los nodos de la capa siguiente 
                        for k in range(capas[i+1]):            
                            suma+=errores[k]*pesos[i][j][k]
                        nuevos_errores[j]=suma*sigmoide_derivado(salidas[ind][i][j])

                        # Actualiza los nodos
                        for k in range(capas[i+1]):
                            pesos[i][j][k]+=learning_rate*errores[k]*salidas[ind][i][j]

                    errores = nuevos_errores

                # ENVIA AL ANTERIOR
                comm.send(errores,dest=myrank-1)
                
                # ENVIA FORWARD              
                entrada=comm.recv(source=myrank-1) # Recibe   
                

                #salidas.append([entrada])
                salidas[ind+1]=[entrada]
                # Capas INTERMEDIAS del PROCESO
                for i in range(numCapas-1):
                    entradas_capa=salidas[ind+1][-1]
                    salidas_capa=[0 for _ in range(capas[i+1])]
                    # Recorre todos los nodos de la capa actual
                    for j in range(capas[i+1]):    
                        suma=0
                        # Suma todos los nodos de la capa anterior
                        for k in range(capas[i]):            
                            suma+=entradas_capa[k]*pesos[i][k][j]
                        salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                    
                    salidas[ind+1].append(salidas_capa)
                # Capa que CONECTA con el SIGUIENTE            
                indice=numCapas-1
                entradas_capa=salidas[ind+1][-1]
                
                salidas_capa=[0 for _ in range(capa_siguiente)]
                # Recorre todos los nodos de la capa actual
                for j in range(capa_siguiente):    
                    suma=0 # Suma todos los nodos de la capa anterior
                    for k in range(capas[indice]):            
                        suma+=entradas_capa[k]*pesos[indice][k][j]
                    salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                    
                salidas[ind+1].append(salidas_capa)
                
                # Devuelve el ultimo elemento
                comm.send(salidas[ind+1][-1],dest=myrank+1)            
                


            # BACKPROPAGATION
            errores=comm.recv(source=myrank+1)            
                
            # ACTUALIZA
            indice=numCapas-1
            # PROCESO ACTUAL CON EL QUE HACE BORDE
            nuevos_errores=[0 for _ in range(capas[indice])]            
            for j in range(capas[indice]): # Recorre todos los nodos de la capa que hace borde
                suma=0 # Suma todos los nodos de la capa siguiente (del otro proceso)
                for k in range(capa_siguiente):            
                    suma+=errores[k]*pesos[indice][j][k]
                nuevos_errores[j]=suma*sigmoide_derivado(salidas[tam_entrenamiento-1][indice][j])

                # Actualiza los nodos
                for k in range(capa_siguiente):
                    pesos[indice][j][k]+=learning_rate*errores[k]*salidas[tam_entrenamiento-1][indice][j]
            errores=nuevos_errores
            
            # OTRAS CAPAS DEL PROCESO 
            for i in range(numCapas-2,-1,-1):
                nuevos_errores=[0 for _ in range(capas[i])]
                # Recorre todos los nodos de la capa actual
                for j in range(capas[i]):
                    suma=0 # Suma todos los nodos de la capa siguiente 
                    for k in range(capas[i+1]):            
                        suma+=errores[k]*pesos[i][j][k]
                    nuevos_errores[j]=suma*sigmoide_derivado(salidas[tam_entrenamiento-1][i][j])

                    # Actualiza los nodos
                    for k in range(capas[i+1]):
                        pesos[i][j][k]+=learning_rate*errores[k]*salidas[tam_entrenamiento-1][i][j]

                errores = nuevos_errores

            # ENVIA AL ANTERIOR
            comm.send(errores,dest=myrank-1)
        else: # Worker2 (SALIDA)        

            tam_salida=comm.recv(source=MASTER)
            etiquetas=comm.recv(source=MASTER)
            
            entrada_prueba_IMC=comm.recv(source=MASTER)
            imcD_min=comm.recv(source=MASTER)
            imcD_max=comm.recv(source=MASTER)
            

            for i in range(tam_entrenamiento):            
                data=comm.recv(source=myrank-1) # Recibe float:IMC calculado (TODO mejorar?)
                
                errores=[]
                #for j in range(tam_salida):
                errores.append((etiquetas[i]-data[0])*sigmoide_derivado(data[0]))            
                comm.send(errores,dest=myrank-1)
        
        

        comm.Barrier()
        
    if myrank!=numWorkers:
        print("(DESPUES) ID: {}. pesos={}".format(myrank,pesos))


    
    timePredStart = MPI.Wtime()

    # Prediccion
    if myrank==MASTER: # MASTER (ENTRADA)

        # En todo el entrenamiento se pierde espacio*2 de todas las tam_entrenamiento        
        salidas=[]
        errores=[]
        
        # FORWARD
        for ind in range(entrada_prueba_tam):                                             
            salidas.append([entrada_prueba[ind]])      
            
            # Capas intermedias del MASTER
            for i in range(numCapas-1):
                entradas_capa=salidas[ind][-1]
                salidas_capa=[0 for _ in range(capas[i+1])]                
                # Recorre todos los nodos de la capa actual
                for j in range(capas[i+1]):    
                    suma=0 # Suma todos los nodos de la capa anterior
                    for k in range(capas[i]):            
                        suma+=entradas_capa[k]*pesos[i][k][j]
                    salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                
                salidas[ind].append(salidas_capa)

            # Capa que conecta con el siguiente
            indice=numCapas-1
            entradas_capa=salidas[ind][-1]
            salidas_capa=[0 for _ in range(capa_siguiente)]
            # Recorre todos los nodos de la primera capa del siguiente procesp
            for j in range(capa_siguiente):    
                suma=0 # Suma todos los nodos de la capa actual
                for k in range(capas[indice]):            
                    suma+=entradas_capa[k]*pesos[indice][k][j]
                salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                
            salidas[ind].append(salidas_capa)
            
            # Devuelve el ultimo elemento
            comm.send(salidas[ind][-1],dest=1)
        
        timePredEnd = MPI.Wtime()
        print("Tiempo de Prediccion: {}s\n".format(timePredEnd-timePredStart))
    
    elif myrank!=numProc-1: # Worker1 (OCULTA)
        
        salidas=[]
        errores=[]

        # FORWARD
        for ind in range(entrada_prueba_tam):
            entrada=comm.recv(source=myrank-1) # Recibe                         
            salidas.append([entrada]) 
            # Capas INTERMEDIAS del PROCESO
            for i in range(numCapas-1):
                entradas_capa=salidas[ind][-1]
                salidas_capa=[0 for _ in range(capas[i+1])]
                # Recorre todos los nodos de la capa actual
                for j in range(capas[i+1]):    
                    suma=0 # Suma todos los nodos de la capa anterior
                    for k in range(capas[i]):            
                        suma+=entradas_capa[k]*pesos[i][k][j]
                    salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                
                salidas[ind].append(salidas_capa)
            # Capa que CONECTA con el SIGUIENTE
            indice=numCapas-1
            entradas_capa=salidas[ind][-1]  
            
            salidas_capa=[0 for _ in range(capa_siguiente)]
            # Recorre todos los nodos de la primera capa del siguiente proceso
            for j in range(capa_siguiente):    
                suma=ind # Suma todos los nodos de la capa actual
                for k in range(capas[indice]):                    
                    suma+=entradas_capa[k]*pesos[indice][k][j]
                salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
                
            salidas[0].append(salidas_capa)
            
            # Devuelve el ultimo elemento                
            comm.send(salidas[ind][-1],dest=myrank+1)
    
    else: # Worker2 (SALIDA)for i in range(entrada_prueba_tam):            
        
        for i in range(entrada_prueba_tam):
            data=comm.recv(source=myrank-1) # Recibe float:IMC calculado (TODO mejorar?)
            
            #print(data,imcD_min,imcD_max)
            print(desnormalizar_dato(data[0],imcD_min,imcD_max))
            """print(  f"Altura: {datos_prueba[i][0]:.2f}m. Peso: {datos_prueba[i][1]:.2f}kg. "
                f"IMC Predicho: {prediccion:.3f}. IMC Real: {datos_prueba_IMC[i]:.3f}. Fallo: {abs(prediccion-datos_prueba_IMC[i]):.3f}")"""
            
        
                   
            
        



main()

# Red Neuronal
Basado en la naturaleza, las Redes Neuronales se suelen representar como un cerebro, neuronas interconectadas con otras neuronas,  funcionando como una red. Una trozo de informacion fluye por muchas neuronas para dar una respuesta, como "mueve tu mano derecha".

El proceso en esta red es directa, una variable de entrada, (por ejemplo una fotografia de una playa) que despues de una serie de calculos, devuelve una salida (para el caso anterior devuelve "playa". Puede ser más especifico y devolver el nombre de la playa si ha sido entrenado para reconocer playas)

---

Estas neuronas se __representan por columnas__. Estas neuronas están conectadas con las columnas anteriores y posteriores. Y hay diferentes redes que varían las arquitecturas. Se leen de izquierda a derecha. 
- La primera columna es la capa de entrada de la variable. 
- La última columna es la capa de salida con todas las posibles salidas.
- Las columnas intermedias son las capas ocultas.

![Esquema_red](https://github.com/Danipiza/TFG/assets/98972125/a440fcdd-86fc-4ab0-befe-cf02412b614b)

Cada neurona hace una operación simple. Suma los valores de todas las neuronas de la columna anterior. Estos valores multiplicados por un peso que determina la importancia de conexion entre las dos neuronas. Todas las neuronas conectadas tienen un peso que iran cambiando durante el proceso de aprendizaje.
Ademas, un valor bias puede ser añado al valor calculado. No es un valor que viene de una neurona especifica y se escoge antes de la fase de aprendizaje. Puede ser util para la red.
Con el valor calculado se aplica a una funcion de activacion, para obtener el valor final. Se suele usar para dar un valor entre [0-1].

![Perceptron](https://github.com/Danipiza/TFG/assets/98972125/0bdeadf4-cfe5-4994-90db-79c8cb2a694d)

Cuando todas las neuronas de una columna han terminado se pasa a la siguiente columna. Hasta llegar a la última, con valores que deberian de ser utilizables para determinar la salida deseada.

---

## ¿Como aprende la Red Neuronal?
Hay que preparar un monton de datos para entrenar a la red. Estos datos incluyen la entrada y la salida deseada para la red neuronal.

### Proceso de aprendizaje:
Lo que queremos que haga la red neuronal, es que dado una entrada devuelva una salida. Al principio no va a ser así, solo por suerte devuelve la salida correcta. Por esto se genera la etapa de aprendizaje, en la que cada entrada tiene asociada una etiqueta, para explicar que salida deberia de haber adivinado. 
Si acierta, los parametros actuales se guardan, y se envia la siguiente entrada. 
Si no acierta, es decir, la salida no es igual a la etiqueta dada con la entrada, los pesos son cambiados (mencionado anteriormente que estos valores son los unicos que cambian). Este proceso se puede ver como unas combinaciones que van cambiando cuando la salida es erronea.

Para determinar que peso modificar, se usa un proceso llamado "backpropagation", propagación hacia atrás en español. Como el nombre indica consiste en ir hacia atras en la red e inspeccionar cada conexion para comprobar como hubiera sido la salida con un cambio de peso.

Para finalizar este proceso de aprendizaje, tenemos un parametro para controlar como aprende la red neuronal, la tasa de aprendizaje. Determina la velocidad en la cual la red neuronal aprenderá, más bien, como modificar el peso, poco a poco, o mas rapido. Normalmente se usara 1 como parametro.

---

## EJEMPLO SIMPLE:
Perceptron, fue la primera red neuronal creada, consiste en dos neuronas como entrada una una neurona como salida. Esta configuracion permite crear clasificadores simples para distinguier entre dos grupos. 

Vamos a crear uan red neuronal que devuelva como salida and logica.
- A y B son verdad  -> verdad
- en caso contrario -> falso

Se puede configurar para que verdad sea 1 y falso 0. 
Definición de las librerias y valores inciales
```
import numpy, random, os

tA = 1  	# tasa de aprendizaje
bias = 1 	# valor de bias 
# pesos generados en forma de lista (3 pesos en total para 2 neuronas y bias)
pesos = [random.random(), random.random(), random.random()] 
```

Funcion para definir el trabajo de la neurona de salida. 2 parametros de entrada y la salida deseada. "error" se usa para calcular el cambio de valores de "pesos"
```
def Perceptron(in1, in2, output) :
   ret = in1*pesos[0]+in2*pesos[1]+bias*pesos[2]
   
   if ret > 0 : # Funcion de activacion (Escalon de Heaviside)
      ret = 1
   else :
      ret = 0
	  
   error = output – ret
   pesos[0] += error * in1 * lr
   pesos[1] += error * in2 * lr
   pesos[2] += error * bias * lr
```

Etapa de aprendizaje, el numero de iteraciones es la precision que queremos que tenga la red neuronal. Muchas iteraciones puede llevar a sobre ajuste, y se centra mucho en los casos dados, por lo que no puede acertar en casos que no esten en la etapa de aprendiza.
```
for i in range(50) :
   Perceptron(0,0,0) # falso y falso (falso, salida)
   Perceptron(0,1,0) # falso y verdad (falso, salida)
   Perceptron(1,0,0) # verdad y falso (falso, salida)
   Perceptron(1,1,1) # verdad y verdad(verdad, salida)
```

Comprobar si la red funciona
```
x = int(input())
y = int(input())
query = x*pesos[0] + y*pesos[1] + bias*pesos[2]
if query > 0 : #activation function
   query = 1
else :
   query = 0
print(x, " or ", y, " is : ", query)
```



[INFO](https://towardsdatascience.com/first-neural-network-for-beginners-explained-with-code-4cfd37e06eaf)
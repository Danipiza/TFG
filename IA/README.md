# Aprendizaje Automático

## Aprendizaje no supervisado
- Algoritmos de agrupamiento jerárquico
- Algoritmos de agrupamiento basado en particiones
## Aprendizaje supervisado
- k vecinos más cercanos
- Árboles de decisión
- Perceptrón multicapa

La __capacidad de aprendizaje__ permite realizar nuevas tareas que previamente no podían realizarse, o bien realizar mejor (más rápidamente, con mayor exactitud, etc.) las que ya se realizaban, como resultado de los cambios producidos en el sistema al resolver problemas anteriores.

__La capacidad de aprendizaje no puede añadirse a posteriori.__


La __IA simbólica__ trata con representaciones simbólicas de alto nivel (cercanas al entendimiento humano). Adecuada para:
- Representar conocimiento humano y razonar con él
- Resolver problemas bien-definidos o de índole lógica

La __IA subsimbólica__ es capaz de tratar con representaciones cercanas al problema y extraer conocimiento de ellas.

## Aprendizaje Automático (machine learning) e IA subsimbólica
En el aprendizaje automático, mediante algoritmos de aprendizaje se extraen “reglas” o “patrones” de los datos. Las aproximaciones de aprendizaje subsimbólico proporcionan
- Mayor robustez frente al ruido
- Mayor capacidad de escalamiento (nuevos ejemplos o nuevas variables)
- Mayor capacidad para trabajar con cantidades ingentes de datos
- Menor dependencia del experto

__Aprendizaje supervisado:__ Hay que suministrar al sistema ejemplos clasificados. El objetivo es descubrir "reglas" de clasificación 

__Aprendizaje no supervisado__ o por descubrimiento: No hay información sobre la clase a la que pertenecen los ejemplos. Objetivo: descubrir patrones en el conjunto de entrenamiento que permitan agrupar y diferenciar unos ejemplos de otros

### Representación de los individuos
Partimos de datos que son un conjunto de descripciones de objetos. Tendremos un número de individuos o elementos (n) descrito por un conjunto de variables (m).

Los datos se representan en forma de matriz 𝒏𝒏 × 𝒎𝒎 donde las filas son los individuos y las columnas las variables
- Variable Cuantitativa: variables reales o enteras
- Variable Cualitativa: variables categóricas u ordinales (p.ej. grupos de edad)

![Representacion_Individuos](https://github.com/Danipiza/TFG/assets/98972125/20d52cd6-40df-4873-9ba0-d791fca48396)

Si tenemos 3 variables cuantitativas nuestros individuos pueden considerarse como puntos en un espacio tridimensional

Los individuos son puntos representados en un espacio m-dimensional 

Suele ser de gran ayuda poder inspeccionar los datos visualmente, para ello se suele utilizar el diagrama de dispersión (scatter plot en inglés)

No podemos ver mas de 3 dimensiones, para ello mostramos diagramas de dispersion 2 a 2, si no son demasiadas variables.

![Diagrama_dispersion_+3variables](https://github.com/Danipiza/TFG/assets/98972125/d6e2340a-95cd-40b3-ab5d-70311ca92b2e)

Los algoritmos de Aprendizaje Automático son sensibles a la forma en que los individuos de nuestro problema están representados. 
Las variables redundantes o no relevantes para el problema, empeoran la clasificación, por esto puede producirse ruido, errores de medidad, valores perdidos. No siempre se puede determinar apriori que variables no son relevantes.

Los algoritmos de aprendizaje automático trabajan bien cuando el conjunto de datos tiene numerosos individuos que cubren bien la casuística que se puede dar en la vida real. Pero si hay regiones en el espacion sin individuos es complicado aprender nuevas cosas.

## Preparando los datos para el análisis
Es una tarea crucial que afecta a los resultados, aunque no ahondaremos en ello. Incluye operaciones como:

### Selección de variables relevantes para el problema
- Transformación de variables iniciales
```
Cambiar la escala, normalizando
-> escalar => x'=(x-xMin)/(xMax-xMin) o estandarizar 
Discretizar una variable numérica, es decir, dividir su rango de valores posibles en categorías ordenadas
-> Edad: [0 – 100] ➔ Bebé, Niño, Adolescente, Joven, Adulto, Anciano
Transformación de variables categóricas en variables binarias. Hombre: 0 Mujer: 1
```
- Combinación de variables iniciales(ej. Agrupando aquellas variables que están muy correlacionadas)
- Eliminación de variables no relevantes o redundantes

### Tratamiento de valores perdidas 
- Eliminar la fila para el individuo
- Relleñar los valores perdidos con el valor medio o modal de todos los individuos

## Entendiendo los datos a procesar
Antes de acometer una tarea de aprendizaje automático conviene entender los datos lo mejor posible, para ello suele ser recomendable "trabajarlos" previamente.
- Visualización de datos:

Permite determinar qué variables están más relacionadas entre sí y cuál es la naturaleza de la relación (lineal, exponencial, etc)

En los problemas de clasificación permite ver cómo de bien se separan las clases y qué variables separan mejor

- Calcular estadísticos descriptivos:

Tendencia central: media, mediana, moda

Dispersión: desviación típica, valores mínimos y máximos, percentiles

Bivariantes: coeficiente de correlación o tablas de contingencia

- Representar la distribución de las variables

Observar valores más frecuentes y valores extremos (¿tienen sentido o son aberrantes?)



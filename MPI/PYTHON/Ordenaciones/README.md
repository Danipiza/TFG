## Ordenaciones
Todas las ordenaciones son ascendentes. Están implementadas sin recursion ni llamadas a otras funciones para que sean lo más eficientes posibles.

---

### BubbleSort
Recorre el array de izquierda a derechas, comparando cada elemento adyacente. Si el elemento siguiente al actual es menor, se hace un __swap()__, intercambiando sus valores. 

``` 
n = len(a)
for i in range(n-1):
    for j in range(n-1-i):
        if a[j] > a[j+1]:
            tmp = a[j]
            a[j] = a[j+1]
            a[j+1] = tmp
```

__Caso Peor:__ si el array esta ordenado de manera descendente, tiene que hacer (N-1)*((N-1)/2) _swaps()_.

__Coste Temporal O(N^2)__

__Coste Espacial O(1)__


### InsertionSort
Recorre el array de izquierda a derechas, comparando el elemento actual con la parte izquierda ya procesada, moviendo hacia la izquierda el elemento hasta que no sea menor.

```
n = len(a)
for i in range(1, n):
    if a[i-1] > a[i]:                
        pos=i
        tmp = a[pos]
        while pos > 0 and tmp < a[pos-1]:
            a[pos] = a[pos-1]
            pos -= 1
        a[pos] = tmp
```

__Caso Peor:__ si el array esta ordenado de manera descendente, tiene que hacer ((N-1)/2)*(N-1) _swaps()_. Este algoritmo es parecido al anterior pero el numero de comparaciones va aumentando, conforme procesa el array.

__Coste Temporal O(N^2)__

__Coste Espacial O(1)__


### SelectionSort
Recorre el array de izquierda a derechas. En cada iteración recorre la parte no procesada y compara los elementos, guardando el de menor valor para ponerlo en la primera posición de la parte no procesada.

```
n = len(a)
minE = 0
pos = 0
for i in range(n-1):
    minE = a[i]
    pos = i
    for j in range(i+1, n):
        if minE > a[j]:
            minE = a[j]
            pos = j            
    tmp = a[i]
    a[i] = a[pos]
    a[pos] = tmp
```

__Caso Peor:__ si el array esta ordenado de manera descendente, tiene que hacer (N-1)*((N-1)/2) comparaciones, todas evaluadas a True.

__Coste Temporal O(N^2)__

__Coste Espacial O(1)__

### SequentialSort
Recorre el array N veces (1 por cada elemento) recorriendo el array de izquierda a derecha, comparando el valor actual con todo el array, para que cuando termine, colocarlo en que posición del array ordenado.

```
for i in range(n):
cont=0
val=a[i]
for i in range(n):  
    if a[i]<val: cont+=1
while b[cont]!=INF: cont+=1
b[cont]=val
```

Si el elemento siguiente al actual es menor, se hace un __swap()__, intercambiando sus valores. 

__Caso Peor:__ si el array esta ordenado de manera descendente, tiene que hacer N*N comparaciones

__Coste Temporal O(N^2)__

__Coste Espacial O(N)__

## Pruebas
N:100000 ordenados de manera descendente

O(N^2)
- BubbleSort:           517.9079863999978s
- InsertionSort:        339.88781240000026s
- SelectionSort:        141.95964079999976s    
- SequentialSort:       429.5713084000017s
- MPI SequentialSort:   50.1617846100001s

__SpeedUp:__ SequentialSort/SequentialSortMPI = 8.56

O(NlogN)
- QuickSort:            RecursionError: maximum recursion depth exceeded in comparison
- MergeSort:            20.67818360000092s
- MPI MergeSort:         1.149167099996702s

__SpeedUp:__ MergeSort/MergeSortMPI = 17.994 ≈ 18
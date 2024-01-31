from concurrent.futures import ThreadPoolExecutor

def BinarySearch(a, x, i, j):
    while i <= j:
        m = (i + j) // 2  
        if a[m] == x: return m            # encontrado
        elif a[m] < x: i = m + 1          # derecha
        else: j = m - 1                   # izquierda
    return -1  


def ParallelBinarySearch(a, x, hilos=2):
    # Divide el trabajo entre los hilos
    tamHilo = len(a)//2 

	# lista con las tuplas de los rangos para buscar para los hilos
    rangos = [(i * tamHilo, (i + 1) * tamHilo) for i in range(hilos)]

    with ThreadPoolExecutor(max_workers=hilos) as executor:
        futures = [executor.submit(BinarySearch, a, x, start, end) for (start, end) in rangos]

    # resultados de los hilos
    retHilos = [future.result() for future in futures]

    # Busca la posicion del hilo
    for i, ret in enumerate(retHilos):
        if ret != -1: return ret + i * tamHilo

    return -1

# Uso del ejemplo
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
x = 8
ret = ParallelBinarySearch(a, x)
print(f"El elemento {x} esta en la posicion {ret}" if ret!=-1 else "Elemento no esta en el array")
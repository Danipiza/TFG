def binary_search(a, x, i, j):
    while i <= j:
        m = (i + j) // 2  
        if a[m] == x: return m            # encontrado
        elif a[m] < x: i = m + 1          # derecha
        else: j = m - 1                   # izquierda
    return -1  
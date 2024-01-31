def SequentialSearch(a, x, i, j):
    while i <= j:
        if a[i] == x: return i            # encontrado
        i+=1
    return -1 
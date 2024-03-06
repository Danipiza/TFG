class MergeSort:
    def merge(self, a, izq, m, der):
        i = izq
        j = m + 1
        k = izq
        aux = [0] * len(a)
        for i in range(izq, der+1):
            aux[i] = a[i]

        i = izq

        while i <= m and j <= der:
            if aux[i] <= aux[j]:
                a[k] = aux[i]
                i += 1
            else:
                a[k] = aux[j]
                j += 1
            k += 1

        while i <= m:
            a[k] = aux[i]
            k += 1
            i += 1

        while j <= der:
            a[k] = aux[j]
            k += 1
            j += 1

    def mergesort(self, a, izq, der):
        if izq < der:
            m = (izq + der) // 2
            self.mergesort(a, izq, m)
            self.mergesort(a, m+1, der)
            self.merge(a, izq, m, der)

class BubbleSort:
    def swap(self, a, pos):
        tmp = a[pos]
        a[pos] = a[pos+1]
        a[pos+1] = tmp

    def sort(self, a):
        n = len(a)
        for i in range(n-1):
            for j in range(n-1-i):
                if a[j] > a[j+1]:
                    self.swap(a, j)

class InsertionSort:
    def mueve(self, a, pos):
        tmp = a[pos]
        while pos > 0 and tmp < a[pos-1]:
            a[pos] = a[pos-1]
            pos -= 1
        a[pos] = tmp

    def sort(self, a):
        n = len(a)
        for i in range(1, n):
            if a[i-1] > a[i]:
                self.mueve(a, i)

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

class QuickSort:
    def particion(self, a, izq, der):
        pivote = a[der]
        posPivote = der
        der -= 1
        eIzq = a[izq]
        eDer = a[der]
        tmp = 0
        while izq < der:
            while eIzq < pivote:
                izq += 1
                eIzq = a[izq]
            while eDer > pivote and izq < der:
                der -= 1
                eDer = a[der]
            if izq < der:
                # swap
                tmp = a[izq]
                a[izq] = a[der]
                a[der] = tmp
                # aumenta los punteros
                izq += 1
                eIzq = a[izq]
                der -= 1
                eDer = a[der]
                if izq == der:
                    izq += 1
        # swap
        a[posPivote] = a[izq]
        a[izq] = pivote
        return izq

    def sort(self, a, izq, der):
        if izq < der:
            pInd = self.particion(a, izq, der)
            self.sort(a, izq, pInd - 1)
            self.sort(a, pInd + 1, der)

class SelectionSort:
    def swap(self, a, i, j):
        tmp = a[i]
        a[i] = a[j]
        a[j] = tmp

    def sort(self, a):
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
            self.swap(a, i, pos)





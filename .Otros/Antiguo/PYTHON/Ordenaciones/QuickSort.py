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

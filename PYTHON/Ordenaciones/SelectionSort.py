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


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

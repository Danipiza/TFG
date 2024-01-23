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

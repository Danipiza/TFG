import random


class Gen:
    def __init__(self, l, v):
        self.v = []

        if v is not None:
            for a in v:
                self.v.append(a)
        else:
            for i in range(l):
                self.v.append(random.randint(0, 1))

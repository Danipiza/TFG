import random


class Gen:
    def __init__(self, l, v):
        self.v = []

        if v is not None:
            self.v=[(v[i]) for i in range(len(v))]
            #for a in v:
            #   self.v.append(a)
        else:
            self.v=[(random.randint(0,1)) for i in range(l)]
            #for i in range(l):
            #    self.v.append(random.randint(0, 1))

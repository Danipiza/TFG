import random
import math

class Gen:
    def __init__(self, l=None, gen=None):
        if gen is not None:
            self.v = gen.v[:]
        elif l is not None:
            self.v = [random.randint(0, 1) for _ in range(l)]

class Individuo:
    def __init__(self, num=None, tam_genes=None, xMax=None, xMin=None, poblacion=None):
        if poblacion is not None:
            num = len(poblacion.genes)
            self.genes = [Gen(gen=c) for c in poblacion.genes]
        else:
            self.genes = [Gen(l=l) for l in tam_genes]
            self.fenotipo = [0] * num
            self.fitness = 0

    def bin2dec(self, gen):
        ret = 0
        cont = 1
        for i in range(len(gen.v) - 1, -1, -1):
            if gen.v[i] == 1:
                ret += cont
            cont *= 2
        return ret

    def calcular_fenotipo(self, xMax, xMin):
        for i in range(len(self.genes)):
            self.fenotipo[i] = self.calcular_fenotipo_cromosoma(self.genes[i], xMax[i], xMin[i])

    def calcular_fenotipo_cromosoma(self, ind, xMax, xMin):
        return xMin + self.bin2dec(ind) * ((xMax - xMin) / (2 ** len(ind.v) - 1))

    def print_individuo(self):
        for c in self.genes:
            for a in c.v:
                print(a, end=' ')
        print("fenotipo x1:", self.fenotipo[0], "fenotipo x2:", self.fenotipo[1])

def tam_genes():
    ret = []
    for i in range(num_genes):
        ret.append(tam_gen(precision, minimos[i], maximos[i]))
    return ret

def tam_gen(precision, min_val, max_val):
    return math.ceil((math.log10(((max_val - min_val) / precision) + 1) / math.log10(2)))

def init_poblacion():
    global poblacion
    poblacion = [Individuo(num_genes, tam_genes, maximos, minimos) for _ in range(tam_poblacion)]

def fitness(nums):
    return (nums[0] ** 2 + 2 * nums[1] ** 2)

def evaluacion_poblacion():
    global fitness_total, mejor_total
    fitness_total = 0
    mejor_generacion = float('-inf')

    for ind in poblacion:
        ind.calcular_fenotipo(maximos, minimos)
        fit = fitness(ind.fenotipo)
        ind.fitness = fit
        fitness_total += fit
        mejor_generacion = max(mejor_generacion, fit)

    mejor_total = max(mejor_total, mejor_generacion)

def seleccion_poblacion(tam_seleccionados, k):
    seleccionados = []

    for _ in range(tam_seleccionados):
        max_fitness = float('-inf')
        index_max = -1
        for _ in range(k):
            random_index = random.randint(0, tam_poblacion - 1)
            random_fitness = poblacion[random_index].fitness
            if random_fitness > max_fitness:
                max_fitness = random_fitness
                index_max = random_index
        seleccionados.append(Individuo(poblacion[index_max]))

    return seleccionados

def cruce_poblacion(selec):
    n = len(selec)
    ret = []

    if n % 2 == 1:
        ret.append(selec[-1])
        n -= 1

    long_genes = [len(selec[0].genes[i].v) for i in range(len(selec[0].genes))]
    corte_maximo = sum(long_genes) - 1
    i = 0
    while i < n:
        ind1 = Individuo(selec[i])
        ind2 = Individuo(selec[i + 1])

        if random.random() < prob_cruce:
            corte = random.randint(1, corte_maximo)
            cont = 0
            j = 0
            for k in range(corte):
                tmp = ind1.genes[cont].v[j]
                ind1.genes[cont].v[j] = ind2.genes[cont].v[j]
                ind2.genes[cont].v[j] = tmp
                j += 1
                if j == long_genes[cont]:
                    cont += 1
                    j = 0

        ret.extend([ind1, ind2])
        i += 2

    return ret

def mutacion_poblacion():
    ret = []

    for ind in poblacion:
        act = Individuo(ind)
        for c in range(len(ind.genes)):
            for j in range(len(ind.genes[c].v)):
                if random.random() < prob_mut:
                    act.genes[c].v[j] = (act.genes[c].v[j] + 1) % 2
        ret.append(act)

    return ret

def set_valores():
    global tam_poblacion, generaciones, prob_cruce, prob_mut, precision, maximos, minimos, num_genes, tam_genes, mejor_total
    tam_poblacion = 100
    generaciones = 10
    prob_cruce = 0.6
    prob_mut = 0.05
    precision = 0.01

    maximos = [10, 10]
    minimos = [-10, -10]

    num_genes = 2
    tam_genes = tam_genes()

    mejor_total = float('-inf')

def ejecuta():
    #set_valores()
    global tam_poblacion, generaciones, prob_cruce, prob_mut, precision, maximos, minimos, num_genes, tam_genes, mejor_total
    tam_poblacion = 100
    generaciones = 10
    prob_cruce = 0.6
    prob_mut = 0.05
    precision = 0.01

    maximos = [10, 10]
    minimos = [-10, -10]

    num_genes = 2
    tam_genes = tam_genes()

    mejor_total = float('-inf')
    init_poblacion()
    evaluacion_poblacion()

    while generaciones != 0:
        selec = seleccion_poblacion(tam_poblacion, 5)
        poblacion = cruce_poblacion(selec)
        poblacion = mutacion_poblacion()
        evaluacion_poblacion()
        generaciones -= 1

    print(mejor_total)



if __name__ == "__main__":
    ejecuta()

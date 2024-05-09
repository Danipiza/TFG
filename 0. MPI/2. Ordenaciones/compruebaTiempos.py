



def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        numeros = [float(numero.replace(',', '.')) for linea in archivo for numero in linea.strip().split(',')]
    return numeros

def division_elemento_por_elemento(lista1, lista2):
    ret=[]
    for a, b in zip(lista1, lista2):
        if b!=0: ret.append(a/b) # GARANTIZA QUE NO SE DIVIDA POR CERO
        else: ret.append(float('inf'))  # INF AL DIVIDIR POR CERO

    return ret

def main():
    PRINT=False

    archivo1="BubbleSort.txt"
    archivo2="SelectionSort.txt"

    try:
        a1=leer_archivo(archivo1)
        a2=leer_archivo(archivo2)

        ret = division_elemento_por_elemento(a1, a2)

        # Imprime el resultado
        print("Resultado de la división elemento por elemento:")
        maxV=0
        for val in ret:
            if maxV<val:maxV=val
            if PRINT: print(val)

    except FileNotFoundError:
        print("No se pudo encontrar uno de los archivos.")
    except ValueError:
        print("Los archivos contienen datos no válidos.")

if __name__ == "__main__":
    main()



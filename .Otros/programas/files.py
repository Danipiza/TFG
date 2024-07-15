



def leeArchivo(archivo):
    with open(archivo, 'r') as file:
        content = file.read()
    float_list = [float(x.strip()) for x in content.split(',')]
    return float_list

def escribeArchivo(entrada, salida):
    float_lists = []
    for archivo in entrada:
        float_lists.append(leeArchivo(archivo))
    
    with open(salida, 'w') as outfile:
        length = min(len(float_list) for float_list in float_lists)
        for i in range(length):
            line = ' '.join(str(float_list[i]) for float_list in float_lists)
            outfile.write(f"{line}\n")

def write_converged_file3D(entrada, salida, D):    
    float_lists = [[] for _ in range(3)]
    
    cont=0
    for archivo in entrada:
        float_lists[cont]=(leeArchivo(archivo))
        cont=2
    
    float_lists[1]=[D for _ in range(len(float_lists[0]))]
    
    with open(salida, 'w') as outfile:        
        length = min(len(float_list) for float_list in float_lists)
        for i in range(length):
            line = ' '.join(str(float_list[i]) for float_list in float_lists)
            outfile.write(f"{line}\n")


entrada = ['TamDatos.txt','AglomerativoC_MPI20.txt', 'AglomerativoC_MPI50.txt','AglomerativoC_MPI75.txt','AglomerativoC_MPI100.txt','AglomerativoC_MPI128.txt']
salida = 'a.txt'

escribeArchivo(entrada, salida)

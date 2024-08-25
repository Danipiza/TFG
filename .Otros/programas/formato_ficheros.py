


def div(input_file, output_file, divisor):
    with open(input_file, 'r') as file:
        lines=file.readlines()
    
    with open(output_file, 'w') as file:
        for line in lines:
            numbers=list(map(float, line.split()))
            
            if numbers: numbers[0]/=divisor
            file.write(' '.join(map(str, numbers)) + '\n')

def mul(input_file, output_file, mult):
    with open(input_file, 'r') as file:
        lines=file.readlines()
    
    with open(output_file, 'w') as file:
        for line in lines:
            numbers=list(map(float, line.split()))

            numbers[0]*=mult            
            file.write(' '.join(map(str, numbers)) + '\n')

def main():
    input_files=['kmedias.txt','kmedias_speedup.txt','knn.txt','knn_speedup.txt','redneu1.txt','redneu2.txt']
    divisor=10000  
    mult=10

    for input in input_files:
        #mul(input, input[0:-4]+"_.txt", divisor)
        mul(input, input[0:-4]+"_.txt", mult)


main()
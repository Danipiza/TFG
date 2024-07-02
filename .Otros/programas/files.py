def read_floats_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    # Convert the comma-separated string to a list of floats
    float_list = [float(x.strip()) for x in content.split(',')]
    return float_list

def write_converged_file(input_files, output_file):
    # Read the floats from each input file
    float_lists = []
    for filename in input_files:
        float_lists.append(read_floats_from_file(filename))
    
    # Open the output file for writing
    with open(output_file, 'w') as outfile:
        # Ensure all files have the same length
        length = min(len(float_list) for float_list in float_lists)
        for i in range(length):
            # Write the corresponding elements from each file
            line = ' '.join(str(float_list[i]) for float_list in float_lists)
            outfile.write(f"{line}\n")

def write_converged_file3D(input_files, output_file, D):
    # Read the floats from each input file
    float_lists = [[] for _ in range(3)]
    
    cont=0
    for filename in input_files:
        float_lists[cont]=(read_floats_from_file(filename))
        cont=2
    
    float_lists[1]=[D for _ in range(len(float_lists[0]))]
    # Open the output file for writing
    with open(output_file, 'w') as outfile:
        # Ensure all files have the same length
        length = min(len(float_list) for float_list in float_lists)
        for i in range(length):
            # Write the corresponding elements from each file
            line = ' '.join(str(float_list[i]) for float_list in float_lists)
            outfile.write(f"{line}\n")

# Usage
input_files = ['TamDatos.txt','Mul_Matriz_MPI16.txt', 'Mul_Matriz_MPI32.txt','Mul_Matriz_MPI64.txt','Mul_Matriz_MPI128.txt']
output_file = 'mult.txt'

write_converged_file(input_files, output_file)

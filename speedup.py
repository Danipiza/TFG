def read_input(file_path):
    with open(file_path, 'r') as file:
        data = file.read().strip().split(',')
    return [float(num.strip()) for num in data]

def calculate_speedup(input_file1, input_file2, output_file, ideal_speed_file, p):
    data1 = read_input(input_file1)
    data2 = read_input(input_file2)

    speedup = [str(data1[i] / data2[i]) for i in range(len(data1))]

    with open(output_file, 'w') as file:
        file.write(', '.join(speedup))

    ideal=[p for _ in range(len(speedup))]
    with open(ideal_speed_file, 'w') as file:
        file.write(str(ideal))


if __name__ == "__main__":
    processors=4
    input_file1 = "M100X100.txt"
    input_file2 = "M100X100_2MPI({}).txt".format(processors)
    output_file = "arb.txt"
    ideal_speed_file = "ideal_speed.txt"
    
    calculate_speedup(input_file1, input_file2, output_file, ideal_speed_file, processors)
    

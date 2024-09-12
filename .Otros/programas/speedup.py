def read_input(file_path):
    with open(file_path, 'r') as file:
        data=file.read().strip().split(',')

    return [float(num.strip()) for num in data]

def calculate_speedup(in_f1, in_f2, out_f, ideal_speed_file, p):
    data1=read_input(in_f1)
    data2=read_input(in_f2)

    speedup=[str(data1[i] / data2[i]) for i in range(len(data1))]

    with open(out_f, 'w') as file:
        file.write(', '.join(speedup))

    ideal=[p for _ in range(len(speedup))]
    with open(ideal_speed_file, 'w') as file:
        file.write(str(ideal))


if __name__ == "__main__":
    processors=4
    in_f1="M100X100.txt"
    in_f2="M100X100_2MPI({}).txt".format(processors)
    out_f="arb.txt"
    ideal_speed_file="ideal_speed.txt"
    
    calculate_speedup(in_f1, in_f2, out_f, ideal_speed_file, processors)
    

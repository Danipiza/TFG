def multiplicar_contenido(input_file, output_file, multiplicador):
    try:
        with open(input_file, 'r') as f_input:
            with open(output_file, 'w') as f_output:
                for line in f_input:
                    try:
                        numeros = [float(num.strip()) for num in line.split(',')]
                        resultados = [num * multiplicador for num in numeros]
                        resultados_formateados = ", ".join([f"{resultado:.10f}" for resultado in resultados])
                        f_output.write(f"{resultados_formateados}\n")
                    except ValueError:
                        print(f"Error: No se pudieron convertir los números en '{line.strip()}' a números.")
    except FileNotFoundError:
        print("Error: El archivo de entrada no existe.")

# Ejemplo de uso
if __name__ == "__main__":
    archivo_entrada = "ent3.txt"
    archivo_salida = "AER3_3MPI(4).txt"
    valor_multiplicador = 4  # Puedes cambiar este valor según tu necesidad
    
    multiplicar_contenido(archivo_entrada, archivo_salida, valor_multiplicador)

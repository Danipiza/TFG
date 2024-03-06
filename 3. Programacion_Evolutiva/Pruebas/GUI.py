import tkinter as tk
from tkinter import ttk

def calculate():
    # Retrieve values from text fields and perform calculation
    value1 = float(entry1.get())
    value2 = float(entry2.get())
    result = value1 + value2
    # Update the result label
    result_label.config(text="Valor Optimo: " + str(result))
    #result_label.config(text="Peor: " + str(0))

# Create the main application window
root = tk.Tk()
root.title("Simple Calculator")

# Set the size of the window
root.geometry("800x600")

# Create and place the entry fields with default values
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)
entry1.insert(0, "100")  # Default value for entry1
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1)
entry2.insert(0, "100")  # Default value for entry2

# Create and place labels
tk.Label(root, text="Poblacion:").grid(row=0, column=0)
tk.Label(root, text="Generaciones:").grid(row=1, column=0)
result_label = tk.Label(root, text="Valor Optimo: ")
result_label.grid(row=2, columnspan=2)

# Create and place buttons
calculate_button = tk.Button(root, text="Run", command=calculate)
calculate_button.grid(row=3, columnspan=2)

# Start the GUI application
root.mainloop()

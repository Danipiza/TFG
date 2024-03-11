import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np

def calculate_sum():
    # Get the values from the text fields
    value1 = float(text_field1.get())
    value2 = float(text_field2.get())
    value3 = float(text_field3.get())
    
    # Calculate the sum
    total = value1 + value2 + value3
    
    # Display the sum in the GUI
    sum_label.config(text="Sum: {:.2f}".format(total))
    
    # Get the selected options from the comboboxes
    selected_option1 = combo_box1.get()
    selected_option2 = combo_box2.get()
    selected_option3 = combo_box3.get()
    
    # Display the selected options in the GUI
    selected_options_label.config(text=f"Selected options: {selected_option1}, {selected_option2}, {selected_option3}")
    
    # Plot the function
    plot_function(value1, value2)

def plot_function(a, b):
    x = np.linspace(0, 10, 100)
    y = 2 * x**2 + b
    
    ax.clear()
    ax.plot(x, y)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('2*x^2 + y')
    canvas.draw()

# Create the main window
root = tk.Tk()
root.title("GUI Example")

# Create and place the widgets
text_field1 = ttk.Entry(root)
text_field1.pack()

text_field2 = ttk.Entry(root)
text_field2.pack()

text_field3 = ttk.Entry(root)
text_field3.pack()

combo_box1 = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"])
combo_box1.pack()

combo_box2 = ttk.Combobox(root, values=["Option A", "Option B", "Option C"])
combo_box2.pack()

combo_box3 = ttk.Combobox(root, values=["Choice X", "Choice Y", "Choice Z"])
combo_box3.pack()

calculate_button = ttk.Button(root, text="Calculate", command=calculate_sum)
calculate_button.pack()

sum_label = ttk.Label(root, text="")
sum_label.pack()

selected_options_label = ttk.Label(root, text="")
selected_options_label.pack()

# Add the matplotlib plot
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Run the application
root.mainloop()

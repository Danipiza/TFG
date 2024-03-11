import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PlotterApp:
    def __init__(self, master):
        self.master = master
        master.title("Plotter")

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.plot_area = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button = ttk.Button(master, text="Plot", command=self.plot)
        self.button.pack()

    def plot(self):
        # Clear previous plot
        self.plot_area.clear()

        # Generate some sample data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        # Plot the data
        self.plot_area.plot(x, y)
        self.plot_area.set_title('Sine Wave')
        self.plot_area.set_xlabel('X')
        self.plot_area.set_ylabel('Y')

        # Refresh canvas
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = PlotterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

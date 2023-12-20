import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import sqrt, sin, cos, tan, pi
import sympy as sp

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(root, textvariable=self.entry_var, font=('Arial', 16), justify='right')
        self.entry.grid(row=0, column=0, columnspan=5, sticky='nsew')

        buttons = [
            '7', '8', '9', '/', 'sqrt',
            '4', '5', '6', '*', 'sin',
            '1', '2', '3', '-', 'cos',
            '0', '.', '=', '+', 'tan',
            '(', ')', 'C', 'AC', '^',
            'log', 'exp', 'pi', 'abs', 'matrix',
            'plot', 'clear_plot', 'x', 'y', 'solve_eq'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            ttk.Button(root, text=button, command=lambda b=button: self.on_button_click(b)).grid(row=row_val, column=col_val, sticky='nsew')
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

        # Configure row and column weights
        for i in range(7):
            root.grid_rowconfigure(i, weight=1)
            root.grid_columnconfigure(i, weight=1)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=5, rowspan=7, sticky='nsew')

    def on_button_click(self, button):
        current_text = self.entry_var.get()

        if button == '=':
            try:
                result = eval(current_text)
                self.entry_var.set(result)
            except Exception as e:
                self.entry_var.set("Error")

        elif button == 'C':
            self.entry_var.set(current_text[:-1])

        elif button == 'AC':
            self.entry_var.set("")

        elif button == 'sqrt':
            self.entry_var.set(str(sqrt(eval(current_text))))

        elif button == '^':
            self.entry_var.set(current_text + '**')

        elif button == 'sin':
            self.entry_var.set(str(sin(eval(current_text))))

        elif button == 'cos':
            self.entry_var.set(str(cos(eval(current_text))))

        elif button == 'tan':
            self.entry_var.set(str(tan(eval(current_text))))

        elif button == 'log':
            self.entry_var.set(str(np.log10(eval(current_text))))

        elif button == 'exp':
            self.entry_var.set(str(np.exp(eval(current_text))))

        elif button == 'pi':
            self.entry_var.set(current_text + str(np.pi))

        elif button == 'abs':
            self.entry_var.set(str(abs(eval(current_text))))

        elif button == 'matrix':
            self.create_matrix_window()

        elif button == 'plot':
            self.plot_graph()

        elif button == 'clear_plot':
            self.clear_plot()

        elif button == 'x':
            self.entry_var.set(current_text + 'x')

        elif button == 'y':
            self.entry_var.set(current_text + 'y')

        elif button == 'solve_eq':
            self.solve_equation()

        else:
            self.entry_var.set(current_text + button)

    def create_matrix_window(self):
        matrix_window = tk.Toplevel(self.root)
        matrix_window.title("Matrix Calculator")

        ttk.Label(matrix_window, text="Enter matrix A (comma separated values):").pack()
        entry_matrix_a = ttk.Entry(matrix_window)
        entry_matrix_a.pack()

        ttk.Label(matrix_window, text="Enter matrix B (comma separated values):").pack()
        entry_matrix_b = ttk.Entry(matrix_window)
        entry_matrix_b.pack()

        result_label = ttk.Label(matrix_window, text="")
        result_label.pack()

        def calculate_matrix():
            try:
                matrix_a = np.array([list(map(float, row.split(','))) for row in entry_matrix_a.get().split(';')])
                matrix_b = np.array([list(map(float, row.split(','))) for row in entry_matrix_b.get().split(';')])
                result = np.dot(matrix_a, matrix_b)
                result_label.config(text=f"Result: \n{result}")
            except Exception as e:
                result_label.config(text="Error")

        ttk.Button(matrix_window, text="Calculate", command=calculate_matrix).pack()

    def plot_graph(self):
        try:
            x = np.linspace(-10, 10, 100)
            y = eval(self.entry_var.get().replace('x', 'np.array(x)').replace('y', 'np.array(y)'))
            self.ax.plot(x, y)
            self.canvas.draw()
        except Exception as e:
            self.entry_var.set("Error plotting")

    def clear_plot(self):
        self.ax.clear()
        self.canvas.draw()

    def solve_equation(self):
        try:
            equation = self.entry_var.get()
            x, y = sp.symbols('x y')
            solution = sp.solve(equation, (x, y))
            self.entry_var.set(f"Solutions: {solution}")
        except Exception as e:
            self.entry_var.set("Error solving equation")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

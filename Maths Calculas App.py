import tkinter as tk
from tkinter import ttk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 150
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Functions to compute intercepts, asymptotes, domain, range, extrema, and inflection points
def find_x_intercepts(func, x):
    return sp.solve(func, x)

def find_y_intercept(func, x):
    return func.subs(x, 0)

def find_vertical_asymptotes(func, x):
    vertical_asymptotes = sp.solve(sp.denom(func), x)
    return vertical_asymptotes

def find_horizontal_asymptotes(func, x):
    limit_plus_inf = sp.limit(func, x, sp.oo)
    limit_minus_inf = sp.limit(func, x, -sp.oo)
    return (limit_minus_inf, limit_plus_inf)

def find_slant_asymptote(func, x):
    if sp.degree(sp.numer(func), x) == sp.degree(sp.denom(func), x) + 1:
        quotient, remainder = sp.div(sp.numer(func), sp.denom(func))
        return quotient
    return None

def find_extrema(func, x):
    derivative = sp.diff(func, x)
    critical_points = sp.solve(derivative, x)
    extrema = []
    for point in critical_points:
        if sp.diff(derivative, x).subs(x, point) != 0:
            extrema.append((point, func.subs(x, point)))
    return extrema

def find_inflection_points(func, x):
    second_derivative = sp.diff(func, x, 2)
    inflection_points = sp.solve(second_derivative, x)
    return [(pt, func.subs(x, pt)) for pt in inflection_points]

def plot_function(func_str, min_x=-10, max_x=10, min_range=None, max_range=None):
    x = sp.symbols('x')
    func = sp.sympify(func_str)
    
    x_vals = np.linspace(float(min_x), float(max_x), 400)
    y_vals = [float(func.subs(x, val)) for val in x_vals]

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label=f'{func_str}')
    
    # Shade the area under the curve between min_range and max_range
    if min_range is not None and max_range is not None:
        x_shade = np.linspace(float(min_range), float(max_range), 400)
        y_shade = [float(func.subs(x, val)) for val in x_shade]
        ax.fill_between(x_shade, y_shade, color='lightblue', alpha=0.5, label='Shaded area')
        ax.axvline(x=min_range, color='r', linestyle='--')
        ax.axvline(x=max_range, color='r', linestyle='--')

    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    
    root.canvas = FigureCanvasTkAgg(fig, master=root)
    root.canvas.draw()
    root.canvas.get_tk_widget().grid(row=7, column=0, columnspan=3)

def substitute_constants(value):
    """ Substitutes `e`, `pi`, `-oo`, and `+oo` in the range values. """
    value = value.replace('e', str(sp.E))
    value = value.replace('pi', str(sp.pi))
    value = value.replace('-oo', '-1000')
    value = value.replace('+oo', '1000')
    return value

def compute_limit():
    user_func_str = func_entry.get()
    limit_point_str = limit_entry.get()
    limit_point = sp.sympify(substitute_constants(limit_point_str))
    
    x = sp.symbols('x')
    try:
        f = sp.sympify(user_func_str)
        limit_left = sp.limit(f, x, limit_point, dir='-')
        limit_right = sp.limit(f, x, limit_point, dir='+')
        
        if limit_left == limit_right:
            limit_result = limit_left
        else:
            limit_result = 'Limit does not exist'

    except Exception as e:
        result_label.config(text=f'Error in limit calculation: {e}')
        return
    
    result_label.config(text=f'Limit as x approaches {limit_point}: {limit_result}')
    plot_function(user_func_str)

def integrate_function():
    func_input = func_entry.get().replace('|x|', 'Abs(x)')
    x = sp.symbols('x')
    func = sp.sympify(func_input)

    try:
        if integration_type.get() == 'Definite':
            range_min_input = min_entry.get()
            range_max_input = max_entry.get()

            range_min = sp.sympify(substitute_constants(range_min_input))
            range_max = sp.sympify(substitute_constants(range_max_input))
            
            # Explicitly handle symbolic limits
            if range_max_input == '+oo':
                range_max = sp.oo
            if range_min_input == '-oo':
                range_min = -sp.oo
            
            integral_result = sp.integrate(func, (x, range_min, range_max))
            result_label.config(text=f'Definite Integral result: {integral_result}')
            
            min_val = float(range_min if range_min != -sp.oo else -1000)
            max_val = float(range_max if range_max != sp.oo else 1000)
            plot_function(func_input, min_val, max_val, range_min, range_max)

        elif integration_type.get() == 'Indefinite':
            # Integrate and extract the real part to avoid complex results
            integral_result = sp.re(sp.integrate(func, x))
            result_label.config(text=f'Indefinite Integral: {integral_result} + C')
            plot_function(str(integral_result))

    except Exception as e:
        result_label.config(text=f"Error in integration: {e}")

def compute_differentiation():
    func_input = func_entry.get()
    x = sp.symbols('x')
    
    try:
        func = sp.sympify(func_input)
        derivative = sp.diff(func, x)
        
        # Display derivative
        result_label.config(text=f'Derivative: {derivative}')
        
        # Plot the original function and its derivative
        plot_function(func_input)
        show_all_properties()  # Show properties of the original function

    except Exception as e:
        result_label.config(text=f"Error in differentiation: {e}")


def show_all_properties():
    func_input = func_entry.get()
    x = sp.symbols('x')
    func = sp.sympify(func_input)
    
    x_intercepts = find_x_intercepts(func, x)
    y_intercept = find_y_intercept(func, x)
    vertical_asymptotes = find_vertical_asymptotes(func, x)
    horizontal_asymptotes = find_horizontal_asymptotes(func, x)
    slant_asymptote = find_slant_asymptote(func, x)
    extrema = find_extrema(func, x)
    inflection_points = find_inflection_points(func, x)
    
    properties_text = "Properties:\n"
    properties_text += f"X-Intercepts: {x_intercepts}\n"
    properties_text += f"Y-Intercept: {y_intercept}\n"
    properties_text += f"Vertical Asymptotes: {vertical_asymptotes if vertical_asymptotes else 'None'}\n"
    properties_text += f"Horizontal Asymptotes: {horizontal_asymptotes}\n"
    properties_text += f"Slant Asymptote: {slant_asymptote if slant_asymptote else 'None'}\n"
    properties_text += f"Relative Extrema: {extrema}\n"
    properties_text += f"Inflection Points: {inflection_points}\n"
    
    result_label.config(text=properties_text)
    plot_function(func_input)

def clear_widgets():
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 0:
            widget.grid_forget()

    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().destroy()

def on_option_change(*args):
    option = operation_var.get()
    if option == 'Limit':
        show_limit_widgets()
    elif option == 'Integrate':
        show_integration_type_widgets()
    elif option == 'Differentiation':
        show_differentiation_widgets()
    elif option == 'Instruction':
        show_instruction()

def show_limit_widgets():
    clear_widgets()
    func_label.grid(row=1, column=0)
    func_entry.grid(row=1, column=1)
    limit_label.grid(row=2, column=0)
    limit_entry.grid(row=2, column=1)
    compute_limit_button.grid(row=3, column=0, columnspan=2)
    result_label.grid(row=4, column=0, columnspan=2)

def show_integration_type_widgets():
    clear_widgets()
    integration_type_label.grid(row=1, column=0)
    defined_radio.grid(row=1, column=1)
    undefined_radio.grid(row=1, column=2)
    show_function_widgets()

def show_function_widgets():
    func_label.grid(row=2, column=0)
    func_entry.grid(row=2, column=1)
    
    # Only show range inputs for Definite Integration
    if integration_type.get() == 'Definite':
        min_label.grid(row=3, column=0)
        min_entry.grid(row=3, column=1)
        max_label.grid(row=4, column=0)
        max_entry.grid(row=4, column=1)
    else:
        # Hide range inputs for Indefinite Integration
        min_label.grid_forget()
        min_entry.grid_forget()
        max_label.grid_forget()
        max_entry.grid_forget()
    
    compute_integration_button.grid(row=5, column=0, columnspan=2)
    result_label.grid(row=6, column=0, columnspan=2)


def show_differentiation_widgets():
    clear_widgets()
    func_label.grid(row=1, column=0)
    func_entry.grid(row=1, column=1)
    compute_differentiation_button.grid(row=2, column=0, columnspan=2)
    result_label.grid(row=3, column=0, columnspan=2)

def show_instruction():
    clear_widgets()
    instruction_text = (
        "Instructions:\n\n"
        "1. For limits, specify the point of interest (e.g., 0, pi/2, -oo).\n"
        "2. For integration, choose 'Definite' for a specific range or 'Indefinite' otherwise.\n"
        "3. For differentiation, just enter the function and click 'Compute Differentiation'.\n"
        "4. For inverse trigonometric functions, use 'asin', 'acos', 'atan', etc."
    )
    result_label.config(text=instruction_text)
    result_label.grid(row=1, column=0, columnspan=2)

# GUI Setup
root = tk.Tk()
root.title("Math Calculas App")

# Widgets for input and output
operation_var = tk.StringVar(value='Limit')
operation_var.trace('w', on_option_change)

operation_label = ttk.Label(root, text="Select Operation:")
operation_label.grid(row=0, column=0)

operation_menu = ttk.Combobox(root, textvariable=operation_var, values=('Limit', 'Integrate', 'Differentiation', 'Instruction'))
operation_menu.grid(row=0, column=1)

# Function Input Widgets
func_label = ttk.Label(root, text="Enter Function:")
func_entry = ttk.Entry(root)

# Limit Widgets
limit_label = ttk.Label(root, text="Limit Point:")
limit_entry = ttk.Entry(root)
compute_limit_button = ttk.Button(root, text="Compute Limit", command=compute_limit)

# Integration Widgets
integration_type_label = ttk.Label(root, text="Integration Type:")
integration_type = tk.StringVar(value='Definite')
defined_radio = ttk.Radiobutton(root, text='Definite', variable=integration_type, value='Definite', command=show_function_widgets)
undefined_radio = ttk.Radiobutton(root, text='Indefinite', variable=integration_type, value='Indefinite', command=show_function_widgets)

min_label = ttk.Label(root, text="Min Range:")
min_entry = ttk.Entry(root)
max_label = ttk.Label(root, text="Max Range:")
max_entry = ttk.Entry(root)
compute_integration_button = ttk.Button(root, text="Compute Integration", command=integrate_function)

# Differentiation Widgets
compute_differentiation_button = ttk.Button(root, text="Compute Differentiation", command=compute_differentiation)

# Result Display
result_label = ttk.Label(root, text="", wraplength=400)

# Start by showing the limit widgets
on_option_change()

root.mainloop()

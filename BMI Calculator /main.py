import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

def compute_bmi(weight, height):
    """Calculate BMI using weight (kg) and height (m)."""
    return weight / (height ** 2)

def get_bmi_category(bmi):
    """Categorize BMI into health ranges."""
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 24.9:
        return 'Normal weight'
    elif 25 <= bmi < 29.9:
        return 'Overweight'
    else:
        return 'Obesity'

def store_user_data(weight, height, bmi, category):
    """Save BMI data to a JSON file for tracking."""
    # Ensure the 'data' directory exists
    os.makedirs('data', exist_ok=True)
    
    file_path = 'data/bmi_records.json'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)
    
    with open(file_path, 'r+') as file:
        records = json.load(file)
        records.append({
            'weight': weight,
            'height': height,
            'bmi': bmi,
            'category': category
        })
        file.seek(0)
        json.dump(records, file, indent=4)

def plot_bmi_trends():
    """Visualize BMI data trends."""
    file_path = 'data/bmi_records.json'
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r') as file:
        records = json.load(file)

    weights = [record['weight'] for record in records]
    heights = [record['height'] for record in records]
    bmis = [record['bmi'] for record in records]
    
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(bmis)), bmis, marker='o', linestyle='-', color='green')
    plt.xlabel('Record Number')
    plt.ylabel('BMI')
    plt.title('BMI Records Over Time')
    
    canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, pady=10)
    canvas.draw()

def display_results():
    """Process user input and show BMI results."""
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        
        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive values.")
        
        bmi = compute_bmi(weight, height)
        category = get_bmi_category(bmi)
        
        result_text.set(f"Your BMI: {bmi:.2f}\nCategory: {category}")
        store_user_data(weight, height, bmi, category)
        plot_bmi_trends()
    
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Set up GUI
window = tk.Tk()
window.title("Advanced BMI Calculator")

tk.Label(window, text="Weight (kg):").grid(row=0, column=0, padx=10, pady=10)
weight_entry = tk.Entry(window)
weight_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(window, text="Height (m):").grid(row=1, column=0, padx=10, pady=10)
height_entry = tk.Entry(window)
height_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Button(window, text="Calculate BMI", command=display_results).grid(row=2, column=0, columnspan=2, pady=10)
result_text = tk.StringVar()
tk.Label(window, textvariable=result_text).grid(row=3, column=0, columnspan=2, pady=10)

window.mainloop()

import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

def generate_password(length, include_numbers, include_symbols, exclude_chars, min_uppercase):
    """Generate a random password based on user criteria."""
    letters = string.ascii_letters
    numbers = string.digits if include_numbers else ''
    symbols = string.punctuation if include_symbols else ''
    
    characters = letters + numbers + symbols
    characters = ''.join(c for c in characters if c not in exclude_chars)
    
    if not characters:
        raise ValueError("At least one character set must be included.")
    
    password = []
    if min_uppercase:
        password.append(random.choice(string.ascii_uppercase))
        length -= 1
    
    password += [random.choice(characters) for _ in range(length)]
    random.shuffle(password)
    
    return ''.join(password)

def on_generate_click():
    """Handle the Generate button click."""
    try:
        length = int(length_entry.get())
        if length < 1:
            raise ValueError("Password length must be at least 1.")
        
        include_numbers = numbers_var.get()
        include_symbols = symbols_var.get()
        exclude_chars = exclude_chars_entry.get()
        min_uppercase = min_uppercase_var.get()
        
        password = generate_password(length, include_numbers, include_symbols, exclude_chars, min_uppercase)
        password_var.set(password)
        pyperclip.copy(password)  # Copy password to clipboard
        messagebox.showinfo("Success", "Password copied to clipboard!")
    
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Set up GUI
window = tk.Tk()
window.title("Advanced Password Generator")

tk.Label(window, text="Password Length:").grid(row=0, column=0, padx=10, pady=10)
length_entry = tk.Entry(window)
length_entry.grid(row=0, column=1, padx=10, pady=10)

numbers_var = tk.BooleanVar()
tk.Checkbutton(window, text="Include Numbers", variable=numbers_var).grid(row=1, column=0, padx=10, pady=10)

symbols_var = tk.BooleanVar()
tk.Checkbutton(window, text="Include Symbols", variable=symbols_var).grid(row=1, column=1, padx=10, pady=10)

tk.Label(window, text="Exclude Characters:").grid(row=2, column=0, padx=10, pady=10)
exclude_chars_entry = tk.Entry(window)
exclude_chars_entry.grid(row=2, column=1, padx=10, pady=10)

min_uppercase_var = tk.BooleanVar()
tk.Checkbutton(window, text="Include at least one uppercase letter", variable=min_uppercase_var).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

tk.Button(window, text="Generate Password", command=on_generate_click).grid(row=4, column=0, columnspan=2, pady=10)

password_var = tk.StringVar()
tk.Entry(window, textvariable=password_var, width=50).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()

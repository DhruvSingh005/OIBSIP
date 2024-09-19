import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

def get_weather(api_key, location):
    """Fetch weather data from the API and return it."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if response.status_code != 200:
        raise ValueError(f"Error fetching data: {data.get('message', 'Unknown error')}")
    
    weather_info = {
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'weather': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }
    return weather_info

def update_weather():
    """Update weather data on the GUI."""
    api_key = 'YOUR_API_KEY_HERE'  # Replace with your OpenWeatherMap API key
    location = location_entry.get()
    
    try:
        weather = get_weather(api_key, location)
        temperature_var.set(f"Temperature: {weather['temperature']}°C")
        humidity_var.set(f"Humidity: {weather['humidity']}%")
        weather_var.set(f"Weather: {weather['weather']}")
        
        # Load and display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))
        icon_image = icon_image.resize((50, 50))  # Resize the icon
        icon_photo = ImageTk.PhotoImage(icon_image)
        
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo
        
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Set up GUI
window = tk.Tk()
window.title("Weather App")

tk.Label(window, text="Enter location:").grid(row=0, column=0, padx=10, pady=10)
location_entry = tk.Entry(window)
location_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Button(window, text="Get Weather", command=update_weather).grid(row=1, column=0, columnspan=2, pady=10)

temperature_var = tk.StringVar()
humidity_var = tk.StringVar()
weather_var = tk.StringVar()

tk.Label(window, textvariable=temperature_var).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
tk.Label(window, textvariable=humidity_var).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
tk.Label(window, textvariable=weather_var).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

icon_label = tk.Label(window)
icon_label.grid(row=2, column=2, rowspan=3, padx=10, pady=10)

window.mainloop()

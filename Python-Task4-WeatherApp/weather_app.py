import tkinter as tk
from tkinter import messagebox
import requests


# ============================================================
# OPENWEATHERMAP API KEY
# ============================================================
# Paste your NEW OpenWeatherMap API key between the quotes.
API_KEY = "dd16c1303a4d64f8ab1acf52cb2759cf"


# ============================================================
# GET WEATHER
# ============================================================
def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning(
            "Input Required",
            "Please enter a city name."
        )
        return

    if API_KEY == "PASTE_YOUR_NEW_API_KEY_HERE":
        messagebox.showerror(
            "API Key Required",
            "Please add your OpenWeatherMap API key in the code."
        )
        return

    status_label.config(
        text="Fetching weather information...",
        fg="#1688e8"
    )

    root.update_idletasks()

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"

        parameters = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(
            url,
            params=parameters,
            timeout=10
        )

        data = response.json()

        # Invalid API key
        if response.status_code == 401:
            messagebox.showerror(
                "API Error",
                "Invalid API key. Please check your OpenWeatherMap API key."
            )
            status_label.config(
                text="Invalid API key.",
                fg="#dc3545"
            )
            return

        # City not found
        if response.status_code == 404:
            messagebox.showerror(
                "City Not Found",
                f"Could not find the city '{city}'.\n"
                "Please check the spelling and try again."
            )
            status_label.config(
                text="City not found.",
                fg="#dc3545"
            )
            return

        # Other errors
        if response.status_code != 200:
            messagebox.showerror(
                "Weather Error",
                "Unable to retrieve weather information."
            )
            status_label.config(
                text="Unable to retrieve weather.",
                fg="#dc3545"
            )
            return

        # ====================================================
        # GET WEATHER DATA
        # ====================================================

        city_name = data["name"]
        country = data["sys"]["country"]

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        wind_speed = data["wind"]["speed"]

        description = data["weather"][0]["description"]
        description = description.title()

        # ====================================================
        # DISPLAY WEATHER DATA
        # ====================================================

        location_label.config(
            text=f"{city_name}, {country}"
        )

        temperature_label.config(
            text=f"{temperature:.1f}°C"
        )

        description_label.config(
            text=description
        )

        feels_like_value.config(
            text=f"{feels_like:.1f}°C"
        )

        humidity_value.config(
            text=f"{humidity}%"
        )

        wind_value.config(
            text=f"{wind_speed:.1f} m/s"
        )

        pressure_value.config(
            text=f"{pressure} hPa"
        )

        status_label.config(
            text="✓ Weather information updated successfully.",
            fg="#198754"
        )

    except requests.exceptions.Timeout:

        messagebox.showerror(
            "Connection Timeout",
            "The weather service took too long to respond.\n"
            "Please try again."
        )

        status_label.config(
            text="Connection timed out.",
            fg="#dc3545"
        )

    except requests.exceptions.ConnectionError:

        messagebox.showerror(
            "Connection Error",
            "Could not connect to the weather service.\n"
            "Please check your internet connection."
        )

        status_label.config(
            text="Connection error.",
            fg="#dc3545"
        )

    except requests.exceptions.RequestException:

        messagebox.showerror(
            "Network Error",
            "A network error occurred while retrieving weather data."
        )

        status_label.config(
            text="Network error.",
            fg="#dc3545"
        )

    except Exception as error:

        messagebox.showerror(
            "Unexpected Error",
            f"An unexpected error occurred:\n{error}"
        )

        status_label.config(
            text="Unexpected error occurred.",
            fg="#dc3545"
        )


# ============================================================
# CLEAR WEATHER
# ============================================================
def clear_weather():

    city_entry.delete(0, tk.END)

    location_label.config(
        text="City, Country"
    )

    temperature_label.config(
        text="--°C"
    )

    description_label.config(
        text="Weather Description"
    )

    feels_like_value.config(
        text="--"
    )

    humidity_value.config(
        text="--"
    )

    wind_value.config(
        text="--"
    )

    pressure_value.config(
        text="--"
    )

    status_label.config(
        text="Ready to search for weather information.",
        fg="#6c757d"
    )


# ============================================================
# ENTER KEY
# ============================================================
def enter_pressed(event):
    get_weather()


# ============================================================
# MAIN WINDOW
# ============================================================
root = tk.Tk()

root.title("Weather App")

root.geometry("950x650")

root.minsize(850, 600)

root.configure(
    bg="#f4f6f8"
)


# ============================================================
# TITLE BAR
# ============================================================
title_frame = tk.Frame(
    root,
    bg="#1688e8",
    height=80
)

title_frame.pack(fill="x")

title_frame.pack_propagate(False)


title_label = tk.Label(
    title_frame,
    text="Weather App",
    font=("Arial", 24, "bold"),
    bg="#1688e8",
    fg="white"
)

title_label.pack(
    side="left",
    padx=30,
    pady=18
)


subtitle_label = tk.Label(
    title_frame,
    text="Check real-time weather information for any city",
    font=("Arial", 10),
    bg="#1688e8",
    fg="white"
)

subtitle_label.pack(
    side="left",
    padx=5
)


# ============================================================
# MAIN FRAME
# ============================================================
main_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=25
)


# ============================================================
# SEARCH SECTION
# ============================================================
search_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid"
)

search_frame.pack(
    fill="x",
    pady=(0, 20)
)


search_title = tk.Label(
    search_frame,
    text="Search Weather",
    font=("Arial", 15, "bold"),
    bg="white",
    fg="#222222"
)

search_title.pack(
    anchor="w",
    padx=25,
    pady=(20, 5)
)


search_instruction = tk.Label(
    search_frame,
    text="Enter a city name to view its current weather conditions.",
    font=("Arial", 9),
    bg="white",
    fg="#777777"
)

search_instruction.pack(
    anchor="w",
    padx=25,
    pady=(0, 15)
)


search_container = tk.Frame(
    search_frame,
    bg="white"
)

search_container.pack(
    fill="x",
    padx=25,
    pady=(0, 20)
)


city_entry = tk.Entry(
    search_container,
    font=("Arial", 12),
    bd=1,
    relief="solid"
)

city_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=8
)


search_button = tk.Button(
    search_container,
    text="Search Weather",
    font=("Arial", 10, "bold"),
    bg="#1688e8",
    fg="white",
    activebackground="#0d72c7",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    command=get_weather
)

search_button.pack(
    side="left",
    padx=(10, 5),
    ipadx=15,
    ipady=8
)


clear_button = tk.Button(
    search_container,
    text="Clear",
    font=("Arial", 10, "bold"),
    bg="#eeeeee",
    fg="#333333",
    activebackground="#dddddd",
    bd=0,
    cursor="hand2",
    command=clear_weather
)

clear_button.pack(
    side="left",
    padx=(5, 0),
    ipadx=15,
    ipady=8
)


# ============================================================
# WEATHER DISPLAY
# ============================================================
weather_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid"
)

weather_frame.pack(
    fill="both",
    expand=True
)


# ============================================================
# LOCATION
# ============================================================
location_label = tk.Label(
    weather_frame,
    text="City, Country",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#222222"
)

location_label.pack(
    pady=(25, 5)
)


description_label = tk.Label(
    weather_frame,
    text="Weather Description",
    font=("Arial", 11),
    bg="white",
    fg="#777777"
)

description_label.pack(
    pady=(0, 10)
)


# ============================================================
# TEMPERATURE
# ============================================================
temperature_label = tk.Label(
    weather_frame,
    text="--°C",
    font=("Arial", 42, "bold"),
    bg="white",
    fg="#1688e8"
)

temperature_label.pack(
    pady=(5, 5)
)


temperature_text = tk.Label(
    weather_frame,
    text="Current Temperature",
    font=("Arial", 9),
    bg="white",
    fg="#777777"
)

temperature_text.pack(
    pady=(0, 20)
)


# ============================================================
# WEATHER INFORMATION
# ============================================================
info_frame = tk.Frame(
    weather_frame,
    bg="white"
)

info_frame.pack(
    fill="x",
    padx=30,
    pady=5
)


# ============================================================
# FEELS LIKE
# ============================================================
feels_frame = tk.Frame(
    info_frame,
    bg="#f5f9ff",
    bd=1,
    relief="solid"
)

feels_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5,
    ipady=10
)


tk.Label(
    feels_frame,
    text="Feels Like",
    font=("Arial", 10, "bold"),
    bg="#f5f9ff",
    fg="#555555"
).pack(
    pady=(10, 3)
)


feels_like_value = tk.Label(
    feels_frame,
    text="--",
    font=("Arial", 18, "bold"),
    bg="#f5f9ff",
    fg="#1688e8"
)

feels_like_value.pack(
    pady=(0, 10)
)


# ============================================================
# HUMIDITY
# ============================================================
humidity_frame = tk.Frame(
    info_frame,
    bg="#f5f9ff",
    bd=1,
    relief="solid"
)

humidity_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5,
    ipady=10
)


tk.Label(
    humidity_frame,
    text="Humidity",
    font=("Arial", 10, "bold"),
    bg="#f5f9ff",
    fg="#555555"
).pack(
    pady=(10, 3)
)


humidity_value = tk.Label(
    humidity_frame,
    text="--",
    font=("Arial", 18, "bold"),
    bg="#f5f9ff",
    fg="#1688e8"
)

humidity_value.pack(
    pady=(0, 10)
)


# ============================================================
# WIND SPEED
# ============================================================
wind_frame = tk.Frame(
    info_frame,
    bg="#f5f9ff",
    bd=1,
    relief="solid"
)

wind_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5,
    ipady=10
)


tk.Label(
    wind_frame,
    text="Wind Speed",
    font=("Arial", 10, "bold"),
    bg="#f5f9ff",
    fg="#555555"
).pack(
    pady=(10, 3)
)


wind_value = tk.Label(
    wind_frame,
    text="--",
    font=("Arial", 18, "bold"),
    bg="#f5f9ff",
    fg="#1688e8"
)

wind_value.pack(
    pady=(0, 10)
)


# ============================================================
# PRESSURE
# ============================================================
pressure_frame = tk.Frame(
    info_frame,
    bg="#f5f9ff",
    bd=1,
    relief="solid"
)

pressure_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5,
    ipady=10
)


tk.Label(
    pressure_frame,
    text="Pressure",
    font=("Arial", 10, "bold"),
    bg="#f5f9ff",
    fg="#555555"
).pack(
    pady=(10, 3)
)


pressure_value = tk.Label(
    pressure_frame,
    text="--",
    font=("Arial", 18, "bold"),
    bg="#f5f9ff",
    fg="#1688e8"
)

pressure_value.pack(
    pady=(0, 10)
)


# ============================================================
# STATUS
# ============================================================
status_label = tk.Label(
    root,
    text="Ready to search for weather information.",
    font=("Arial", 9),
    bg="#f4f6f8",
    fg="#6c757d"
)

status_label.pack(
    pady=(0, 12)
)


# ============================================================
# ENTER KEY SUPPORT
# ============================================================
city_entry.bind(
    "<Return>",
    enter_pressed
)


# ============================================================
# START APPLICATION
# ============================================================
root.mainloop()
import json
import random
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import csv

# Sample motivational quotes
quotes = {
    "en": [
        "Every journey begins with a single step.",
        "Push yourself, because no one else is going to do it for you.",
        "A fool asks for an easier road, a wise man asks for stronger legs. Which one are you?",
        "It's better to light a candle than curse the darkness...",
        "You hold power beyond measure!",
        "You are the master of your fate, you are the captain of your soul!"
    ],
    "es": [
        "Cree en ti mismo y en todo lo que eres.",
        "El secreto para avanzar es comenzar.",
        "Cada viaje comienza con un solo paso.",
        "Empújate a ti mismo, porque nadie más lo hará por ti.",
        "El éxito no es definitivo, el fracaso no es fatal: es el coraje de continuar lo que cuenta."
    ],
    "fr": [
        "Croyez en vous et en tout ce que vous êtes.",
        "Le secret pour avancer est de commencer.",
        "Chaque voyage commence par un seul pas.",
        "Poussez-vous, car personne d'autre ne le fera pour vous.",
        "Le succès n'est pas définitif, l'échec n'est pas fatal : c'est le courage de continuer qui compte."
    ],
    "zh": [
        "Xiāngxìn nǐ zìjǐ yǐjí nǐ suǒ yǒngyǒu de yīqiè.",
        "Chénggōng de mìmì zàiyú kāishǐ xíngdòng.",
        "Měi duàn lǚchéng dōu shǐ yú dì yī bù.",
        "Tuīdòng zìjǐ, yīnwèi méiyǒu rén huì tì nǐ xíngdòng.",
        "Chénggōng bùshì zhōngdiǎn, shībài yě bùshì mò rì: guānjiàn zàiyú jìxù qiánxíng de yǒngqì."
    ],
    "zh_pinyin": [
        "Xiāngxìn nǐ zìjǐ yǐjí nǐ suǒ yǒngyǒu de yīqiè.",
        "Chénggōng de mìmì zàiyú kāishǐ xíngdòng.",
        "Měi duàn lǚchéng dōu shǐ yú dì yī bù.",
        "Tuīdòng zìjǐ, yīnwèi méiyǒu rén huì tì nǐ xíngdòng.",
        "Chénggōng bùshì zhōngdiǎn, shībài yě bùshì mò rì: guānjiàn zàiyú jìxù qiánxíng de yǒngqì."
    ]
}

# Function to save data to JSON file
def save_data(data):
    with open("fitness_data.json", "w") as file:
        json.dump(data, file, indent=4)

# Function to load data from JSON file
def load_data():
    try:
        with open("fitness_data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty list if no data or invalid data

# Function to show progress chart based on user input data
def show_chart():
    data = load_data()  # Load the actual user data
    if not data:
        messagebox.showinfo("No Data", "No data available to display chart!")
        return
    
    dates = [entry["date"] for entry in data]
    calories = [int(entry["calories"]) for entry in data]  # Assuming calories are integers

    plt.figure(figsize=(6, 4))
    plt.plot(dates, calories, marker="o", linestyle="-", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Calories Burned")
    plt.title("Calorie Burn Progress")
    plt.grid()
    plt.show()

# Function to add a fitness entry
def add_entry():
    # Get user input
    date = entry_date.get()
    workout = entry_workout.get()
    sets = entry_sets.get()
    reps = entry_reps.get()
    calories = entry_calories.get()
    heart_rate = entry_heart_rate.get()

    # Ensure all fields are filled
    if not all([date, workout, sets, reps, calories, heart_rate]):
        messagebox.showerror("Input Error", "All fields must be filled!")
        return

    # Add the entry to the Listbox and save to file
    entry_text = f"Date: {date} | Workout: {workout} | Sets: {sets} | Reps: {reps} | Calories: {calories} | Heart Rate: {heart_rate}"
    lb_entries.insert(tk.END, entry_text)

    # Load existing data and append the new entry
    data = load_data()
    data.append({
        "date": date,
        "workouts": workout,
        "sets": sets,
        "reps": reps,
        "calories": calories,
        "heart_rate": heart_rate
    })
    save_data(data)

    # Show a motivational quote in the selected language
    selected_language = language_var.get()
    quote = random.choice(quotes[selected_language])
    lbl_quote.config(text=f"👉 {quote}")

    # Clear the entry fields for the next input
    entry_date.delete(0, tk.END)
    entry_workout.delete(0, tk.END)
    entry_sets.delete(0, tk.END)
    entry_reps.delete(0, tk.END)
    entry_calories.delete(0, tk.END)
    entry_heart_rate.delete(0, tk.END)

# Function to display previous entries
def display_entries():
    data = load_data()
    lb_entries.delete(0, tk.END)  # Clear the Listbox before displaying
    if not data:
        lb_entries.insert(tk.END, "No fitness data available. Add some entries!")
        return
    for entry in data:
        entry_text = f"Date: {entry['date']} | Workout: {entry['workouts']} | Sets: {entry['sets']} | Reps: {entry['reps']} | Calories: {entry['calories']} | Heart Rate: {entry['heart_rate']}"
        lb_entries.insert(tk.END, entry_text)

# Function to export data to CSV
def export_to_csv():
    data = load_data()
    if not data:
        messagebox.showerror("No Data", "No data to export.")
        return
    with open("fitness_data.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    messagebox.showinfo("Export Successful", "Data exported to 'fitness_data.csv' successfully!")

# Function to clear all entries
def clear_entries():
    save_data([])
    lb_entries.delete(0, tk.END)
    messagebox.showinfo("Clear Successful", "All entries cleared.")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Fitness Tracker")
root.geometry("500x600")
root.config(bg="#eaf2f8")  # Set a light gradient background for modern feel

# Header Frame (Title)
header_frame = tk.Frame(root, bg="#eaf2f8")
header_frame.pack(pady=20)

title_label = tk.Label(header_frame, text="🏋️ Fitness Tracker", font=("Helvetica", 18, "bold"), bg="#eaf2f8", fg="#2980b9")
title_label.pack()

# Buttons Frame (Action Buttons)
button_frame = tk.Frame(root, bg="#eaf2f8")
button_frame.pack(pady=10)

# Modern Button Style with hover effects
def on_hover(event):
    event.widget.config(bg="#1abc9c")

def on_leave(event):
    event.widget.config(bg="#3498db")

btn_style = {
    'font': ("Helvetica", 12),
    'bg': "#3498db",  # Blue background for buttons
    'fg': "white",  # White text
    'relief': "flat",
    'bd': 3,
    'width': 20,
    'height': 2,
}

btn_add = tk.Button(button_frame, text="➕ Add Entry", command=add_entry, **btn_style)
btn_add.grid(row=0, column=0, padx=10, pady=10)
btn_add.bind("<Enter>", on_hover)
btn_add.bind("<Leave>", on_leave)

btn_chart = tk.Button(button_frame, text="📊 View Progress", command=show_chart, **btn_style)
btn_chart.grid(row=0, column=1, padx=10, pady=10)
btn_chart.bind("<Enter>", on_hover)
btn_chart.bind("<Leave>", on_leave)

btn_display = tk.Button(button_frame, text="📝 View Entries", command=display_entries, **btn_style)
btn_display.grid(row=1, column=0, padx=10, pady=10)
btn_display.bind("<Enter>", on_hover)
btn_display.bind("<Leave>", on_leave)

btn_export = tk.Button(button_frame, text="💾 Export Data", command=export_to_csv, **btn_style)
btn_export.grid(row=1, column=1, padx=10, pady=10)
btn_export.bind("<Enter>", on_hover)
btn_export.bind("<Leave>", on_leave)

btn_clear = tk.Button(button_frame, text="🗑️ Clear Entries", command=clear_entries, **btn_style)
btn_clear.grid(row=2, column=0, padx=10, pady=10)
btn_clear.bind("<Enter>", on_hover)
btn_clear.bind("<Leave>", on_leave)

# Input Fields Frame (User Input)
input_frame = tk.Frame(root, bg="#eaf2f8")
input_frame.pack(pady=10)

entry_date = tk.Entry(input_frame, font=("Helvetica", 12), width=20, bd=2, relief="solid")
entry_date.grid(row=0, column=1, padx=5, pady=5)
entry_workout = tk.Entry(input_frame, font=("Helvetica", 12), width=20, bd=2, relief="solid")
entry_workout.grid(row=1, column=1, padx=5, pady=5)
entry_sets = tk.Entry(input_frame, font=("Helvetica", 12), width=20, bd=2, relief="solid")
entry_sets.grid(row=2, column=1, padx=5, pady=5)
entry_reps = tk.Entry(input_frame, font=("Helvetica", 12), width=20, bd=2, relief="solid")
entry_reps.grid(row=3, column=1, padx=5, pady=5)
entry_calories = tk.Entry(input_frame, font=("Helvetica", 12), width=20, bd=2, relief="solid")
entry_calories.grid(row=4, column=1, padx=5, pady=5)
entry_heart_rate = tk.Entry(input_frame, font=("Helvetica", 12), width=20, bd=2, relief="solid")
entry_heart_rate.grid(row=5, column=1, padx=5, pady=5)

# Labels for input fields
labels = ["Date (YYYY-MM-DD)", "Workout", "Sets", "Reps", "Calories", "Heart Rate (BPM)"]
for i, label_text in enumerate(labels):
    label = tk.Label(input_frame, text=label_text, font=("Helvetica", 12), bg="#eaf2f8", fg="#2980b9")
    label.grid(row=i, column=0, padx=5, pady=5)

# Language Selection Dropdown (For Quotes)
language_var = tk.StringVar(value="en")  # Default is English
language_label = tk.Label(root, text="Select Language for Quotes:", font=("Helvetica", 12), bg="#eaf2f8", fg="#2980b9")
language_label.pack(pady=5)

language_menu = tk.OptionMenu(root, language_var, "en", "es", "fr", "zh", "zh_pinyin")
language_menu.config(font=("Helvetica", 12), bg="#3498db", fg="white")
language_menu.pack(pady=5)

# Displaying the motivational quote
lbl_quote = tk.Label(root, text="👉 Stay Motivated!", font=("Helvetica", 14, "italic"), bg="#eaf2f8", fg="#1abc9c")
lbl_quote.pack(pady=5)

# Listbox to display the saved entries
lb_entries = tk.Listbox(root, font=("Helvetica", 10), height=10, width=50, bd=2, relief="solid")
lb_entries.pack(pady=10)

# Run the Tkinter app
root.mainloop()

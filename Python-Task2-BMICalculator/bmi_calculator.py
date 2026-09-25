import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


# ==========================================================
# DATABASE
# ==========================================================

conn = sqlite3.connect("bmi_history.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        weight REAL NOT NULL,
        height REAL NOT NULL,
        bmi REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
    )
""")

conn.commit()


# ==========================================================
# BMI CALCULATION
# ==========================================================

def calculate_bmi():
    name = name_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    # Validate name
    if not name:
        messagebox.showerror("Input Error", "Please enter your name.")
        return

    # Validate weight and height
    try:
        weight = float(weight_text)
        height_cm = float(height_text)

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numbers for weight and height."
        )
        return

    # Check positive values
    if weight <= 0:
        messagebox.showerror(
            "Input Error",
            "Weight must be greater than 0."
        )
        return

    if height_cm <= 0:
        messagebox.showerror(
            "Input Error",
            "Height must be greater than 0."
        )
        return

    # Convert height from cm to meters
    height_m = height_cm / 100

    # BMI formula
    bmi = weight / (height_m ** 2)

    # Determine category
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    # Display BMI
    bmi_value_label.config(
        text=f"{bmi:.2f}"
    )

    category_label.config(
        text=category
    )

    # Store current calculation
    global current_bmi
    global current_category

    current_bmi = bmi
    current_category = category


# ==========================================================
# SAVE RECORD
# ==========================================================

def save_record():
    name = name_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    # Check whether BMI has been calculated
    if current_bmi is None:
        messagebox.showwarning(
            "Calculate BMI",
            "Please calculate BMI before saving the record."
        )
        return

    try:
        weight = float(weight_text)
        height = float(height_text)

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid weight and height."
        )
        return

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO bmi_records
        (name, weight, height, bmi, category, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        weight,
        height,
        current_bmi,
        current_category,
        date
    ))

    conn.commit()

    messagebox.showinfo(
        "Record Saved",
        "BMI record saved successfully!"
    )

    load_history()


# ==========================================================
# LOAD HISTORY
# ==========================================================

def load_history():
    # Clear existing rows
    for item in history_table.get_children():
        history_table.delete(item)

    cursor.execute("""
        SELECT name, weight, height, bmi, category, date
        FROM bmi_records
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    for record in records:
        name, weight, height, bmi, category, date = record

        history_table.insert(
            "",
            tk.END,
            values=(
                name,
                f"{weight:.2f}",
                f"{height:.2f}",
                f"{bmi:.2f}",
                category,
                date
            )
        )


# ==========================================================
# SHOW GRAPH
# ==========================================================

def show_graph():

    cursor.execute("""
        SELECT name, bmi, date
        FROM bmi_records
        ORDER BY id
    """)

    records = cursor.fetchall()

    if not records:
        messagebox.showinfo(
            "No Data",
            "No BMI records available. Save at least one record first."
        )
        return

    names = [record[0] for record in records]
    bmi_values = [record[1] for record in records]

    plt.figure(figsize=(10, 5))

    plt.plot(
        range(1, len(bmi_values) + 1),
        bmi_values,
        marker="o",
        linewidth=2
    )

    plt.axhline(
        y=18.5,
        linestyle="--",
        label="Underweight Limit"
    )

    plt.axhline(
        y=25,
        linestyle="--",
        label="Normal Limit"
    )

    plt.axhline(
        y=30,
        linestyle="--",
        label="Overweight Limit"
    )

    plt.title("BMI History")
    plt.xlabel("Record Number")
    plt.ylabel("BMI")
    plt.xticks(
        range(1, len(names) + 1),
        names,
        rotation=45,
        ha="right"
    )

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.show()


# ==========================================================
# CLEAR INPUTS
# ==========================================================

def clear_fields():

    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    bmi_value_label.config(
        text="--"
    )

    category_label.config(
        text="Category"
    )

    global current_bmi
    global current_category

    current_bmi = None
    current_category = None


# ==========================================================
# CLOSE APPLICATION
# ==========================================================

def close_application():
    conn.close()
    root.destroy()


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()

root.title("BMI Calculator")
root.geometry("1100x650")
root.minsize(1000, 600)

root.configure(
    bg="#f4f6f8"
)


# ==========================================================
# TITLE BAR
# ==========================================================

title_frame = tk.Frame(
    root,
    bg="#1688e8",
    height=60
)

title_frame.pack(
    fill="x"
)

title_frame.pack_propagate(False)


title_label = tk.Label(
    title_frame,
    text="BMI Calculator",
    font=("Arial", 22, "bold"),
    bg="#1688e8",
    fg="white"
)

title_label.pack(
    side="left",
    padx=25,
    pady=12
)


subtitle_label = tk.Label(
    title_frame,
    text="Calculate your Body Mass Index and maintain your health records",
    font=("Arial", 10),
    bg="#1688e8",
    fg="white"
)

subtitle_label.pack(
    side="left",
    padx=10
)


# ==========================================================
# MAIN CONTENT
# ==========================================================

main_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


# ==========================================================
# LEFT PANEL
# ==========================================================

left_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid"
)

left_frame.pack(
    side="left",
    fill="y",
    padx=(0, 15)
)


details_title = tk.Label(
    left_frame,
    text="Enter Your Details",
    font=("Arial", 15, "bold"),
    bg="white",
    fg="#222222"
)

details_title.pack(
    anchor="w",
    padx=20,
    pady=(20, 5)
)


instruction_label = tk.Label(
    left_frame,
    text="Calculate your BMI and maintain your health records.",
    font=("Arial", 9),
    bg="white",
    fg="#777777"
)

instruction_label.pack(
    anchor="w",
    padx=20,
    pady=(0, 20)
)


# ---------------- NAME ----------------

name_label = tk.Label(
    left_frame,
    text="Name",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333"
)

name_label.pack(
    anchor="w",
    padx=20
)


name_entry = tk.Entry(
    left_frame,
    font=("Arial", 11),
    width=32,
    bd=1,
    relief="solid"
)

name_entry.pack(
    padx=20,
    pady=(5, 15),
    ipady=5
)


# ---------------- WEIGHT ----------------

weight_label = tk.Label(
    left_frame,
    text="Weight (kg)",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333"
)

weight_label.pack(
    anchor="w",
    padx=20
)


weight_entry = tk.Entry(
    left_frame,
    font=("Arial", 11),
    width=32,
    bd=1,
    relief="solid"
)

weight_entry.pack(
    padx=20,
    pady=(5, 15),
    ipady=5
)


# ---------------- HEIGHT ----------------

height_label = tk.Label(
    left_frame,
    text="Height (cm)",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333"
)

height_label.pack(
    anchor="w",
    padx=20
)


height_entry = tk.Entry(
    left_frame,
    font=("Arial", 11),
    width=32,
    bd=1,
    relief="solid"
)

height_entry.pack(
    padx=20,
    pady=(5, 15),
    ipady=5
)


# ==========================================================
# BMI RESULT
# ==========================================================

result_frame = tk.Frame(
    left_frame,
    bg="#f5f9ff",
    bd=1,
    relief="solid"
)

result_frame.pack(
    padx=20,
    pady=10,
    fill="x"
)


bmi_value_label = tk.Label(
    result_frame,
    text="--",
    font=("Arial", 25, "bold"),
    bg="#f5f9ff",
    fg="#1688e8"
)

bmi_value_label.pack(
    pady=(10, 0)
)


bmi_text_label = tk.Label(
    result_frame,
    text="BMI",
    font=("Arial", 9),
    bg="#f5f9ff",
    fg="#777777"
)

bmi_text_label.pack()


category_label = tk.Label(
    result_frame,
    text="Category",
    font=("Arial", 10, "bold"),
    bg="#f5f9ff",
    fg="#333333"
)

category_label.pack(
    pady=(3, 12)
)


# ==========================================================
# BUTTONS
# ==========================================================

calculate_button = tk.Button(
    left_frame,
    text="Calculate BMI",
    font=("Arial", 10, "bold"),
    bg="#1688e8",
    fg="white",
    activebackground="#0d72c7",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    command=calculate_bmi
)

calculate_button.pack(
    padx=20,
    pady=(5, 7),
    fill="x",
    ipady=7
)


save_button = tk.Button(
    left_frame,
    text="Save Record",
    font=("Arial", 10, "bold"),
    bg="#2e9d45",
    fg="white",
    activebackground="#247c37",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    command=save_record
)

save_button.pack(
    padx=20,
    pady=5,
    fill="x",
    ipady=7
)


graph_button = tk.Button(
    left_frame,
    text="Show Graph",
    font=("Arial", 10, "bold"),
    bg="#555555",
    fg="white",
    activebackground="#444444",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    command=show_graph
)

graph_button.pack(
    padx=20,
    pady=5,
    fill="x",
    ipady=7
)


clear_button = tk.Button(
    left_frame,
    text="Clear",
    font=("Arial", 10, "bold"),
    bg="#eeeeee",
    fg="#333333",
    activebackground="#dddddd",
    bd=0,
    cursor="hand2",
    command=clear_fields
)

clear_button.pack(
    padx=20,
    pady=(5, 15),
    fill="x",
    ipady=5
)


# ==========================================================
# RIGHT PANEL - BMI HISTORY
# ==========================================================

right_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid"
)

right_frame.pack(
    side="right",
    fill="both",
    expand=True
)


history_title = tk.Label(
    right_frame,
    text="BMI History",
    font=("Arial", 15, "bold"),
    bg="white",
    fg="#222222"
)

history_title.pack(
    anchor="w",
    padx=20,
    pady=(20, 15)
)


# ==========================================================
# TREEVIEW STYLE
# ==========================================================

style = ttk.Style()

style.configure(
    "Treeview",
    font=("Arial", 9),
    rowheight=30
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 9, "bold")
)


# ==========================================================
# HISTORY TABLE
# ==========================================================

table_frame = tk.Frame(
    right_frame,
    bg="white"
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 20)
)


columns = (
    "Name",
    "Weight (kg)",
    "Height (cm)",
    "BMI",
    "Category",
    "Date"
)


history_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


for column in columns:

    history_table.heading(
        column,
        text=column
    )


history_table.column(
    "Name",
    width=110,
    anchor="center"
)

history_table.column(
    "Weight (kg)",
    width=90,
    anchor="center"
)

history_table.column(
    "Height (cm)",
    width=90,
    anchor="center"
)

history_table.column(
    "BMI",
    width=70,
    anchor="center"
)

history_table.column(
    "Category",
    width=110,
    anchor="center"
)

history_table.column(
    "Date",
    width=150,
    anchor="center"
)


# Scrollbar

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=history_table.yview
)

history_table.configure(
    yscrollcommand=scrollbar.set
)


history_table.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# ==========================================================
# GLOBAL VARIABLES
# ==========================================================

current_bmi = None
current_category = None


# ==========================================================
# LOAD PREVIOUS RECORDS
# ==========================================================

load_history()


# ==========================================================
# CLOSE EVENT
# ==========================================================

root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)


# ==========================================================
# START APPLICATION
# ==========================================================

root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
import string
import secrets


# ---------------- PASSWORD FUNCTIONS ---------------- #

def generate_password():
    try:
        length = int(length_entry.get())

        if length < 8:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 8 characters."
            )
            return

        selected_types = []

        if uppercase_var.get():
            selected_types.append("uppercase")

        if lowercase_var.get():
            selected_types.append("lowercase")

        if numbers_var.get():
            selected_types.append("numbers")

        if symbols_var.get():
            selected_types.append("symbols")

        if len(selected_types) < 2:
            messagebox.showerror(
                "Selection Error",
                "Please select at least two character types."
            )
            return

        # Character sets
        character_sets = {
            "uppercase": string.ascii_uppercase,
            "lowercase": string.ascii_lowercase,
            "numbers": string.digits,
            "symbols": string.punctuation
        }

        # Make sure at least one character from every selected type is included
        password_characters = [
            secrets.choice(character_sets[char_type])
            for char_type in selected_types
        ]

        # Combine selected character sets
        all_characters = "".join(
            character_sets[char_type]
            for char_type in selected_types
        )

        # Fill remaining characters
        remaining_length = length - len(password_characters)

        password_characters.extend(
            secrets.choice(all_characters)
            for _ in range(remaining_length)
        )

        # Securely shuffle the password
        secrets.SystemRandom().shuffle(password_characters)

        password = "".join(password_characters)

        password_entry.config(state="normal")
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
        password_entry.config(state="readonly")

        update_strength(password)

        status_label.config(
            text="✓ Password generated successfully!",
            foreground="#198754"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid password length."
        )


def update_strength(password):
    """Calculate and display password strength."""

    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(char in string.punctuation for char in password):
        score += 1

    if score <= 2:
        strength_label.config(
            text="Weak",
            foreground="#dc3545"
        )
    elif score <= 4:
        strength_label.config(
            text="Medium",
            foreground="#fd7e14"
        )
    else:
        strength_label.config(
            text="Strong",
            foreground="#198754"
        )


def copy_password():
    password = password_entry.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Please generate a password first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    status_label.config(
        text="✓ Password copied to clipboard!",
        foreground="#198754"
    )


def clear_password():
    password_entry.config(state="normal")
    password_entry.delete(0, tk.END)
    password_entry.config(state="readonly")

    strength_label.config(
        text="Not Generated",
        foreground="#6c757d"
    )

    status_label.config(
        text="Ready to generate a password.",
        foreground="#6c757d"
    )


def toggle_password():
    if password_entry.cget("show") == "":
        password_entry.config(show="•")
        show_button.config(text="Show")
    else:
        password_entry.config(show="")
        show_button.config(text="Hide")


# ---------------- MAIN WINDOW ---------------- #

root = tk.Tk()

root.title("Random Password Generator")
root.geometry("850x650")
root.minsize(800, 600)
root.configure(bg="#f4f6f8")


# ---------------- TITLE BAR ---------------- #

title_frame = tk.Frame(
    root,
    bg="#1688e8",
    height=75
)

title_frame.pack(fill="x")
title_frame.pack_propagate(False)


title_label = tk.Label(
    title_frame,
    text="Random Password Generator",
    font=("Arial", 22, "bold"),
    bg="#1688e8",
    fg="white"
)

title_label.pack(side="left", padx=25, pady=18)


subtitle_label = tk.Label(
    title_frame,
    text="Create secure and strong passwords instantly",
    font=("Arial", 10),
    bg="#1688e8",
    fg="white"
)

subtitle_label.pack(side="left", padx=10)


# ---------------- MAIN FRAME ---------------- #

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


# ---------------- LEFT CARD ---------------- #

settings_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid"
)

settings_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 15)
)


settings_title = tk.Label(
    settings_frame,
    text="Password Settings",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="#222222"
)

settings_title.pack(
    anchor="w",
    padx=25,
    pady=(25, 5)
)


instruction_label = tk.Label(
    settings_frame,
    text="Customize your password requirements.",
    font=("Arial", 9),
    bg="white",
    fg="#777777"
)

instruction_label.pack(
    anchor="w",
    padx=25,
    pady=(0, 20)
)


# ---------------- LENGTH ---------------- #

length_label = tk.Label(
    settings_frame,
    text="Password Length",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333"
)

length_label.pack(
    anchor="w",
    padx=25
)


length_entry = tk.Entry(
    settings_frame,
    font=("Arial", 11),
    width=30,
    bd=1,
    relief="solid"
)

length_entry.pack(
    padx=25,
    pady=(6, 20),
    ipady=6,
    fill="x"
)

length_entry.insert(0, "12")


# ---------------- CHARACTER TYPES ---------------- #

types_label = tk.Label(
    settings_frame,
    text="Character Types",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333"
)

types_label.pack(
    anchor="w",
    padx=25,
    pady=(0, 8)
)


uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)


uppercase_check = tk.Checkbutton(
    settings_frame,
    text="Uppercase Letters (A-Z)",
    variable=uppercase_var,
    font=("Arial", 10),
    bg="white",
    activebackground="white",
    anchor="w"
)

uppercase_check.pack(
    anchor="w",
    padx=25,
    pady=3
)


lowercase_check = tk.Checkbutton(
    settings_frame,
    text="Lowercase Letters (a-z)",
    variable=lowercase_var,
    font=("Arial", 10),
    bg="white",
    activebackground="white",
    anchor="w"
)

lowercase_check.pack(
    anchor="w",
    padx=25,
    pady=3
)


numbers_check = tk.Checkbutton(
    settings_frame,
    text="Numbers (0-9)",
    variable=numbers_var,
    font=("Arial", 10),
    bg="white",
    activebackground="white",
    anchor="w"
)

numbers_check.pack(
    anchor="w",
    padx=25,
    pady=3
)


symbols_check = tk.Checkbutton(
    settings_frame,
    text="Symbols (!@#$...)",
    variable=symbols_var,
    font=("Arial", 10),
    bg="white",
    activebackground="white",
    anchor="w"
)

symbols_check.pack(
    anchor="w",
    padx=25,
    pady=3
)


# ---------------- GENERATE BUTTON ---------------- #

generate_button = tk.Button(
    settings_frame,
    text="Generate Password",
    font=("Arial", 10, "bold"),
    bg="#1688e8",
    fg="white",
    activebackground="#0d72c7",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    command=generate_password
)

generate_button.pack(
    padx=25,
    pady=(25, 8),
    fill="x",
    ipady=8
)


clear_button = tk.Button(
    settings_frame,
    text="Clear",
    font=("Arial", 10, "bold"),
    bg="#eeeeee",
    fg="#333333",
    activebackground="#dddddd",
    bd=0,
    cursor="hand2",
    command=clear_password
)

clear_button.pack(
    padx=25,
    pady=5,
    fill="x",
    ipady=6
)


# ---------------- RIGHT CARD ---------------- #

result_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid"
)

result_frame.pack(
    side="right",
    fill="both",
    expand=True
)


result_title = tk.Label(
    result_frame,
    text="Generated Password",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="#222222"
)

result_title.pack(
    anchor="w",
    padx=25,
    pady=(25, 5)
)


result_instruction = tk.Label(
    result_frame,
    text="Your secure password will appear below.",
    font=("Arial", 9),
    bg="white",
    fg="#777777"
)

result_instruction.pack(
    anchor="w",
    padx=25,
    pady=(0, 25)
)


# ---------------- PASSWORD DISPLAY ---------------- #

password_container = tk.Frame(
    result_frame,
    bg="#f5f9ff",
    bd=1,
    relief="solid"
)

password_container.pack(
    padx=25,
    pady=5,
    fill="x"
)


password_entry = tk.Entry(
    password_container,
    font=("Consolas", 14, "bold"),
    justify="center",
    bd=0,
    bg="#f5f9ff",
    fg="#1688e8",
    readonlybackground="#f5f9ff",
    state="readonly"
)

password_entry.pack(
    side="left",
    padx=12,
    pady=15,
    fill="x",
    expand=True
)


show_button = tk.Button(
    password_container,
    text="Show",
    font=("Arial", 9, "bold"),
    bg="#eeeeee",
    fg="#333333",
    bd=0,
    cursor="hand2",
    command=toggle_password
)

show_button.pack(
    side="right",
    padx=8,
    pady=8,
    ipadx=5,
    ipady=4
)


# ---------------- COPY BUTTON ---------------- #

copy_button = tk.Button(
    result_frame,
    text="Copy Password",
    font=("Arial", 10, "bold"),
    bg="#2e9d45",
    fg="white",
    activebackground="#247c37",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    command=copy_password
)

copy_button.pack(
    padx=25,
    pady=(15, 20),
    fill="x",
    ipady=8
)


# ---------------- STRENGTH ---------------- #

strength_title = tk.Label(
    result_frame,
    text="Password Strength",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333"
)

strength_title.pack(
    anchor="w",
    padx=25
)


strength_label = tk.Label(
    result_frame,
    text="Not Generated",
    font=("Arial", 13, "bold"),
    bg="white",
    fg="#6c757d"
)

strength_label.pack(
    anchor="w",
    padx=25,
    pady=(5, 20)
)


# ---------------- SECURITY INFORMATION ---------------- #

security_frame = tk.Frame(
    result_frame,
    bg="#f8f9fa",
    bd=1,
    relief="solid"
)

security_frame.pack(
    padx=25,
    pady=10,
    fill="x"
)


security_title = tk.Label(
    security_frame,
    text="Security Features",
    font=("Arial", 10, "bold"),
    bg="#f8f9fa",
    fg="#333333"
)

security_title.pack(
    anchor="w",
    padx=15,
    pady=(12, 5)
)


security_text = tk.Label(
    security_frame,
    text="• Minimum length of 8 characters\n"
         "• Multiple character types supported\n"
         "• Uses Python secrets module\n"
         "• Selected character types are guaranteed",
    font=("Arial", 9),
    bg="#f8f9fa",
    fg="#666666",
    justify="left"
)

security_text.pack(
    anchor="w",
    padx=15,
    pady=(0, 12)
)


# ---------------- STATUS ---------------- #

status_label = tk.Label(
    root,
    text="Ready to generate a password.",
    font=("Arial", 9),
    bg="#f4f6f8",
    fg="#6c757d"
)

status_label.pack(
    pady=(0, 10)
)


# ---------------- START APPLICATION ---------------- #

root.mainloop()
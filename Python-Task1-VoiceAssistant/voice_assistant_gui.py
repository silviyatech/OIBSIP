import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random
import threading


# ==========================================
# INITIALIZATION
# ==========================================

recognizer = sr.Recognizer()

conversation_history = []

# Prevent multiple speech operations at the same time
speech_lock = threading.Lock()


# ==========================================
# TEXT TO SPEECH
# ==========================================

def speak(text):
    # Show response in conversation history
    add_message("Assistant", text)

    # Speak the response
    with speech_lock:
        try:
            engine = pyttsx3.init()

            engine.say(text)
            engine.runAndWait()

            engine.stop()

        except Exception as e:
            print("Speech Error:", e)


# ==========================================
# ADD MESSAGE TO CONVERSATION
# ==========================================

def add_message(sender, message):

    conversation_history.append(
        f"{sender}: {message}"
    )

    def update_gui():

        conversation_text.config(
            state="normal"
        )

        if sender == "You":

            conversation_text.insert(
                tk.END,
                f"You:\n{message}\n\n"
            )

        else:

            conversation_text.insert(
                tk.END,
                f"Assistant:\n{message}\n\n"
            )

        conversation_text.see(tk.END)

        conversation_text.config(
            state="disabled"
        )

    root.after(
        0,
        update_gui
    )


# ==========================================
# LISTEN TO MICROPHONE
# ==========================================

def listen():

    try:

        update_status(
            "Adjusting microphone...",
            "orange"
        )

        # Device 1 is your working microphone
        with sr.Microphone(
            device_index=1
        ) as source:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            update_status(
                "Listening...",
                "lightgreen"
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        update_status(
            "Processing...",
            "yellow"
        )

        # Convert speech to text
        command = recognizer.recognize_google(
            audio
        )

        print("You:", command)

        add_message(
            "You",
            command
        )

        update_status(
            "Ready",
            "lightgreen"
        )

        return command.lower()

    except sr.WaitTimeoutError:

        speak(
            "I did not hear anything. Please try again."
        )

        update_status(
            "Ready",
            "lightgreen"
        )

        return ""

    except sr.UnknownValueError:

        speak(
            "Sorry, I could not understand what you said."
        )

        update_status(
            "Ready",
            "lightgreen"
        )

        return ""

    except sr.RequestError:

        speak(
            "Sorry, the speech recognition service is unavailable."
        )

        update_status(
            "Ready",
            "lightgreen"
        )

        return ""

    except OSError:

        speak(
            "There is a problem with the microphone. "
            "Please check your microphone."
        )

        update_status(
            "Microphone Error",
            "red"
        )

        return ""

    except Exception as e:

        print(
            "Microphone Error:",
            e
        )

        speak(
            "Something went wrong while listening."
        )

        update_status(
            "Ready",
            "lightgreen"
        )

        return ""


# ==========================================
# LISTEN AND PROCESS
# ==========================================

def listen_and_process():

    command = listen()

    if command:

        process_command(
            command
        )


# ==========================================
# PROCESS COMMAND
# ==========================================

def process_command(command):

    command = command.lower().strip()

    if not command:
        return


    # --------------------------------------
    # GREETING
    # --------------------------------------

    if (
        "hello" in command
        or "hi" in command
        or "hey" in command
    ):

        speak(
            "Hello! Nice to talk with you."
        )


    # --------------------------------------
    # HOW ARE YOU
    # --------------------------------------

    elif "how are you" in command:

        speak(
            "I am doing great! "
            "Thank you for asking. "
            "How can I help you?"
        )


    # --------------------------------------
    # WHAT IS YOUR NAME
    # --------------------------------------

    elif (
        "your name" in command
        or "who are you" in command
    ):

        speak(
            "I am your voice assistant."
        )


    # --------------------------------------
    # WHAT CAN YOU DO
    # --------------------------------------

    elif (
        "what can you do" in command
        or "your functions" in command
    ):

        speak(
            "I can tell you the time and date, "
            "search the web, open websites, "
            "tell jokes, and respond to simple commands."
        )


    # --------------------------------------
    # TIME
    # --------------------------------------

    elif "time" in command:

        current_time = datetime.datetime.now().strftime(
            "%I:%M:%S %p"
        )

        speak(
            f"The current time is {current_time}."
        )


    # --------------------------------------
    # DATE
    # --------------------------------------

    elif (
        "date" in command
        or "today" in command
    ):

        current_date = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        speak(
            f"Today's date is {current_date}."
        )


    # --------------------------------------
    # SEARCH GOOGLE
    # --------------------------------------

    elif "search" in command:

        search_query = command.replace(
            "search",
            "",
            1
        ).strip()

        if search_query:

            speak(
                f"Searching for {search_query}."
            )

            url = (
                "https://www.google.com/search?q="
                + search_query.replace(
                    " ",
                    "+"
                )
            )

            webbrowser.open(
                url
            )

        else:

            speak(
                "Please tell me what you want me to search for."
            )


    # --------------------------------------
    # OPEN YOUTUBE
    # --------------------------------------

    elif "youtube" in command:

        speak(
            "Opening YouTube."
        )

        webbrowser.open(
            "https://www.youtube.com"
        )


    # --------------------------------------
    # OPEN GOOGLE
    # --------------------------------------

    elif "google" in command:

        speak(
            "Opening Google."
        )

        webbrowser.open(
            "https://www.google.com"
        )


    # --------------------------------------
    # OPEN SPOTIFY
    # --------------------------------------

    elif "spotify" in command:

        speak(
            "Opening Spotify."
        )

        webbrowser.open(
            "https://open.spotify.com"
        )


    # --------------------------------------
    # TELL A JOKE
    # --------------------------------------

    elif "joke" in command:

        jokes = [

            "Why did the computer go to the doctor? "
            "Because it had a virus!",

            "Why was the computer cold? "
            "Because it left its Windows open!",

            "Why do programmers prefer dark mode? "
            "Because light attracts bugs!"

        ]

        speak(
            random.choice(jokes)
        )


    # --------------------------------------
    # HELP
    # --------------------------------------

    elif "help" in command:

        speak(
            "You can ask me for the time, date, "
            "search the web, open Google, "
            "YouTube or Spotify, tell a joke, "
            "or ask me how I am."
        )


    # --------------------------------------
    # THANK YOU
    # --------------------------------------

    elif (
        "thank you" in command
        or "thanks" in command
    ):

        speak(
            "You're welcome! "
            "I am happy to help."
        )


    # --------------------------------------
    # GOOD MORNING
    # --------------------------------------

    elif "good morning" in command:

        speak(
            "Good morning! "
            "I hope you have a great day."
        )


    # --------------------------------------
    # GOOD NIGHT
    # --------------------------------------

    elif "good night" in command:

        speak(
            "Good night! Have a nice rest."
        )


    # --------------------------------------
    # EXIT
    # --------------------------------------

    elif (
        "bye" in command
        or "exit" in command
        or "quit" in command
        or "goodbye" in command
        or "stop" in command
    ):

        speak(
            "Goodbye! Have a nice day."
        )

        root.after(
            1500,
            root.destroy
        )


    # --------------------------------------
    # UNKNOWN COMMAND
    # --------------------------------------

    else:

        speak(
            "Sorry, I don't know that command yet. "
            "Say help to hear the available commands."
        )


# ==========================================
# TEXT COMMAND
# ==========================================

def execute_text_command():

    command = command_entry.get().strip()

    if not command:
        return

    command_entry.delete(
        0,
        tk.END
    )

    add_message(
        "You",
        command
    )

    # Run command in background
    threading.Thread(
        target=process_command,
        args=(command,),
        daemon=True
    ).start()


# ==========================================
# LISTEN BUTTON
# ==========================================

def start_listening():

    listen_button.config(
        state="disabled"
    )

    update_status(
        "Starting microphone...",
        "orange"
    )

    def run():

        command = listen()

        if command:

            process_command(
                command
            )

        root.after(
            0,
            lambda: listen_button.config(
                state="normal"
            )
        )

    threading.Thread(
        target=run,
        daemon=True
    ).start()


# ==========================================
# CLEAR CONVERSATION
# ==========================================

def clear_conversation():

    conversation_history.clear()

    conversation_text.config(
        state="normal"
    )

    conversation_text.delete(
        "1.0",
        tk.END
    )

    conversation_text.config(
        state="disabled"
    )

    update_status(
        "Conversation cleared",
        "lightgreen"
    )


# ==========================================
# VIEW HISTORY
# ==========================================

def view_history():

    if not conversation_history:

        messagebox.showinfo(
            "Conversation History",
            "No conversation history available."
        )

        return

    history_window = tk.Toplevel(
        root
    )

    history_window.title(
        "Conversation History"
    )

    history_window.geometry(
        "600x450"
    )

    history_window.configure(
        bg="#202235"
    )

    title = tk.Label(
        history_window,
        text="Conversation History",
        font=("Arial", 18, "bold"),
        bg="#202235",
        fg="white"
    )

    title.pack(
        pady=15
    )

    history_box = tk.Text(
        history_window,
        bg="#2d3048",
        fg="white",
        font=("Arial", 11),
        wrap="word"
    )

    history_box.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    history_box.insert(
        tk.END,
        "\n\n".join(
            conversation_history
        )
    )

    history_box.config(
        state="disabled"
    )


# ==========================================
# STATUS UPDATE
# ==========================================

def update_status(
    text,
    color
):

    def update():

        status_label.config(
            text=f"● {text}",
            fg=color
        )

    root.after(
        0,
        update
    )


# ==========================================
# EXIT APPLICATION
# ==========================================

def exit_application():

    result = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if result:

        root.destroy()


# ==========================================
# GUI WINDOW
# ==========================================

root = tk.Tk()

root.title(
    "Voice Assistant"
)

root.geometry(
    "1000x650"
)

root.minsize(
    850,
    550
)

root.configure(
    bg="#1d1f2f"
)


# ==========================================
# TITLE
# ==========================================

title_frame = tk.Frame(
    root,
    bg="#1d1f2f"
)

title_frame.pack(
    fill="x",
    padx=25,
    pady=(20, 5)
)


title_label = tk.Label(
    title_frame,
    text="🎙 Voice Assistant",
    font=("Arial", 25, "bold"),
    bg="#1d1f2f",
    fg="white"
)

title_label.pack(
    anchor="w"
)


subtitle_label = tk.Label(
    title_frame,
    text="Smart Voice Assistant with Productivity Features",
    font=("Arial", 11),
    bg="#1d1f2f",
    fg="#9fa4c4"
)

subtitle_label.pack(
    anchor="w",
    pady=(3, 0)
)


# ==========================================
# MAIN AREA
# ==========================================

main_frame = tk.Frame(
    root,
    bg="#1d1f2f"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=15
)


# ==========================================
# LEFT PANEL
# ==========================================

left_panel = tk.Frame(
    main_frame,
    bg="#282b40",
    width=300
)

left_panel.pack(
    side="left",
    fill="y",
    padx=(0, 15)
)

left_panel.pack_propagate(
    False
)


controls_title = tk.Label(
    left_panel,
    text="Controls",
    font=("Arial", 16, "bold"),
    bg="#282b40",
    fg="white"
)

controls_title.pack(
    anchor="w",
    padx=20,
    pady=(20, 15)
)


# Listen button
listen_button = tk.Button(
    left_panel,
    text="🎤  Listen",
    command=start_listening,
    font=("Arial", 12, "bold"),
    bg="#7b5cff",
    fg="white",
    activebackground="#6848e8",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    height=2
)

listen_button.pack(
    fill="x",
    padx=20,
    pady=8
)


# Text command label
text_label = tk.Label(
    left_panel,
    text="⌨ Text Command",
    font=("Arial", 10),
    bg="#282b40",
    fg="#bfc3d9"
)

text_label.pack(
    anchor="w",
    padx=20,
    pady=(15, 5)
)


# Text command entry
command_entry = tk.Entry(
    left_panel,
    font=("Arial", 11),
    bg="#34374f",
    fg="white",
    insertbackground="white",
    relief="flat"
)

command_entry.pack(
    fill="x",
    padx=20,
    ipady=10
)


command_entry.bind(
    "<Return>",
    lambda event: execute_text_command()
)


# Execute button
execute_button = tk.Button(
    left_panel,
    text="▶  Execute",
    command=execute_text_command,
    font=("Arial", 11, "bold"),
    bg="#43a047",
    fg="white",
    activebackground="#388e3c",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    height=2
)

execute_button.pack(
    fill="x",
    padx=20,
    pady=8
)


# Clear button
clear_button = tk.Button(
    left_panel,
    text="Clear",
    command=clear_conversation,
    font=("Arial", 11, "bold"),
    bg="#34374f",
    fg="white",
    activebackground="#41455f",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    height=2
)

clear_button.pack(
    fill="x",
    padx=20,
    pady=8
)


# History button
history_button = tk.Button(
    left_panel,
    text="View History",
    command=view_history,
    font=("Arial", 11, "bold"),
    bg="#34374f",
    fg="white",
    activebackground="#41455f",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    height=2
)

history_button.pack(
    fill="x",
    padx=20,
    pady=8
)


# Exit button
exit_button = tk.Button(
    left_panel,
    text="Exit",
    command=exit_application,
    font=("Arial", 11, "bold"),
    bg="#ef5350",
    fg="white",
    activebackground="#d32f2f",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    height=2
)

exit_button.pack(
    fill="x",
    padx=20,
    pady=8
)


# Status
status_label = tk.Label(
    left_panel,
    text="● Ready",
    font=("Arial", 10, "bold"),
    bg="#282b40",
    fg="lightgreen"
)

status_label.pack(
    anchor="w",
    padx=20,
    pady=(15, 5)
)


# ==========================================
# SUGGESTED COMMANDS
# ==========================================

suggestions_title = tk.Label(
    left_panel,
    text="Try saying:",
    font=("Arial", 10),
    bg="#282b40",
    fg="#9fa4c4"
)

suggestions_title.pack(
    anchor="w",
    padx=20,
    pady=(15, 5)
)


suggestions = [
    "Hello",
    "How are you?",
    "What is the time?",
    "What is today's date?",
    "Search Python",
    "Open YouTube",
    "Tell me a joke",
    "Thank you",
    "Bye"
]


suggestions_text = tk.Label(
    left_panel,
    text="\n".join(
        "• " + item
        for item in suggestions
    ),
    justify="left",
    font=("Arial", 9),
    bg="#282b40",
    fg="#bfc3d9"
)

suggestions_text.pack(
    anchor="w",
    padx=25
)


# ==========================================
# RIGHT PANEL
# ==========================================

right_panel = tk.Frame(
    main_frame,
    bg="#282b40"
)

right_panel.pack(
    side="right",
    fill="both",
    expand=True
)


conversation_title = tk.Label(
    right_panel,
    text="Conversation History",
    font=("Arial", 16, "bold"),
    bg="#282b40",
    fg="white"
)

conversation_title.pack(
    anchor="w",
    padx=20,
    pady=(20, 10)
)


# Conversation area
conversation_text = tk.Text(
    right_panel,
    bg="#30334b",
    fg="#e8e9f2",
    font=("Arial", 11),
    wrap="word",
    relief="flat",
    padx=15,
    pady=15,
    state="disabled"
)

conversation_text.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 20)
)


# ==========================================
# STARTING MESSAGE
# ==========================================

add_message(
    "Assistant",
    "Hello! I am your voice assistant. "
    "How can I help you?"
)


# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()
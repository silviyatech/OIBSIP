import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# Text-to-speech function
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# Listen to user's voice
def listen():
    try:
        with sr.Microphone(device_index=1) as source:

            # Adjust microphone for background noise
            print("Adjusting for background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            # Listen for user's command
            print("Listening...")

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        # Convert speech to text
        command = recognizer.recognize_google(audio)

        print("You:", command)
        return command.lower()

    except sr.WaitTimeoutError:
        speak("I did not hear anything. Please try again.")
        return ""

    except sr.UnknownValueError:
        speak("Sorry, I could not understand what you said.")
        return ""

    except sr.RequestError:
        speak("Sorry, the speech recognition service is unavailable.")
        return ""

    except OSError:
        speak("There is a problem with the microphone. Please check your microphone.")
        return ""

    except Exception as e:
        print("Error:", e)
        speak("Something went wrong while listening.")
        return ""


# Tell current time
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}.")


# Tell today's date
def tell_date():
    current_date = datetime.datetime.now().strftime("%d %B %Y")
    speak(f"Today's date is {current_date}.")


# Tell a random joke
def tell_joke():
    jokes = [
        "Why did the computer go to the doctor? Because it had a virus!",
        "Why was the computer cold? Because it left its Windows open!",
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ]

    speak(random.choice(jokes))


# Show available commands
def show_help():
    speak("You can ask me for the time or date.")
    speak("You can also ask me to search the web.")
    speak("I can open Google, YouTube, or Spotify.")
    speak("You can also ask me to tell you a joke.")
    speak("Say goodbye or exit to close me.")


# Main voice assistant
def voice_assistant():

    speak("Hello! I am your voice assistant.")
    speak("How can I help you?")

    while True:

        command = listen()

        if command == "":
            continue

        # Greeting
        if "hello" in command or "hi" in command:
            speak("Hello! Nice to talk with you.")

        # Time
        elif "time" in command:
            tell_time()

        # Date
        elif "date" in command or "today" in command:
            tell_date()

        # Search the web
        elif "search" in command:

            search_query = command.replace("search", "").strip()

            if search_query:
                speak(f"Searching for {search_query}.")

                url = (
                    "https://www.google.com/search?q="
                    + search_query.replace(" ", "+")
                )

                webbrowser.open(url)

            else:
                speak("Please tell me what you want me to search for.")

        # Open YouTube
        elif "youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        # Open Google
        elif "google" in command:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        # Open Spotify
        elif "spotify" in command:
            speak("Opening Spotify.")
            webbrowser.open("https://open.spotify.com")

        # Tell a joke
        elif "joke" in command:
            tell_joke()

        # Help
        elif "help" in command:
            show_help()

        # Exit
        elif (
            "exit" in command
            or "quit" in command
            or "goodbye" in command
            or "stop" in command
        ):
            speak("Goodbye! Have a nice day.")
            break

        # Unknown command
        else:
            speak(
                "Sorry, I don't know that command yet. "
                "Say help to hear the available commands."
            )


# Start the program
if __name__ == "__main__":
    voice_assistant()
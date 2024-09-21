import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice commands and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Command received: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech recognition service.")
            return None

def handle_command(command):
    """Handle recognized voice commands."""
    if command is None:
        return False
    
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    
    elif "time" in command:
        now = datetime.datetime.now()
        speak(f"The current time is {now.strftime('%H:%M:%S')}")

    elif "date" in command:
        today = datetime.date.today()
        speak(f"Today's date is {today.strftime('%B %d, %Y')}")

    elif "search" in command:
        speak("What would you like to search for?")
        search_query = listen()  # Listen for the search query
        if search_query:
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            speak(f"Searching the web for {search_query}")
        else:
            speak("Sorry, I didn't catch that.")

    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        return True
    
    else:
        speak("Sorry, I can't help with that command.")
    
    return False

def wake_word_detected(command):
    """Check if the wake word 'Hey Assistant' is in the command."""
    return "hey assistant" in command

def main():
    """Run the voice assistant."""
    speak("Voice assistant is now active. Say 'Hey Assistant' to start.")
    
    while True:
        command = listen()  # Listening for wake word
        if wake_word_detected(command):
            speak("I'm listening...")
            command = listen()  # Listen for the actual command
            if handle_command(command):
                break

if __name__ == "__main__":
    main()

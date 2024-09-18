import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import holidays
from datetime import timedelta

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Function to speak the text using TTS"""
    engine.say(text)
    engine.runAndWait()

def get_command():
    """Function to get the voice command from the user"""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech recognition service.")
            return None

def send_email(subject, body, to_email):
    """Function to send an email"""
    from_email = "your_email@gmail.com"
    password = "your_password"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)

def get_weather(city):
    """Function to get the weather update for a specified city"""
    api_key = "20acb7ff9bf1c0f2ae465715790f3d29"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url).json()
    if response.get('main'):
        temp = response['main']['temp']
        weather_desc = response['weather'][0]['description']
        return f"Current temperature in {city} is {temp}°C with {weather_desc}."
    else:
        return "Sorry, I could not fetch the weather data."

def get_date_info(date_str):
    """Return information about a specific date"""
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date_obj.strftime('%A')
        return f"The date {date_str} falls on a {day_of_week}."
    except ValueError:
        return "Sorry, I could not understand the date format."

def calculate_future_or_past_date(days):
    """Calculate a date that is a number of days from today"""
    today = datetime.datetime.now()
    future_date = today + timedelta(days=days)
    return future_date.strftime('%Y-%m-%d')

def get_holidays(year, country_code='US'):
    """Retrieve public holidays for a given year and country"""
    try:
        year_holidays = holidays.CountryHoliday(country_code, years=year)
        return "\n".join([f"{date}: {name}" for date, name in year_holidays.items()])
    except Exception as e:
        return f"Error retrieving holidays: {e}"

def play_youtube_video(query):
    """Play a YouTube video based on a search query with user selection"""
    api_key = "AIzaSyDSBX7UDMSoZLZAnOjrT_yVgzzo9kJshpI"
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={query}&key={api_key}"
    
    response = requests.get(search_url).json()
    if 'items' in response and len(response['items']) > 0:
        results = response['items']
        speak("Here are the top results:")
        for i, item in enumerate(results):
            title = item['snippet']['title']
            speak(f"Option {i + 1}: {title}")
            print(f"{i + 1}. {title}")
        
        speak("Please say the number of the video you want to play.")
        choice = get_command()
        
        try:
            choice = int(choice)
            if 1 <= choice <= len(results):
                video_id = results[choice - 1]['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                webbrowser.open(video_url)
                speak(f"Playing video: {results[choice - 1]['snippet']['title']}")
            else:
                speak("Invalid choice. Please try again.")
        except (ValueError, IndexError):
            speak("Sorry, I couldn't understand the choice. Please try again.")
    else:
        speak("Sorry, I couldn't find any videos matching your query.")

def get_news():
    """Retrieve the latest news headlines"""
    api_key = "2cb3d6a2183d4dc0ba6f95eda75bef54"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    
    response = requests.get(url).json()
    if response.get('articles'):
        headlines = [article['title'] for article in response['articles'][:5]]
        return "\n".join(headlines)
    else:
        return "Sorry, I could not fetch the news."

def handle_command(command):
    """Function to handle various voice commands"""
    if command:
        if 'hello' in command:
            speak("Hello! How can I assist you today?")
        elif 'time' in command:
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M:%S")
            speak(f"The current time is {time_str}")
        elif 'date' in command:
            today = datetime.date.today()
            date_str = today.strftime("%B %d, %Y")
            speak(f"Today's date is {date_str}")
        elif 'search' in command:
            search_query = command.replace('search', '')
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            speak(f"Here are the search results for {search_query}")
        elif 'email' in command:
            # Example command: "send an email to example@example.com with subject Meeting and body Please join the meeting at 10 AM."
            pass  # Implement email parsing and sending
        elif 'weather' in command:
            speak("Please say the city for which you want the weather update.")
            city_command = get_command()
            if city_command:
                weather_info = get_weather(city_command)
                speak(weather_info)
        elif 'date info' in command:
            date_str = command.split('date info ')[-1]
            info = get_date_info(date_str)
            speak(info)
        elif 'holiday' in command:
            year = int(command.split('holiday ')[-1])
            holidays_info = get_holidays(year)
            speak(holidays_info)
        elif 'calculate' in command:
            days = int(command.split('calculate ')[-1])
            future_date = calculate_future_or_past_date(days)
            speak(f"The date {days} days from now is {future_date}.")
        elif 'play' in command:
            video_query = command.replace('play', '').strip()
            play_youtube_video(video_query)
        elif 'news' in command:
            news_info = get_news()
            speak(f"Here are the latest news headlines: {news_info}")
        elif "exit" in command.lower() or "stop" in command.lower():
            speak("Goodbye!")
            return  # End the loop
        else:
            speak("I am not sure how to help with that command.")

if __name__ == "__main__":
    speak("Voice Assistant is now active. How can I help you?")
    while True:
        command = get_command()
        if command:
            handle_command(command)

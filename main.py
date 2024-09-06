from dotenv import load_dotenv
import os
import requests
from twilio.rest import Client
import schedule
import time

# Load environment variables from .env file
load_dotenv()

# Set up your credentials from environment variables
OWM_API_KEY = os.getenv('OWM_API_KEY')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
YOUR_PHONE_NUMBER = os.getenv('YOUR_PHONE_NUMBER')

# Fetch the weather forecast
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=imperial"
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        main = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        city_name = data["name"]

        return f"Today's weather in {city_name}: {main} ({description}). Temperature: {temp}°F."
    else:
        return "Sorry, I couldn't retrieve the weather data at the moment."

# Send SMS using Twilio
def send_sms(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=YOUR_PHONE_NUMBER
    )

# Define the task
def send_weather_forecast():
    city = "Charlotte, NC"  # City and state
    weather_report = get_weather(city)
    send_sms(weather_report)

# Send a test message immediately
send_weather_forecast()

# Optional: Schedule the task if needed later
# schedule.every().day.at("08:00").do(send_weather_forecast)

# Keep the script running (if you want to maintain this for further testing)
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute if it's time to run the task

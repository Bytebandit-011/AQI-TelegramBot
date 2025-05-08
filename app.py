# Import necessary libraries and configuration variables
from config import API_TOKEN, OWM_API_KEY, api_key
import telebot
import requests

# Initialize the Telegram bot with your API token
bot = telebot.TeleBot(API_TOKEN)

# Handler for the /start command
@bot.message_handler(commands=['start'])
def welcome(message):
    """Send a welcome message when the user starts the bot."""
    bot.send_message(message.chat.id, f"Welcome {message.from_user.first_name}! 🌍\nSend me a city name to get air quality and weather info!")

# Handle all text messages from users
@bot.message_handler(func=lambda message: True)
def handle_city(message):
    """Process city names entered by users."""
    city = message.text.strip()

    if not city:
        bot.reply_to(message, "Please enter a city name:")
        return

    bot.reply_to(message, f'🔍 Searching data for {city}...')

    lat, lon = geocode_address(city, api_key)
    if lat is None or lon is None:
        bot.send_message(message.chat.id, "❌ Could not find the city. Please try another one.")
        return

    air_quality = owm_aqi_quality(lat, lon)
    bot.send_message(message.chat.id, f"🌫 Air Quality for {city}:\n{air_quality}")

def geocode_address(city, api_key):
    """Convert city name to latitude/longitude using OpenCage Geocoder."""
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": city,
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get('results'):
        location = data['results'][0]['geometry']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        return None, None

def owm_aqi_quality(lat, lon):
    """Fetch air quality from OpenWeatherMap Air Pollution API."""
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OWM_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "list" in data and data["list"]:
            aqi_index = data["list"][0]["main"]["aqi"]
            components = data["list"][0]["components"]
            aqi_desc = interpret_owm_aqi(aqi_index)

            msg = (
                f"🔢 AQI Index: {aqi_index}  ({aqi_desc})\n"
                f"🌫️ PM2.5: *{components.get('pm2_5', 'N/A')} µg/m³*\n"
                f"🌫️ PM10: *{components.get('pm10', 'N/A')} µg/m³*\n"
                f"🧪 CO: *{components.get('co', 'N/A')} µg/m³*\n"
                f"💨 NO₂: *{components.get('no2', 'N/A')} µg/m³*"
            )
            return msg
        else:
            return "⚠️ Air quality data unavailable for this location."

    except Exception as e:
        print(f"API Error: {e}")
        return "🚨 Unable to fetch data. Try again later."

def interpret_owm_aqi(aqi_value):
    """Interpret AQI levels from OpenWeatherMap."""
    mapping = {
        1: "Good ✅",
        2: "Fair 🙂",
        3: "Moderate ⚠️",
        4: "Poor 😷",
        5: "Very Poor ☠️"
    }
    return mapping.get(aqi_value, "Unknown")

# Start the bot in polling mode
if __name__ == '__main__':
    print("Bot started polling...")
    bot.polling()

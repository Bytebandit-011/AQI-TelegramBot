# 🌍 Telegram Bot for Air Quality Info

This is a Telegram bot that provides real-time **air quality** and basic **weather data** based on the city name entered by the user. It integrates with the [OpenWeatherMap Air Pollution API](https://openweathermap.org/api/air-pollution) and [OpenCage Geocoder](https://opencagedata.com/api).

---

## 🚀 Features

- Accepts any city name
- Returns air quality index (AQI) with detailed pollutants:
  - PM2.5 🌫️
  - PM10 🌫️
  - CO 🧪
  - NO₂ 💨
- Interprets AQI levels (Good, Fair, etc.)
- Friendly user interaction on Telegram

---

## 🛠️ Tech Stack

- Python 🐍
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- Requests (for HTTP calls)
- OpenWeatherMap API
- OpenCage Geocoding API
- Deployed on: PythonAnywhere.com

---
Output:
<br>
![image](https://github.com/user-attachments/assets/cb0979f7-e791-4f6d-941a-29f504da9a4f)

<br>
## 📦 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/air-quality-telegram-bot.git
cd air-quality-telegram-bot

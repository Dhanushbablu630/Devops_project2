from flask import Flask, render_template, request
import requests, datetime, os

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY", "your_api_key_here")

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    city = "New York"  # default
    if request.method == "POST":
        city = request.form.get("city")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") == 200:
        weather_data = {
            "city": response["name"],
            "country": response["sys"]["country"],
            "temp": response["main"]["temp"],
            "feels_like": response["main"]["feels_like"],
            "humidity": response["main"]["humidity"],
            "wind": response["wind"]["speed"],
            "description": response["weather"][0]["description"].title(),
            "icon": response["weather"][0]["icon"],
            "sunrise": datetime.datetime.fromtimestamp(response["sys"]["sunrise"]).strftime("%H:%M"),
            "sunset": datetime.datetime.fromtimestamp(response["sys"]["sunset"]).strftime("%H:%M")
        }

    return render_template("index.html", weather=weather_data, city=city)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

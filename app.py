import requests
from flask import Flask, request, jsonify
import geocoder
import os

app = Flask(__name__)

API_KEY = "6ac781cdf5ef55a8b457c84bb73ce3fd"  # مفتاح OpenWeather

def suggest_clothes(temp, weather_desc):
    suggestions = []
    if temp >= 30:
        suggestions.append("تيشرت خفيف وشورت")
    elif temp >= 20:
        suggestions.append("قميص وبنطلون خفيف")
    elif temp >= 10:
        suggestions.append("جاكيت خفيف")
    else:
        suggestions.append("جاكيت ثقيل أو معطف")
    if "rain" in weather_desc.lower():
        suggestions.append("مظلة أو جاكيت ضد المطر")
    if "snow" in weather_desc.lower():
        suggestions.append("جزمة ومعدات للتدفئة")
    return suggestions

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    ip = request.args.get("ip")
    lat = lon = None

    if city:
        g = geocoder.osm(city)
        if g.ok:
            lat, lon = g.latlng
        else:
            return jsonify({"error": "City not found"}), 404
    elif ip:
        g = geocoder.ip(ip)
        if g.ok:
            lat, lon = g.latlng
        else:
            return jsonify({"error": "IP not found"}), 404
    else:
        return jsonify({"error": "Please provide city or IP"}), 400

    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    temp = response['current']['temp']
    desc = response['current']['weather'][0]['description']
    clothes = suggest_clothes(temp, desc)

    return jsonify({
        "latitude": lat,
        "longitude": lon,
        "temperature": temp,
        "description": desc,
        "clothes_suggestion": clothes
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

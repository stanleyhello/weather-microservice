import zmq
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1"
CITY = "Corvallis"

def is_valid_date(input_str):
    try:
        datetime.strptime(input_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_forecast(date_str):
    try:
        response = requests.get(
            f"{BASE_URL}/forecast.json",
            params={"key": API_KEY, "q": CITY, "dt": date_str},
            headers={"Accept": "application/json"},
            timeout=1.5
        )
        print("Status code:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type"))

        if "application/json" not in response.headers.get("Content-Type", ""):
            return "Error: Unexpected response format. Check your API key or date."

        data = response.json()
        if "error" in data:
            return f"Error: {data['error']['message']}"

        forecast_day = data["forecast"]["forecastday"][0]["day"]
        temp = forecast_day["avgtemp_f"]
        cond = forecast_day["condition"]["text"]
        return f"{temp} F, {cond}"
    except Exception as e:
        return f"Error:: {str(e)}"

def get_current_weather(city_name):
    try:
        response = requests.get(
            f"{BASE_URL}/current.json",
            params={"key": API_KEY, "q": city_name},
            headers={"Accept": "application/json"},
            timeout=1.5
        )
        data = response.json()
        if "error" in data:
            return f"Error: {data['error']['message']}"
        temp = data["current"]["temp_f"]
        cond = data["current"]["condition"]["text"]
        return f"{temp} F, {cond}"
    except Exception as e:
        return f"Error:: {str(e)}"

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("Weather microservice is running...")

    while True:
        try:
            input_str = socket.recv_string()
            print("Received request:", input_str)
            result = get_forecast(input_str) if is_valid_date(input_str) else get_current_weather(input_str)
        except Exception as e:
            result = f"Error: {str(e)}"
        socket.send_string(result)

if __name__ == "__main__":
    main()

import requests

key = "082658df42df90bb7885de12f150a561"

def get_city_coordinates(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
        else:
            return None, None

def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"]
        }
        return weather_info
    else:
        return None
    
while True:
    city = input("Enter a city name (or type 'exit' to quit): ")
    if city.lower() == 'exit':
        break
    
    lat, lon = get_city_coordinates(city)
    weather = get_weather(lat, lon)

    print(weather)
    if weather:
        print(f"City: {weather['city']}")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Weather: {weather['weather']}")
    else:
        print("City not found. Please try again.")
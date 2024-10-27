import requests
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO


def get_weather(city):
    api_key = 'API_KEY'

    try:

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}"
        weather_data = requests.get(url)


        data = weather_data.json()


        if weather_data.status_code == 401:
            return {"error": "Invalid API key. Please check your API key and make sure it's activated."}

        if weather_data.status_code == 429:
            return {"error": "Too many requests. Please wait before trying again."}

        if weather_data.status_code != 200:
            return {"error": f"{data.get('message', 'Unknown error')} (Status code: {weather_data.status_code})"}

        if data.get('cod') == '404':
            return {"error": "City not found. Please check the city name."}


        weather = data.get('weather', [{}])[0].get('main', 'N/A')
        description = data.get('weather', [{}])[0].get('description', 'N/A').capitalize()
        icon_code = data.get('weather', [{}])[0].get('icon', '01d')
        temp = round(data.get('main', {}).get('temp', 0))


        timestamp = data.get('dt', 0)
        local_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        return {
            "city": city.capitalize(),
            "weather": weather,
            "description": description,
            "temperature": temp,
            "time": local_time,
            "icon_code": icon_code
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


def visualize_weather(data):
    if "error" in data:
        print(data["error"])
        return

    city = data["city"]
    weather = data["weather"]
    description = data["description"]
    temp = data["temperature"]
    time = data["time"]
    icon_code = data["icon_code"]


    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    icon_data = requests.get(icon_url)
    icon_img = Image.open(BytesIO(icon_data.content))


    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis('off')


    ax.imshow(icon_img, aspect='auto', extent=[0.3, 0.7, 0.7, 1])


    text = (
        f"City: {city}\n"
        f"Weather: {weather} ({description})\n"
        f"Temperature: {temp}ºF\n"
        f"Time of Data: {time}"
    )
    plt.text(0.5, 0.4, text, ha='center', va='center', fontsize=12, fontweight='bold', wrap=True)

    plt.show()


def main():
    while True:
        city = input("Enter city (or 'quit' to exit): ").strip()
        if city.lower() == 'quit':
            break
        data = get_weather(city)


        if "error" in data:
            print(data["error"])
        else:
            print(
                f"\nCity: {data['city']}\n"
                f"Weather: {data['weather']} ({data['description']})\n"
                f"Temperature: {data['temperature']}ºF\n"
                f"Time of Data: {data['time']}\n"
            )

        visualize_weather(data)


if __name__ == "__main__":
    main()

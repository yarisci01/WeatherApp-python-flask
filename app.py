from flask import Flask, render_template, request
import requests

app = Flask(__name__)
api_key = "9b4cfeda935a584f9002681aadaf5b2d"

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15)

def translate_weather_description(description):
    translations = {
        'clear': 'Açık',
        'clouds': 'Bulutlu',
        'drizzle': 'Çisenti',
        'rain': 'Yağmurlu',
        'thunderstorm': 'Gök gürültülü fırtına',
        'snow': 'Karlı',
        'mist': 'Sisli',
        'fog': 'Sisli',
        'haze': 'Dumanlı',
        'smoke': 'Dumanlı',
        'dust': 'Tozlu',
        'sand': 'Kumlu',
        'ash': 'Kül',
        'squall': 'Fırtına',
        'tornado': 'Tornado',
        'overcast clouds': 'Kapalı bulutlu',
        'broken clouds': 'Parçalı bulutlu',
        'few clouds': 'Az bulutlu',
        'scattered clouds': 'Dağınık bulutlu',
        'moderate rain': 'Orta şiddetli yağmur',
        'heavy intensity rain': 'Yoğun yağışlı',
        'light intensity shower rain': 'Hafif şiddetli sağanak yağış',
        'shower rain': 'Sağanak yağışlı',
        'light rain': 'Hafif yağmurlu',
        'freezing rain': 'Dondurucu yağmur',
        'thunderstorm with rain': 'Yağmurlu gök gürültülü fırtına',
        'thunderstorm with heavy rain': 'Yoğun yağmurlu gök gürültülü fırtına',
        'thunderstorm with light rain': 'Hafif yağmurlu gök gürültülü fırtına',
        'thunderstorm with drizzle': 'Çisentili gök gürültülü fırtına',
        'heavy intensity drizzle': 'Yoğun çisenti',
        'drizzle rain': 'Çisenti yağışlı',
        'light intensity drizzle rain': 'Hafif şiddetli çisenti yağışlı',
        'shower drizzle': 'Sağanak çisenti yağışlı',
        'light snow': 'Hafif kar yağışlı',
        'heavy snow': 'Yoğun kar yağışlı',
        'sleet': 'Sulu kar',
        'shower sleet': 'Sağanak sulu kar',
        'light shower sleet': 'Hafif sağanak sulu kar',
        'rain and snow': 'Yağmur ve kar',
        'light shower snow': 'Hafif sağanak kar yağışlı',
        'shower snow': 'Sağanak kar yağışlı',
        'clear sky': 'Açık gökyüzü',
    }
    return translations.get(description.lower(), description)

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        description = weather_data['weather'][0]['description']
        translated_description = translate_weather_description(description)
        icon_code = weather_data['weather'][0]['icon']
        temperature_kelvin = weather_data['main']['temp']
        temperature_celsius = kelvin_to_celsius(temperature_kelvin)
        return {'description': translated_description, 'icon': icon_code, 'temperature': temperature_celsius}
    else:
        print(response.json())  # Hata durumunda API yanıtını terminalde göster
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city'].upper()

    # Get weather information for the city
    result = get_weather(city)

    if result:
        return render_template('result.html', result=result, city=city)
    else:
        return render_template('not_found.html', city=city)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import requests


app = Flask('__name__')

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        input_city = request.form.get("city")
        input_city = ''.join(input_city.split(' '))
        resp = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+input_city+'&APPID=73456b857deeee4b59cb952ce9657a38')
        weather_details = resp.json()
        if weather_details['cod'] == 200:
            return render_template('weatherapp.html', 
                city=weather_details['name'], 
                country=weather_details['sys']['country'], 
                icon='http://openweathermap.org/img/wn/'+weather_details['weather'][0]['icon']+'@2x.png',
                temp = str(int(round(weather_details['main']['temp'] - 273.15, 0))) +'C',
                mintemp = str(int(round(weather_details['main']['temp_min'] - 273.15, 0))) +'C',
                maxtemp = str(int(round(weather_details['main']['temp_max'] - 273.15, 0))) +'C',
                humid = weather_details['main']['humidity'],
                desc = weather_details['weather'][0]['description'],
                code = 200
                )
        elif int(weather_details['cod']) == 404:
            return render_template('weatherapp.html', code=404)
        else:
            return render_template('weatherapp.html', code=-1, error=weather_details['cod'])

        
    if request.method == 'GET':
        return render_template('weatherapp.html', code=0)
    

if __name__ == '__main__':
    app.run()
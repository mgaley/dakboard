from flask import Flask, jsonify
import urllib.request
import urllib.error
import json
import os
# AmbientWeather API configuration
AMBIENT_WEATHER_API_KEY = os.getenv('AMBIENTWEATHER_KEY')
AMBIENT_WEATHER_API_URL = f'https://api.ambientweather.net/v1/devices?apiKey={AMBIENT_WEATHER_API_KEY}'

app = Flask(__name__)


def fetch_weather_data():
    """Fetch and format weather data from AmbientWeather API"""
    try:
        # Fetch data from AmbientWeather API
        with urllib.request.urlopen(AMBIENT_WEATHER_API_URL) as response:
            data = json.loads(response.read().decode())
        
        if not data or len(data) == 0:
            return {
                'error': 'No weather station data found',
                'temperature': None,
                'humidity': None
            }, 404

        # Get the first device's last data (most recent reading)
        device = data[0]
        last_data = device.get('lastData', {})

        # Format data for Dakboard
        # Temperature is in Fahrenheit (tempf), humidity is a percentage
        weather_data = {
            'temperature': last_data.get('tempf'),
            'humidity': last_data.get('humidity'),
            'temperatureUnit': '°F',
            'humidityUnit': '%',
            'lastUpdated': last_data.get('date') or None,
            # Additional useful data that might be interesting for Dakboard
            'feelsLike': last_data.get('feelsLike'),
            'dewPoint': last_data.get('dewPoint'),
            'pressure': last_data.get('baromrelin'),
            'pressureUnit': 'inHg'
        }

        return weather_data, 200
        
    except urllib.error.HTTPError as e:
        return {
            'error': f'HTTP Error: {e.code} - {e.reason}',
            'temperature': None,
            'humidity': None
        }, 500
        
    except urllib.error.URLError as e:
        return {
            'error': f'URL Error: {str(e)}',
            'temperature': None,
            'humidity': None
        }, 500
        
    except Exception as e:
        return {
            'error': f'Failed to fetch weather data: {str(e)}',
            'temperature': None,
            'humidity': None
        }, 500


@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Flask route handler for weather data"""
    data, status_code = fetch_weather_data()
    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response, status_code


# Vercel serverless function handler
# Vercel Python functions use BaseHTTPRequestHandler, but we'll export Flask app for compatibility
# For Vercel, we need to use the @vercel/python builder or create a handler
# This is a simple adapter that works with Vercel's serverless function format
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Use Flask app to handle the request
        with app.test_request_context(path=self.path, method='GET'):
            data, status_code = fetch_weather_data()
            response = jsonify(data)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET'
            
            # Send response
            self.send_response(status_code)
            for header, value in response.headers:
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.get_data())


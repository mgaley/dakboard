# Dakboard Weather Integration

This project provides a serverless API endpoint that fetches data from AmbientWeather and formats it for use with Dakboard's Fetch widget. Built with Python.

## Setup

1. Install Vercel CLI (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. Deploy to Vercel:
   ```bash
   vercel
   ```

## Usage

Once deployed, the weather data will be available at:
```
https://your-project.vercel.app/api/weather
```

### Dakboard Configuration

1. In your Dakboard account, add a "Fetch" widget
2. Set the data source URL to: `https://your-project.vercel.app/api/weather`
3. The widget will display the temperature and humidity data

## API Response Format

The API returns JSON in the following format:

```json
{
  "temperature": 72.5,
  "humidity": 45,
  "temperatureUnit": "°F",
  "humidityUnit": "%",
  "lastUpdated": "2024-01-15T10:30:00.000Z",
  "feelsLike": 70.2,
  "dewPoint": 50.1,
  "pressure": 29.92,
  "pressureUnit": "inHg"
}
```

## Local Development

For local testing, you can use Vercel's dev server:
```bash
vercel dev
```

The API will be available at `http://localhost:3000/api/weather`

## Technology

- **Language**: Python 3.9
- **Framework**: Flask (adapted for Vercel serverless functions)
- **Dependencies**: Flask (see requirements.txt)


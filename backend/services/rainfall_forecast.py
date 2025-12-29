"""
Rainfall Forecast Service
Uses Open-Meteo API (free, no API key required)
"""
import requests
from datetime import datetime, timedelta


def get_rainfall_forecast(latitude=16.8661, longitude=96.1951, days=7):
    """
    Get rainfall forecast from Open-Meteo API
    
    Args:
        latitude: Location latitude (default: Yangon, Myanmar)
        longitude: Location longitude (default: Yangon, Myanmar)
        days: Number of forecast days (max 16)
        
    Returns:
        Dictionary with forecast data
    """
    try:
        # Open-Meteo API endpoint (free, no API key needed)
        url = "https://api.open-meteo.com/v1/forecast"
        
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'daily': 'precipitation_sum,precipitation_probability_max,weathercode',
            'current': 'temperature_2m,precipitation,weathercode',
            'timezone': 'auto',
            'forecast_days': min(days, 16)  # API limit is 16 days
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Parse current weather
        current = data.get('current', {})
        current_weather = {
            'temperature': current.get('temperature_2m', 0),
            'precipitation': current.get('precipitation', 0),
            'weathercode': current.get('weathercode', 0),
            'time': current.get('time', '')
        }
        
        # Parse daily forecast
        forecasts = []
        daily = data.get('daily', {})
        dates = daily.get('time', [])
        precipitation = daily.get('precipitation_sum', [])
        probability = daily.get('precipitation_probability_max', [])
        weathercodes = daily.get('weathercode', [])
        
        for i in range(len(dates)):
            forecasts.append({
                'date': dates[i],
                'precipitation_mm': precipitation[i] if precipitation[i] is not None else 0,
                'probability_percent': probability[i] if probability[i] is not None else 0,
                'weathercode': weathercodes[i] if weathercodes and weathercodes[i] is not None else 0,
                'impact': get_rainfall_impact_score(precipitation[i] if precipitation[i] else 0)
            })
        
        return {
            'success': True,
            'current': current_weather,
            'forecast': forecasts,
            'location': {'latitude': latitude, 'longitude': longitude}
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rainfall forecast: {str(e)}")
        return {'success': False, 'error': str(e)}
    except Exception as e:
        print(f"Error parsing rainfall data: {str(e)}")
        return {'success': False, 'error': str(e)}


def get_rainfall_impact_score(precipitation_mm):
    """
    Calculate potential flood impact based on rainfall amount
    
    Args:
        precipitation_mm: Rainfall in millimeters
        
    Returns:
        Impact level string
    """
    if precipitation_mm < 10:
        return 'low'
    elif precipitation_mm < 30:
        return 'moderate'
    elif precipitation_mm < 50:
        return 'high'
    else:
        return 'severe'


def get_weather_description(weathercode):
    """
    Convert WMO weather code to description
    
    Args:
        weathercode: WMO weather code
        
    Returns:
        Weather description string
    """
    weather_codes = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Foggy',
        48: 'Depositing rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        71: 'Slight snow',
        73: 'Moderate snow',
        75: 'Heavy snow',
        80: 'Slight rain showers',
        81: 'Moderate rain showers',
        82: 'Violent rain showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with slight hail',
        99: 'Thunderstorm with heavy hail'
    }
    return weather_codes.get(weathercode, 'Unknown')

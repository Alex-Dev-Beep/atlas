import requests

def find_city(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    results = data.get("results", [])

    if not results:
        return None

    city = results[0]

    return {
        "name": city["name"],
        "country": city.get("country", "Unknown"),
        "latitude": city["latitude"],
        "longitude": city["longitude"]
    }

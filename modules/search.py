
from modules.geocoding import find_city
from modules.weather import get_weather


def search_city(city_input):

    try:
        city = find_city(city_input)

        if city is None:
            return {
                "success": False,
                "error": "City not found."
            }

        weather = get_weather(
            city["latitude"],
            city["longitude"]
        )

        return {
            "success": True,
            "city": city,
            "weather": weather
        }

    except Exception as error:
        return {
            "success": False,
            "error": f"Error: {str(error)[:55]}"
        }

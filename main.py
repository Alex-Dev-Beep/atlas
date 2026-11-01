
import pygame
import sys

from modules.geocoding import find_city
from modules.weather import get_weather


pygame.init()

WIDTH, HEIGHT = 800, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ATLAS")

clock = pygame.time.Clock()

BACKGROUND = (17, 24, 35)
PANEL = (29, 40, 55)
WHITE = (240, 245, 250)
GRAY = (155, 170, 185)
BLUE = (55, 125, 190)

title_font = pygame.font.SysFont("Arial", 32, bold=True)
font = pygame.font.SysFont("Arial", 21)
small_font = pygame.font.SysFont("Arial", 16)

city_input = ""
selected_city = None
weather_data = None
message = "Enter a city name and press ENTER"
loading = False


def draw_text(text, font, color, x, y):
    surface = font.render(str(text), True, color)
    screen.blit(surface, (x, y))


def draw_interface():

    screen.fill(BACKGROUND)

    draw_text("ATLAS", title_font, WHITE, 35, 25)
    draw_text(
        "City Simulator",
        small_font, GRAY, 38, 65
    )

    # Search panel
    pygame.draw.rect(
        screen, PANEL,
        (35, 110, 730, 90),
        border_radius=10
    )

    draw_text("CITY SEARCH", small_font, GRAY, 55, 125)

    pygame.draw.rect(
        screen, (40, 55, 72),
        (55, 150, 690, 38),
        border_radius=5
    )

    draw_text(
        city_input + "|",
        font, WHITE, 65, 157
    )

    # Weather panel
    pygame.draw.rect(
        screen, PANEL,
        (35, 220, 730, 240),
        border_radius=10
    )

    draw_text("WEATHER ANALYSIS", small_font, GRAY, 55, 240)

    if selected_city and weather_data:

        draw_text(
            selected_city["name"] + ", " +
            selected_city["country"],
            title_font, WHITE, 55, 275
        )

        draw_text(
            f"Temperature: {weather_data['temperature_2m']} °C",
            font, WHITE, 55, 335
        )

        draw_text(
            f"Feels like: {weather_data['apparent_temperature']} °C",
            font, WHITE, 55, 370
        )

        draw_text(
            f"Humidity: {weather_data['relative_humidity_2m']}%",
            font, WHITE, 400, 335
        )

        draw_text(
            f"Precipitation: {weather_data['precipitation']} mm",
            font, WHITE, 400, 370
        )

        draw_text(
            f"Wind: {weather_data['wind_speed_10m']} km/h",
            font, WHITE, 400, 405
        )

        draw_button(
            
        )

    else:
        draw_text(message, font, GRAY, 55, 290)


def search_city():

    global selected_city, weather_data, message

    try:
        message = "Searching..."
        city = find_city(city_input)

        if city is None:
            selected_city = None
            weather_data = None
            message = "City not found."
            return

        weather = get_weather(
            city["latitude"],
            city["longitude"]
        )

        selected_city = city
        weather_data = weather

        message = "Weather loaded successfully."

    except Exception as error:
        selected_city = None
        weather_data = None
        message = f"Error: {str(error)[:55]}"


# Main loop
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                if city_input.strip():
                    search_city()

            elif event.key == pygame.K_BACKSPACE:
                city_input = city_input[:-1]

            else:
                if event.unicode.isprintable():
                    city_input += event.unicode

    draw_interface()

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()

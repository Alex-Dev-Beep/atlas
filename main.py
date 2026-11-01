
import pygame
import sys
import threading

from modules.geocoding import find_city
from modules.weather import get_weather

from modules.interface import (
    draw_button,
    draw_text,
    BACKGROUND,
    BLUE,
    PANEL,
    WHITE,
    GRAY,
    DEFAULT_CURSOR,
    HOVER_CURSOR
)

pygame.init()

# --------------------------------------------------
# WINDOW
# --------------------------------------------------

WIDTH, HEIGHT = 800, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ATLAS")

clock = pygame.time.Clock()

# --------------------------------------------------
# FONTS
# --------------------------------------------------

title_font = pygame.font.SysFont("Arial", 32, bold=True)
font = pygame.font.SysFont("Arial", 21)
small_font = pygame.font.SysFont("Arial", 16)

# --------------------------------------------------
# APPLICATION STATE
# --------------------------------------------------

city_input = ""
selected_city = None
weather_data = None

message = "Enter a city name and press ENTER"
loading = False

# Thread communication
search_result = None
search_error = None


# --------------------------------------------------
# SEARCH
# --------------------------------------------------

def run_search(city):
    global search_result, search_error

    try:
        found_city = find_city(city)

        if found_city is None:
            search_result = None
            search_error = "City not found."
            return

        weather = get_weather(
            found_city["latitude"],
            found_city["longitude"]
        )

        search_result = (found_city, weather)
        search_error = None

    except Exception as error:
        search_result = None
        search_error = str(error)


def start_search(city):
    global loading, search_result, search_error, message

    if loading:
        return

    loading = True
    search_result = None
    search_error = None
    message = "Searching..."

    thread = threading.Thread(
        target=run_search,
        args=(city,),
        daemon=True
    )

    thread.start()


def update_search():
    global loading
    global selected_city, weather_data, message
    global search_result, search_error

    if not loading:
        return

    if search_result is not None:

        selected_city, weather_data = search_result

        message = "Weather loaded successfully."
        loading = False

        search_result = None

    elif search_error is not None:

        selected_city = None
        weather_data = None

        message = search_error
        loading = False

        search_error = None


# --------------------------------------------------
# INTERFACE
# --------------------------------------------------

def draw_interface():

    button_rect = None

    screen.fill(BACKGROUND)

    # Header
    draw_text(
        "ATLAS",
        title_font,
        WHITE,
        35,
        25,
        screen
    )

    draw_text(
        "City Simulator",
        small_font,
        GRAY,
        38,
        65,
        screen
    )

    # Search panel
    pygame.draw.rect(
        screen,
        PANEL,
        (35, 110, 730, 90),
        border_radius=10
    )

    draw_text(
        "CITY SEARCH",
        small_font,
        GRAY,
        55,
        125,
        screen
    )

    pygame.draw.rect(
        screen,
        (40, 55, 72),
        (55, 150, 690, 38),
        border_radius=5
    )

    draw_text(
        city_input + ("|" if not loading else ""),
        font,
        WHITE,
        65,
        157,
        screen
    )

    # Weather panel
    pygame.draw.rect(
        screen,
        PANEL,
        (35, 220, 730, 240),
        border_radius=10
    )

    draw_text(
        "WEATHER ANALYSIS",
        small_font,
        GRAY,
        55,
        240,
        screen
    )

    if selected_city and weather_data:

        draw_text(
            selected_city["name"] + ", " + selected_city["country"],
            title_font,
            WHITE,
            55,
            275,
            screen
        )

        draw_text(
            f"Temperature: {weather_data['temperature_2m']} °C",
            font,
            WHITE,
            55,
            335,
            screen
        )

        draw_text(
            f"Feels like: {weather_data['apparent_temperature']} °C",
            font,
            WHITE,
            55,
            370,
            screen
        )

        draw_text(
            f"Humidity: {weather_data['relative_humidity_2m']}%",
            font,
            WHITE,
            400,
            335,
            screen
        )

        draw_text(
            f"Precipitation: {weather_data['precipitation']} mm",
            font,
            WHITE,
            400,
            370,
            screen
        )

        draw_text(
            f"Wind: {weather_data['wind_speed_10m']} km/h",
            font,
            WHITE,
            400,
            405,
            screen
        )

        # History button
        button_rect = draw_button(
            "Show history",
            font,
            WHITE,
            55,
            415,
            screen
        )

    else:

        draw_text(
            message,
            font,
            GRAY,
            55,
            290,
            screen
        )

    return button_rect


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:

                if city_input.strip():
                    start_search(city_input.strip())

            elif event.key == pygame.K_BACKSPACE:

                city_input = city_input[:-1]

            else:

                if event.unicode.isprintable() and not loading:
                    city_input += event.unicode

    # Update asynchronous search results
    update_search()

    # Render interface and obtain button rectangle
    button_rect = draw_interface()

    # Cursor hover detection
    if (
        button_rect is not None
        and button_rect.collidepoint(pygame.mouse.get_pos())
    ):
        pygame.mouse.set_cursor(HOVER_CURSOR)

    else:
        pygame.mouse.set_cursor(DEFAULT_CURSOR)

    pygame.display.flip()

    clock.tick(60)


# --------------------------------------------------
# EXIT
# --------------------------------------------------

pygame.quit()
sys.exit()

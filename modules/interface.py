import pygame

BACKGROUND = (17, 24, 35)
PANEL = (29, 40, 55)
WHITE = (240, 245, 250)
GRAY = (155, 170, 185)
BLUE = (55, 125, 190)

DEFAULT_CURSOR = pygame.SYSTEM_CURSOR_ARROW
HOVER_CURSOR = pygame.SYSTEM_CURSOR_HAND

def draw_text(text, font, color, x, y, screen):
    surface = font.render(str(text), True, color)
    screen.blit(surface, (x, y))

def draw_button(text, font, color, x, y, screen):
    surface = font.render(str(text), True, color)

    button_rect = pygame.Rect(
        x - 10,
        y - 5,
        surface.get_width() + 20,
        surface.get_height() + 10
    )

    hovered = is_hovered(button_rect)

    button_color = (65, 100, 135) if hovered else BLUE

    pygame.draw.rect(
        screen,
        BLUE,
        button_rect,
        border_radius=8
    )

    screen.blit(surface, (x, y))

    return button_rect

def is_hovered(rect):
    return rect.collidepoint(pygame.mouse.get_pos())
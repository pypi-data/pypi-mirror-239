import typing as t
import sys

# TODO rename colors variables to background, forground, accent, error, etc...
black_theme = True

NONE = (-255, 0, 0, 255)
TRANSPARENT = (0, 0, 0, 0)
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)

if (app_module := sys.modules.get('dearpyapp.application')) and getattr(app_module, '_light_theme'):
    GRAY_0 = (255, 255, 255, 255)  # not used
    GRAY_1 = (255, 255, 255, 255)  # not used
    GRAY_2 = (255, 255, 255, 255)
    GRAY_3 = (240, 240, 240, 255)
    GRAY_4 = (220, 220, 220, 255)
    GRAY_5 = (210, 210, 210, 255)
    GRAY_6 = (200, 200, 200, 255)
    GRAY_8 = (155, 155, 155, 255)
    GRAY_10 = (150, 150, 150, 255)
    GRAY_12 = (130, 130, 130, 255)
    GRAY_16 = (120, 120, 120, 255)
    GRAY_14 = (115, 115, 115, 255)
    GRAY_18 = (43, 43, 43, 255)
    GRAY_20 = (32, 32, 32, 255)
    GRAY_22 = (15, 15, 15, 255)
    GRAY_25 = (0, 0, 0, 255)

    BLUE_4 = (180, 230, 255, 255)
    BLUE_9 = (175, 226, 251, 255)
    BLUE_12 = (129, 194, 247, 255)
    BLUE_15 = (100, 163, 217, 255)
    BLUE_18 = (18, 81, 153, 255)

    YELLOW_17 = (220, 110, 0, 255)
    YELLOW_19 = (255, 115, 0, 255)

    RED_9 = (236, 173, 173, 255)
    RED_20 = (200, 30, 41, 255)
    RED_23 = (160, 20, 30, 255)

    GREEN_6 = (170, 235, 170, 255)
    GREEN_18 = (30, 130, 30, 255)
    GREEN_20 = (17, 110, 25, 255)
    GREEN_23 = (10, 85, 25, 255)

else:
    GRAY_0 = (0, 0, 0, 255)  # not used
    GRAY_1 = (17, 17, 17, 255)  # not used
    GRAY_2 = (25, 25, 25, 255)
    GRAY_3 = (32, 32, 32, 255)
    GRAY_4 = (43, 43, 43, 255)
    GRAY_5 = (50, 50, 50, 255)
    GRAY_6 = (65, 65, 65, 255)
    GRAY_8 = (87, 87, 87, 255)
    GRAY_10 = (100, 100, 100, 255)
    GRAY_12 = (120, 120, 120, 255)
    GRAY_14 = (140, 140, 140, 255)
    GRAY_16 = (160, 160, 160, 255)
    GRAY_18 = (180, 180, 180, 255)
    GRAY_20 = (200, 200, 200, 255)
    GRAY_22 = (220, 220, 220, 255)
    GRAY_25 = (240, 240, 240, 255)

    BLUE_4 = (25, 35, 45, 255)
    BLUE_9 = (38, 70, 95, 255)
    BLUE_12 = (43, 82, 120, 255)
    BLUE_15 = (55, 110, 155, 255)
    BLUE_18 = (68, 140, 186, 255)

    YELLOW_17 = (173, 173, 75, 255)
    YELLOW_19 = (190, 190, 75, 255)

    RED_9 = (90, 30, 20, 255)
    RED_20 = (200, 70, 50, 255)
    RED_23 = (235, 85, 65, 255)

    GREEN_6 = (30, 65, 35, 255)
    GREEN_18 = (95, 180, 90, 255)
    GREEN_20 = (100, 200, 95, 255)
    GREEN_23 = (105, 230, 100, 255)


def to_hex_rgb(color: t.Union[list, tuple]):
    return ''.join((f'{num:02x}' for index, num in enumerate(color) if index != 3))



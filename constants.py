import pygame

## Presets
# Screen
WIDTH, HEIGHT = 1920, 1000
BACKGROUND_COLOR = (25, 15, 35)  # Halloween dark purple background

# Colors - Light Halloween Theme (easier on eyes)
WHITE = (255, 255, 255)
BLACK = (40, 40, 50)  # Softer black
GREY = (120, 120, 130)
DARK_PURPLE = (140, 110, 160)  # Much lighter purple
GREEN = (180, 120, 70)  # Lighter orange-brown for correct letters
YELLOW = (255, 200, 100)  # Softer orange for partial matches
TILE_BORDER_COLOR = (160, 140, 170)
LETTER_COLOR = (50, 50, 60)  # Dark text on light backgrounds
KEY_COLOR = (180, 160, 190)  # Light purple-grey
LIGHT_ORANGE = (255, 180, 120)
ORANGE = (255, 150, 100)  # Softer orange
LIGHT_PURPLE = (200, 170, 230)  # Much lighter purple
PURPLE = (150, 120, 180)  # Lighter purple
HALLOWEEN_BACKGROUND = (240, 230, 245)  # Very light purple background
PUMPKIN_ORANGE = (255, 170, 100)  # Lighter pumpkin color
SPOOKY_GREEN = (120, 180, 120)  # Softer green
BLOOD_RED = (200, 100, 100)  # Softer red for accents

KEYBOARD_LAYOUT = ["Q W E R T Y U I O P".split(), 
                   "A S D F G H J K L".split(),
                   ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "DEL"]]

# Tiles
GRID_ROWS = 6
TILE_SIZE = 100
MARGIN = 10
START_Y = 100

# On-screen keyboard
KEY_WIDTH = 55
KEY_HEIGHT = 75
KEY_MARGIN = 6
SPECIAL_KEY_WIDTH = 90

# --- Font Sizes ---
LETTER_FONT_SIZE = 60
KEY_FONT_SIZE = 30
SPECIAL_KEY_FONT_SIZE = 20
MESSAGE_FONT_SIZE = 60  # Increased for bigger title
TARGET_FONT_SIZE = 30
HINT_FONT_SIZE = 24
DEFINITION_FONT_SIZE = 18
DEFINITION_TITLE_FONT_SIZE = 22

# Dictionary Hint Configuration
DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
HINT_PANEL_WIDTH = 300
HINT_PANEL_MARGIN = 20
HINT_TEXT_MARGIN = 15
MAX_DEFINITION_LENGTH = 80  # Characters per line for word wrapping

# Path Length Configuration (for game difficulty balance)
MAX_PATH_GENERATION_RETRIES = 3
MIN_PATH_LENGTH = 3  # Minimum path length for any word size (at least 3 steps)

# Timer Display Configuration
TIMER_FONT_SIZE = 28
TIMER_PANEL_WIDTH = 200
TIMER_PANEL_HEIGHT = 120
TIMER_PANEL_MARGIN = 20

# Layout Ratios
TOP_MARGIN_PX = 150
BOTTOM_MARGIN_PX = 300
MARGIN_RATIO = 0.1
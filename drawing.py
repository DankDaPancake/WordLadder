import pygame
import constants as const 

## Initialize application
pygame.font.init()
LETTER_FONT = None
MESSAGE_FONT = None
KEY_FONT = None
TARGET_FONT = None
SPECIAL_KEY_FONT = None
HINT_FONT = None

def initialize_fonts():
    global LETTER_FONT, MESSAGE_FONT, KEY_FONT, TARGET_FONT, SPECIAL_KEY_FONT, HINT_FONT
    LETTER_FONT = pygame.font.SysFont(None, const.LETTER_FONT_SIZE)
    MESSAGE_FONT = pygame.font.SysFont(None, const.MESSAGE_FONT_SIZE)
    KEY_FONT = pygame.font.SysFont(None, const.KEY_FONT_SIZE)
    TARGET_FONT = pygame.font.SysFont(None, const.LETTER_FONT_SIZE)
    SPECIAL_KEY_FONT = pygame.font.SysFont(None, 20)
    HINT_FONT = pygame.font.SysFont(None, const.HINT_FONT_SIZE)

def create_key_rects():
    key_rects = {}
    
    for i, row in enumerate(const.KEYBOARD_LAYOUT):
        # Position the keyboard rows
        row_width = len(row) * (const.KEY_WIDTH + const.KEY_MARGIN) - const.KEY_MARGIN
        if i == 2:
            row_width += 2 * (const.SPECIAL_KEY_WIDTH - const.KEY_WIDTH)  
                        
        # Position of first key on row
        x = (const.WIDTH - row_width) // 2
        y = const.KEYBOARD_START_Y + i * (const.KEY_HEIGHT + const.KEY_MARGIN)
        
        for key_char in row:
            if len(key_char) > 1:
                key_width = const.SPECIAL_KEY_WIDTH
            else:
                key_width = const.KEY_WIDTH
            
            # Store key's rect information
            key_rect = pygame.Rect(x, y, key_width, const.KEY_HEIGHT)
            key_rects[key_char] = key_rect
            
            x += key_width + const.KEY_MARGIN
        
    return key_rects
    
    
def draw_target_display(SCREEN, start_word, target_word):
    start_text = TARGET_FONT.render(f"Start: {start_word}", True, const.WHITE)
    target_text = TARGET_FONT.render(f"Target: {target_word}", True, const.WHITE)
    
    start_rect = start_text.get_rect(center = (const.WIDTH // 2, 30))
    target_rect = target_text.get_rect(center = (const.WIDTH // 2, 70))
    
    SCREEN.blit(start_text, start_rect)
    SCREEN.blit(target_text, target_rect)

def draw_grid(SCREEN, grid_data, grid_results):
    for row in range(const.GRID_ROWS):
        for col in range(const.GRID_COLS):
            letter = grid_data[row][col]
            result = grid_results[row][col]
            
            # Position of current tile
            x = const.START_X + col * (const.TILE_SIZE + const.MARGIN)
            y = const.START_Y + row * (const.TILE_SIZE + const.MARGIN)
            
            # Tile's information to be drew on canvas
            tile_rect = pygame.Rect(x, y, const.TILE_SIZE, const.TILE_SIZE)
            
            tile_color = const.BLACK
            letter_color = const.WHITE
            border_color = const.TILE_BORDER_COLOR
            
            if result == "green":
                tile_color = const.GREEN
                border_color = const.GREEN
            elif result == "yellow":
                tile_color = const.YELLOW
                border_color = const.YELLOW
            elif result == "grey":
                tile_color = const.GREY
                border_color = const.GREY
            
            # Draw current tile onto canvas
            pygame.draw.rect(SCREEN, tile_color, tile_rect, border_radius = 3)
            if result == "empty":
                pygame.draw.rect(SCREEN, border_color, tile_rect, 2, border_radius = 3)
            
            if letter != " ":
                text_surface = LETTER_FONT.render(letter, True, letter_color)
                text_rect = text_surface.get_rect(center = tile_rect.center)
                
                SCREEN.blit(text_surface, text_rect)

def draw_keyboard(SCREEN, key_rects, key_status):
    
    for key_char, key_rect in key_rects.items():
        status = key_status[key_char]
        
        tile_color = const.KEY_COLOR
        letter_color = const.WHITE
        if status == "green":
            tile_color = const.GREEN
        elif status == "yellow":
            tile_color = const.YELLOW
        elif status == "grey":
            tile_color = const.GREY
            
        pygame.draw.rect(SCREEN, tile_color, key_rect, border_radius = 7)
        
        if len(key_char) > 1:
            text_surface = SPECIAL_KEY_FONT.render(key_char, True, letter_color)
        else:
            text_surface = KEY_FONT.render(key_char, True, letter_color)
        
        text_rect = text_surface.get_rect(center = key_rect.center)
        SCREEN.blit(text_surface, text_rect)

def draw_game_over_screen(SCREEN, did_win, target_word):
    overlay = pygame.Surface((const.WIDTH, const.HEIGHT))
    overlay.set_alpha(100)
    overlay.fill(const.WHITE)
    SCREEN.blit(overlay, (0, 0))
    
    if did_win:
        message = "You solve the ladder!"
    else:
        message = f"Out of steps! Word was: {target_word}"
    
    # Display main message
    text_surface = MESSAGE_FONT.render(message, True, const.BLACK)
    text_rect = text_surface.get_rect(center = (const.WIDTH // 2, const.HEIGHT // 2 - 40))
    SCREEN.blit(text_surface, text_rect)

    # Display "Play Again" option
    prompt_surface = MESSAGE_FONT.render("Press ENTER to Play Again", True, const.GREY)
    promp_rect = prompt_surface.get_rect(center = (const.WIDTH // 2, const.HEIGHT // 2 + 20))
    SCREEN.blit(prompt_surface, promp_rect)

def draw_hint_button(SCREEN, hints_left):
    pygame.draw.rect(SCREEN, const.KEY_COLOR, const.HINT_BUTTON_RECT, border_radius = 5)
    
    text_str = f"Hint ({hints_left})"
    text_surface = HINT_FONT.render(text_str, True, const.WHITE)
    text_rect = text_surface.get_rect(center = const.HINT_BUTTON_RECT.center)
    SCREEN.blit(text_surface, text_rect)
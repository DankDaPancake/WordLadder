import pygame

import constants as const 

## Initialize application
pygame.font.init()
LETTER_FONT = None
KEY_FONT = None
SPECIAL_KEY_FONT = None
MESSAGE_FONT = None
TARGET_FONT = None
HINT_FONT = None

def initialize_fonts():
    global LETTER_FONT, MESSAGE_FONT, KEY_FONT, TARGET_FONT, SPECIAL_KEY_FONT, HINT_FONT
    LETTER_FONT = pygame.font.SysFont(None, const.LETTER_FONT_SIZE)
    KEY_FONT = pygame.font.SysFont(None, const.KEY_FONT_SIZE)
    SPECIAL_KEY_FONT = pygame.font.SysFont(None, const.SPECIAL_KEY_FONT_SIZE)
    MESSAGE_FONT = pygame.font.SysFont(None, const.MESSAGE_FONT_SIZE)
    TARGET_FONT = pygame.font.SysFont(None, const.TARGET_FONT_SIZE)
    HINT_FONT = pygame.font.SysFont(None, const.HINT_FONT_SIZE)

def create_length_selector_rects():
    config = {"BUTTON_RECTS": []}
    BUTTON_COLS, BUTTON_ROWS = 3, 4
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_MARGIN = 150, 100, 20
    
    total_width = (BUTTON_COLS * BUTTON_WIDTH) + ((BUTTON_COLS - 1) * BUTTON_MARGIN)
    start_x_offset = (const.WIDTH - total_width) // 2
    start_y_offset = 250
    
    for i in range(BUTTON_ROWS):
        for j in range(BUTTON_COLS):
            x = start_x_offset + j * (BUTTON_WIDTH + BUTTON_MARGIN)
            y = start_y_offset + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
            print(x, y)
            
            rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
            config["BUTTON_RECTS"].append(rect)
    config["BACK_BUTTON_RECT"] = pygame.Rect(const.WIDTH // 2 - 100, 
                                             start_y_offset + (BUTTON_ROWS * (BUTTON_HEIGHT + BUTTON_MARGIN)), 200, 60)
    return config

def create_key_rects(game_config):
    key_rects = {}
    
    for i, row in enumerate(const.KEYBOARD_LAYOUT):
        # Position the keyboard rows
        key_width = game_config["KEY_WIDTH"]
        special_key_width = game_config["SPECIAL_KEY_WIDTH"]
        key_height = game_config["KEY_HEIGHT"]
        key_margin = game_config["KEY_MARGIN"]
        
        row_width = len(row) * (key_width + key_margin) - key_margin
        if i == 2:
            row_width += 2 * (special_key_width - key_width)  
                        
        # Position of first key on row
        x = (const.WIDTH - row_width) // 2
        y = game_config["KEYBOARD_START_Y"] + i * (key_height + key_margin)
        
        for key_char in row:
            if len(key_char) > 1:
                width = special_key_width
            else:
                width = key_width
            
            # Store key's rect information
            key_rect = pygame.Rect(x, y, width, key_height)
            key_rects[key_char] = key_rect
            x += width + key_margin
        
    return key_rects
    
def draw_target_display(SCREEN, start_word, target_word, game_config):
    start_text = TARGET_FONT.render(f"Start: {start_word}", True, const.WHITE)
    target_text = TARGET_FONT.render(f"Target: {target_word}", True, const.WHITE)
    
    start_rect = start_text.get_rect(center = (const.WIDTH // 2, 60))
    target_rect = target_text.get_rect(center = (const.WIDTH // 2, 100))
    
    SCREEN.blit(start_text, start_rect)
    SCREEN.blit(target_text, target_rect)

def draw_grid(SCREEN, grid_data, grid_results, game_config):
    # Get dynamic values from config
    tile_size = game_config["TILE_SIZE"]
    margin = game_config["MARGIN"]
    start_x = game_config["START_X"]
    start_y = game_config["START_Y"]
    
    for row in range(game_config["GRID_ROWS"]):
        for col in range(game_config["GRID_COLS"]):
            letter = grid_data[row][col]
            result = grid_results[row][col]
            
            # Position of current tile
            x = start_x + col * (tile_size + margin)
            y = start_y + row * (tile_size + margin)
            
            # Tile's information to be drew on canvas
            tile_rect = pygame.Rect(x, y, tile_size, tile_size)
            
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
                dynamic_font = pygame.font.SysFont(None, int(tile_size * 0.75))
                text_surface = dynamic_font.render(letter, True, letter_color)
                text_rect = text_surface.get_rect(center = tile_rect.center)
                
                SCREEN.blit(text_surface, text_rect)

def draw_keyboard(SCREEN, key_rects, key_status, game_config):
    
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

def draw_game_over_screen(SCREEN, did_win, target_word, game_config):
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
    prompt_surface = MESSAGE_FONT.render("Press ENTER or Click to Return to Menu", True, const.GREY)
    promp_rect = prompt_surface.get_rect(center = (const.WIDTH // 2, const.HEIGHT // 2 + 20))
    SCREEN.blit(prompt_surface, promp_rect)

def draw_hint_button(SCREEN, hints_left, game_config):
    pygame.draw.rect(SCREEN, const.KEY_COLOR, game_config["HINT_BUTTON_RECT"], border_radius = 5)
    
    text_str = f"Hint ({hints_left})"
    text_surface = HINT_FONT.render(text_str, True, const.WHITE)
    text_rect = text_surface.get_rect(center = game_config["HINT_BUTTON_RECT"].center)
    SCREEN.blit(text_surface, text_rect)
    
def draw_back_button(SCREEN, game_config):
    pygame.draw.rect(SCREEN, const.KEY_COLOR, game_config["BACK_BUTTON_RECT"], border_radius = 5)
    text = HINT_FONT.render("Back to Menu", True, const.WHITE)
    text_rect = text.get_rect(center = game_config["BACK_BUTTON_RECT"].center)
    SCREEN.blit(text, text_rect)

def draw_main_menu(SCREEN, menu_config):
    SCREEN.fill(const.BLACK)
    
    # Title
    title_text = MESSAGE_FONT.render("Word Ladder", True, const.WHITE)
    title_rect = title_text.get_rect(center = (const.WIDTH // 2, 150))
    SCREEN.blit(title_text, title_rect)
    
    # Play Button
    pygame.draw.rect(SCREEN, const.GREEN, menu_config["PLAY_BUTTON_RECT"], border_radius = 10)
    play_text = MESSAGE_FONT.render("PLAY", True, const.WHITE)
    play_rect = play_text.get_rect(center = menu_config["PLAY_BUTTON_RECT"].center)
    SCREEN.blit(play_text, play_rect)
    
    # Quit Button
    pygame.draw.rect(SCREEN, const.KEY_COLOR, menu_config["QUIT_BUTTON_RECT"], border_radius = 10)
    quit_text = MESSAGE_FONT.render("QUIT", True, const.WHITE)
    quit_rect = quit_text.get_rect(center = menu_config["QUIT_BUTTON_RECT"].center)
    SCREEN.blit(quit_text, quit_rect)

def draw_length_selector(SCREEN, length_config):
    overlay = pygame.Surface((const.WIDTH, const.HEIGHT))
    overlay.set_alpha(20)
    overlay.fill(const.GREY)
    SCREEN.blit(overlay, (0, 0))

    title_text = MESSAGE_FONT.render("Select Word Length", True, const.WHITE)
    title_rect = title_text.get_rect(center = (const.WIDTH // 2, 150))
    SCREEN.blit(title_text, title_rect)
    
    for i, rect in enumerate(length_config["BUTTON_RECTS"]):
        word_length = i + 4
        pygame.draw.rect(SCREEN, const.KEY_COLOR, rect, border_radius = 5)
        text = MESSAGE_FONT.render(str(word_length), True, const.BLACK)
        text_rect = text.get_rect(center = rect.center)
        SCREEN.blit(text, text_rect)
    
    pygame.draw.rect(SCREEN, const.GREY, length_config["BACK_BUTTON_RECT"], border_radius = 5)
    back_text = MESSAGE_FONT.render("Back", True, const.WHITE)
    back_rect = back_text.get_rect(center = length_config["BACK_BUTTON_RECT"].center)
    SCREEN.blit(back_text, back_rect)
import pygame
import math

import constants as const 

## Initialize application
pygame.font.init()
LETTER_FONT = None
KEY_FONT = None
SPECIAL_KEY_FONT = None
MESSAGE_FONT = None
TARGET_FONT = None
HINT_FONT = None

# Global variables
TITLE_IMAGE = None
TITLE_IMAGE_RIGHT = None
BAT_SWARM_IMAGE = None
PUMPKIN_IMAGE = None
DEFINITION_FONT = None
DEFINITION_TITLE_FONT = None
TIMER_FONT = None

MESSAGE_FONT_PATH = "assets/SpookyHalloweenPersonalUse.ttf"
TITLE_IMAGE_PATH = "assets/Cute-Corgi-Pumpkin.png"
TITLE_IMAGE_RIGHT_PATH = "assets/corg-removebg.png"
BAT_SWARM_PATH = "assets/bat swarm.png"
PUMPKIN_PATH = "assets/easy pumpkin.png"

def initialize_fonts():
    global LETTER_FONT, MESSAGE_FONT, KEY_FONT, TARGET_FONT, SPECIAL_KEY_FONT, HINT_FONT, TITLE_IMAGE, TITLE_IMAGE_RIGHT
    global DEFINITION_FONT, DEFINITION_TITLE_FONT, TIMER_FONT, BAT_SWARM_IMAGE, PUMPKIN_IMAGE
    
    LETTER_FONT = pygame.font.SysFont(None, const.LETTER_FONT_SIZE)
    KEY_FONT = pygame.font.SysFont(None, const.KEY_FONT_SIZE)
    SPECIAL_KEY_FONT = pygame.font.SysFont(None, const.SPECIAL_KEY_FONT_SIZE)
    MESSAGE_FONT = pygame.font.SysFont(None, const.MESSAGE_FONT_SIZE) if MESSAGE_FONT_PATH == "" else pygame.font.Font(MESSAGE_FONT_PATH, const.MESSAGE_FONT_SIZE)
    TARGET_FONT = pygame.font.SysFont(None, const.TARGET_FONT_SIZE)
    HINT_FONT = pygame.font.SysFont(None, const.HINT_FONT_SIZE)
    DEFINITION_FONT = pygame.font.SysFont('Cambria', const.DEFINITION_FONT_SIZE)
    DEFINITION_TITLE_FONT = pygame.font.SysFont(None, const.DEFINITION_TITLE_FONT_SIZE)
    TIMER_FONT = pygame.font.SysFont(None, const.TIMER_FONT_SIZE)
    
    # Load and scale the title images
    try:
        TITLE_IMAGE = pygame.image.load(TITLE_IMAGE_PATH)
        # Scale the image to a reasonable size
        TITLE_IMAGE = pygame.transform.scale(TITLE_IMAGE, (180, 120))
    except pygame.error:
        print(f"Could not load image: {TITLE_IMAGE_PATH}")
        TITLE_IMAGE = None
    
    try:
        TITLE_IMAGE_RIGHT = pygame.image.load(TITLE_IMAGE_RIGHT_PATH)
        # Scale the right image to match the left one
        TITLE_IMAGE_RIGHT = pygame.transform.scale(TITLE_IMAGE_RIGHT, (120, 120))
    except pygame.error:
        print(f"Could not load image: {TITLE_IMAGE_RIGHT_PATH}")
        TITLE_IMAGE_RIGHT = None
    
    try:
        BAT_SWARM_IMAGE = pygame.image.load(BAT_SWARM_PATH)
        # Scale bat swarm to fit screen nicely
        BAT_SWARM_IMAGE = pygame.transform.scale(BAT_SWARM_IMAGE, (const.WIDTH, const.HEIGHT))
        # Set opacity to 50%
        BAT_SWARM_IMAGE.set_alpha(128)  # 128 = 50% of 255
    except pygame.error:
        print(f"Could not load image: {BAT_SWARM_PATH}")
        BAT_SWARM_IMAGE = None
    
    try:
        PUMPKIN_IMAGE = pygame.image.load(PUMPKIN_PATH)
        # Scale pumpkin to a nice decorative size
        PUMPKIN_IMAGE = pygame.transform.scale(PUMPKIN_IMAGE, (80, 80))
    except pygame.error:
        print(f"Could not load image: {PUMPKIN_PATH}")
        PUMPKIN_IMAGE = None

def draw_bat_swarm_overlay(SCREEN):
    """Draw bat swarm overlay with 50% opacity after SCREEN.fill() calls."""
    if BAT_SWARM_IMAGE:
        SCREEN.blit(BAT_SWARM_IMAGE, (0, 0))

def draw_text_with_outline(surface, text, font, text_color, outline_color, center_pos, outline_width=3):
    # Create the outline by drawing text in multiple positions around the main position
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:  # Skip the center position for now
                outline_surface = font.render(text, True, outline_color)
                outline_rect = outline_surface.get_rect(center=(center_pos[0] + dx, center_pos[1] + dy))
                surface.blit(outline_surface, outline_rect)
    
    # Draw the main text on top
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=center_pos)
    surface.blit(text_surface, text_rect)
    
    return text_rect

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
    # Halloween-themed target display with outlines (darker text for light background)
    draw_text_with_outline(SCREEN, f"Start: {start_word}", TARGET_FONT, 
                          const.PURPLE, const.WHITE, 
                          (const.WIDTH // 2, 60), outline_width=2)
    
    draw_text_with_outline(SCREEN, f"Target: {target_word}", TARGET_FONT, 
                          const.ORANGE, const.WHITE, 
                          (const.WIDTH // 2, 100), outline_width=2)

def draw_grid(SCREEN, grid_data, grid_results, game_config, animation_info=None):
    # Get dynamic values from config
    tile_size = game_config["TILE_SIZE"]
    margin = game_config["MARGIN"]
    start_x = game_config["START_X"]
    start_y = game_config["START_Y"]
    
    # Animation helper function
    def calculate_animation_offset(row, col):
        if not animation_info or animation_info["state"] is None or animation_info["row"] != row:
            return 0, 0
        
        elapsed_time = animation_info["current_time"] - animation_info["start_time"]
        
        if animation_info["state"] == "jumping":
            # Each tile animates with a delay based on column position
            tile_delay = col * const.ANIMATION_DELAY_BETWEEN_TILES
            tile_elapsed = max(0, elapsed_time - tile_delay)
            
            if tile_elapsed < const.JUMP_ANIMATION_DURATION:
                # Use sine wave for smooth jumping motion
                progress = tile_elapsed / const.JUMP_ANIMATION_DURATION
                jump_offset = -const.JUMP_HEIGHT * abs(math.sin(progress * math.pi))
                return 0, int(jump_offset)
        
        elif animation_info["state"] == "shaking":
            # Shake horizontally for all tiles in the row
            if elapsed_time < const.SHAKE_ANIMATION_DURATION:
                # Use sine wave for shaking motion
                shake_frequency = 20  # Hz
                progress = elapsed_time / 1000.0  # Convert to seconds
                shake_offset = const.SHAKE_INTENSITY * math.sin(progress * shake_frequency * 2 * math.pi)
                return int(shake_offset), 0
        
        return 0, 0
    
    for row in range(game_config["GRID_ROWS"]):
        for col in range(game_config["GRID_COLS"]):
            letter = grid_data[row][col]
            result = grid_results[row][col]
            
            # Position of current tile
            x = start_x + col * (tile_size + margin)
            y = start_y + row * (tile_size + margin)
            
            # Apply animation offset
            offset_x, offset_y = calculate_animation_offset(row, col)
            x += offset_x
            y += offset_y
            
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
        
        # Halloween-themed keyboard colors (adjusted for light theme)
        tile_color = const.KEY_COLOR
        letter_color = const.BLACK  # Dark text on light keys
        if status == "green":
            tile_color = const.GREEN
        elif status == "yellow":
            tile_color = const.YELLOW
        elif status == "grey":
            tile_color = const.GREY
            
        pygame.draw.rect(SCREEN, tile_color, key_rect, border_radius = 7)
        # Add subtle outline to keys
        pygame.draw.rect(SCREEN, const.BLACK, key_rect, width=1, border_radius = 7)
        
        if len(key_char) > 1:
            text_surface = SPECIAL_KEY_FONT.render(key_char, True, letter_color)
        else:
            text_surface = KEY_FONT.render(key_char, True, letter_color)
        
        text_rect = text_surface.get_rect(center = key_rect.center)
        SCREEN.blit(text_surface, text_rect)

def draw_game_over_screen(SCREEN, did_win, target_word, game_config, completion_time=None, is_new_record=False):
    overlay = pygame.Surface((const.WIDTH, const.HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(const.LIGHT_PURPLE)
    SCREEN.blit(overlay, (0, 0))
    
    if did_win:
        message = "You solved the ladder!"
        message_color = const.ORANGE
    else:
        message = f"Out of steps! Word was: {target_word}"
        message_color = const.BLOOD_RED
    
    # Display main message with outline
    draw_text_with_outline(SCREEN, message, LETTER_FONT, 
                          message_color, const.WHITE, 
                          (const.WIDTH // 2, const.HEIGHT // 2 - 60), outline_width=3)

    # Display completion time if player won
    if did_win and completion_time is not None:
        import game_logic
        time_str = f"Time: {game_logic.format_time(completion_time)}"
        time_color = const.PUMPKIN_ORANGE if is_new_record else const.PURPLE
        
        draw_text_with_outline(SCREEN, time_str, TARGET_FONT, 
                              time_color, const.WHITE, 
                              (const.WIDTH // 2, const.HEIGHT // 2 - 20), outline_width=2)
        
        if is_new_record:
            draw_text_with_outline(SCREEN, "NEW PERSONAL BEST!", TARGET_FONT, 
                                  const.PUMPKIN_ORANGE, const.WHITE, 
                                  (const.WIDTH // 2, const.HEIGHT // 2 + 10), outline_width=2)

    # Display "Play Again" option with outline
    play_again_y = const.HEIGHT // 2 + 50 if (did_win and completion_time) else const.HEIGHT // 2 + 20
    draw_text_with_outline(SCREEN, "Press ENTER or Click to Return to Menu", LETTER_FONT, 
                          const.PURPLE, const.WHITE, 
                          (const.WIDTH // 2, play_again_y), outline_width=2)

def draw_hint_button(SCREEN, hints_left, game_config):
    # Halloween-themed hint button
    button_color = const.PUMPKIN_ORANGE if hints_left > 0 else const.GREY
    pygame.draw.rect(SCREEN, button_color, game_config["HINT_BUTTON_RECT"], border_radius = 5)
    pygame.draw.rect(SCREEN, const.BLACK, game_config["HINT_BUTTON_RECT"], width=2, border_radius = 5)
    
    text_str = f"Hint ({hints_left})"
    draw_text_with_outline(SCREEN, text_str, HINT_FONT, 
                          const.BLACK, const.WHITE, 
                          game_config["HINT_BUTTON_RECT"].center, outline_width=1)
    
    # Draw pumpkin decoration under hint button
    if PUMPKIN_IMAGE:
        pumpkin_x = game_config["HINT_BUTTON_RECT"].centerx - PUMPKIN_IMAGE.get_width() // 2
        pumpkin_y = game_config["HINT_BUTTON_RECT"].bottom + 10  # 10 pixels below button
        SCREEN.blit(PUMPKIN_IMAGE, (pumpkin_x, pumpkin_y))
    
def draw_back_button(SCREEN, game_config):
    pygame.draw.rect(SCREEN, const.BLOOD_RED, game_config["BACK_BUTTON_RECT"], border_radius = 5)
    pygame.draw.rect(SCREEN, const.BLACK, game_config["BACK_BUTTON_RECT"], width=2, border_radius = 5)
    
    draw_text_with_outline(SCREEN, "Back to Menu", HINT_FONT, 
                          const.WHITE, const.BLACK, 
                          game_config["BACK_BUTTON_RECT"].center, outline_width=1)

def draw_main_menu(SCREEN, menu_config):
    SCREEN.fill(const.HALLOWEEN_BACKGROUND)
    draw_bat_swarm_overlay(SCREEN)
    
    # Title centered independently
    title_y = 150
    title_center = (const.WIDTH // 2, title_y)
    
    # Position images symmetrically around the title with reduced distance
    image_distance_from_center = 300  # Reduced from previous larger distances
    image_y = title_y - 60  # Closer to the title vertically
    
    # Left image (original corgi pumpkin)
    if TITLE_IMAGE:
        left_image_x = title_center[0] - image_distance_from_center - TITLE_IMAGE.get_width() // 2
        SCREEN.blit(TITLE_IMAGE, (left_image_x, image_y))
    
    # Right image (new corgi)
    if TITLE_IMAGE_RIGHT:
        right_image_x = title_center[0] + image_distance_from_center - TITLE_IMAGE_RIGHT.get_width() // 2
        SCREEN.blit(TITLE_IMAGE_RIGHT, (right_image_x, image_y))
    
    # Title with Halloween outline (bigger font size)
    draw_text_with_outline(SCREEN, "Cordle", MESSAGE_FONT, 
                          const.PUMPKIN_ORANGE, const.BLACK, 
                          title_center, outline_width=4)
    
    # Play Button with outline
    pygame.draw.rect(SCREEN, const.PUMPKIN_ORANGE, menu_config["PLAY_BUTTON_RECT"], border_radius = 10)
    pygame.draw.rect(SCREEN, const.BLACK, menu_config["PLAY_BUTTON_RECT"], width=3, border_radius = 10)
    draw_text_with_outline(SCREEN, "PLAY", MESSAGE_FONT, 
                          const.BLACK, const.WHITE, 
                          menu_config["PLAY_BUTTON_RECT"].center, outline_width=2)
    
    # Quit Button with outline
    pygame.draw.rect(SCREEN, const.PURPLE, menu_config["QUIT_BUTTON_RECT"], border_radius = 10)
    pygame.draw.rect(SCREEN, const.BLACK, menu_config["QUIT_BUTTON_RECT"], width=3, border_radius = 10)
    draw_text_with_outline(SCREEN, "QUIT", MESSAGE_FONT, 
                          const.WHITE, const.BLACK, 
                          menu_config["QUIT_BUTTON_RECT"].center, outline_width=2)

def draw_length_selector(SCREEN, length_config):
    draw_bat_swarm_overlay(SCREEN)
    overlay = pygame.Surface((const.WIDTH, const.HEIGHT))
    overlay.set_alpha(40)
    overlay.fill(const.LIGHT_PURPLE)
    SCREEN.blit(overlay, (0, 0))

    # Title with spooky outline
    draw_text_with_outline(SCREEN, "Select Word Length", MESSAGE_FONT, 
                          const.PURPLE, const.WHITE, 
                          (const.WIDTH // 2, 150), outline_width=3)
    
    for i, rect in enumerate(length_config["BUTTON_RECTS"]):
        word_length = i + 4
        # Alternate colors for Halloween effect
        button_color = const.PUMPKIN_ORANGE if i % 2 == 0 else const.LIGHT_PURPLE
        pygame.draw.rect(SCREEN, button_color, rect, border_radius = 5)
        pygame.draw.rect(SCREEN, const.BLACK, rect, width=2, border_radius = 5)
        
        draw_text_with_outline(SCREEN, str(word_length), MESSAGE_FONT, 
                              const.BLACK, const.WHITE, 
                              rect.center, outline_width=2)
    
    # Back button with outline
    pygame.draw.rect(SCREEN, const.BLOOD_RED, length_config["BACK_BUTTON_RECT"], border_radius = 5)
    pygame.draw.rect(SCREEN, const.BLACK, length_config["BACK_BUTTON_RECT"], width=2, border_radius = 5)
    draw_text_with_outline(SCREEN, "Back", MESSAGE_FONT, 
                          const.WHITE, const.BLACK, 
                          length_config["BACK_BUTTON_RECT"].center, outline_width=2)

def wrap_text(text, font, max_width):
    """
    Wrap text to fit within a specified width.
    Returns a list of lines.
    """
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_surface = font.render(test_line, True, const.WHITE)
        
        if test_surface.get_width() <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # Single word is too long, just add it
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def draw_dictionary_hint(SCREEN, hint_word, definition_data, side="left"):
    """
    Draw dictionary definition on the side of the screen.
    side can be "left" or "right"
    """
    if not definition_data:
        return
    
    # Calculate panel position
    panel_width = const.HINT_PANEL_WIDTH
    panel_height = const.HEIGHT - 200
    
    if side == "left":
        panel_x = const.HINT_PANEL_MARGIN
    else:  # right
        panel_x = const.WIDTH - panel_width - const.HINT_PANEL_MARGIN
    
    panel_y = const.HINT_PANEL_MARGIN
    
    # Draw panel background (lighter for light theme)
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(SCREEN, const.WHITE, panel_rect, border_radius=10)
    pygame.draw.rect(SCREEN, const.ORANGE, panel_rect, width=3, border_radius=10)
    
    # Starting position for text
    text_x = panel_x + const.HINT_TEXT_MARGIN
    text_y = panel_y + const.HINT_TEXT_MARGIN
    text_width = panel_width - 2 * const.HINT_TEXT_MARGIN
    line_spacing = 5
    
    # Draw title
    title_text = f"Hint: {hint_word.upper()}"
    draw_text_with_outline(SCREEN, title_text, DEFINITION_TITLE_FONT,
                          const.ORANGE, const.WHITE,
                          (text_x + text_width // 2, text_y + 15), outline_width=1)
    
    text_y += 45
    
    # Draw phonetic if available
    if definition_data.get("phonetic"):
        phonetic_text = f"/{definition_data['phonetic']}/"
        phonetic_surface = DEFINITION_FONT.render(phonetic_text, True, const.PURPLE)
        SCREEN.blit(phonetic_surface, (text_x, text_y))
        text_y += phonetic_surface.get_height() + line_spacing
    
    text_y += 10
    
    # Draw meanings
    for i, meaning in enumerate(definition_data.get("meanings", [])[:3]):
        # Part of speech
        pos_text = f"({meaning.get('partOfSpeech', 'unknown')})"
        pos_surface = DEFINITION_FONT.render(pos_text, True, const.PURPLE)
        SCREEN.blit(pos_surface, (text_x, text_y))
        text_y += pos_surface.get_height() + line_spacing
        
        # Definition
        definition = meaning.get("definition", "")
        if definition:
            # Wrap definition text
            def_lines = wrap_text(definition, DEFINITION_FONT, text_width)
            for line in def_lines[:3]:  # Max 3 lines per definition
                def_surface = DEFINITION_FONT.render(line, True, const.BLACK)
                SCREEN.blit(def_surface, (text_x + 10, text_y))
                text_y += def_surface.get_height() + line_spacing
        
        # Example if available and space permits
        example = meaning.get("example", "")
        if example and text_y < panel_y + panel_height - 100:
            example_text = f"Ex: {example}"
            ex_lines = wrap_text(example_text, DEFINITION_FONT, text_width)
            for line in ex_lines[:2]:  # Max 2 lines for example
                ex_surface = DEFINITION_FONT.render(line, True, const.ORANGE)
                SCREEN.blit(ex_surface, (text_x + 10, text_y))
                text_y += ex_surface.get_height() + line_spacing
        
        text_y += 15  # Space between meanings
        
        # Stop if we're running out of space
        if text_y > panel_y + panel_height - 50:
            break

def draw_hint_loading(SCREEN, side="left"):
    """
    Draw loading indicator while fetching dictionary data.
    """
    panel_width = const.HINT_PANEL_WIDTH
    panel_height = 150
    
    if side == "left":
        panel_x = const.HINT_PANEL_MARGIN
    else:
        panel_x = const.WIDTH - panel_width - const.HINT_PANEL_MARGIN
    
    panel_y = const.HINT_PANEL_MARGIN
    
    # Draw panel background (lighter for light theme)
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(SCREEN, const.WHITE, panel_rect, border_radius=10)
    pygame.draw.rect(SCREEN, const.ORANGE, panel_rect, width=3, border_radius=10)
    
    # Loading text
    draw_text_with_outline(SCREEN, "Loading hint...", DEFINITION_TITLE_FONT,
                          const.PURPLE, const.WHITE,
                          (panel_x + panel_width // 2, panel_y + panel_height // 2), outline_width=1)

def draw_timer_panel(SCREEN, current_time, best_time, word_length, is_new_record=False):
    """
    Draw timer panel on the right side of the screen.
    """
    import game_logic
    
    # Panel position (right side)
    panel_width = const.TIMER_PANEL_WIDTH
    panel_height = const.TIMER_PANEL_HEIGHT
    panel_x = const.WIDTH - panel_width - const.TIMER_PANEL_MARGIN
    panel_y = const.TIMER_PANEL_MARGIN
    
    # Draw panel background
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(SCREEN, const.WHITE, panel_rect, border_radius=10)
    
    # Border color changes if new record
    border_color = const.PUMPKIN_ORANGE if is_new_record else const.ORANGE
    pygame.draw.rect(SCREEN, border_color, panel_rect, width=3, border_radius=10)
    
    # Timer title
    title_y = panel_y + 15
    draw_text_with_outline(SCREEN, "Timer", TIMER_FONT,
                          const.PURPLE, const.WHITE,
                          (panel_x + panel_width // 2, title_y), outline_width=1)
    
    # Current time
    current_time_str = game_logic.format_time(current_time)
    time_y = title_y + 35
    draw_text_with_outline(SCREEN, current_time_str, TIMER_FONT,
                          const.BLACK, const.WHITE,
                          (panel_x + panel_width // 2, time_y), outline_width=1)
    
    # Personal best
    best_time_str = game_logic.format_time(best_time)
    best_y = time_y + 30
    best_color = const.PUMPKIN_ORANGE if is_new_record else const.PURPLE
    
    draw_text_with_outline(SCREEN, f"Best: {best_time_str}", HINT_FONT,
                          best_color, const.WHITE,
                          (panel_x + panel_width // 2, best_y), outline_width=1)
    
    # New record indicator
    if is_new_record:
        record_y = best_y + 25
        draw_text_with_outline(SCREEN, "NEW RECORD!", HINT_FONT,
                              const.PUMPKIN_ORANGE, const.WHITE,
                              (panel_x + panel_width // 2, record_y), outline_width=1)
import pygame
import math
import constants as const 

## Initialize application
pygame.font.init()
LETTER_FONT = pygame.font.SysFont(None, 60)
MESSAGE_FONT = pygame.font.SysFont(None, 50)
KEY_FONT = pygame.font.SysFont(None, 40)

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
    

def draw_keyboard(SCREEN, key_rects, key_status):
    
    special_key_font = pygame.font.SysFont(None, 30)
    
    for key_char, key_rect in key_rects.items():
        status = key_status[key_char]
        
        if status == "green":
            tile_color = const.GREEN
            letter_color = const.WHITE
        elif status == "yellow":
            tile_color = const.YELLOW
            letter_color = const.WHITE
        elif status == "grey":
            tile_color = const.GREY
            letter_color = const.WHITE
        else:
            tile_color = const.KEY_COLOR
            letter_color = const.WHITE
            
        pygame.draw.rect(SCREEN, tile_color, key_rect, border_radius = 7)
        
        if len(key_char) > 1:
            text_surface = special_key_font.render(key_char, True, letter_color)
        else:
            text_surface = KEY_FONT.render(key_char, True, letter_color)
        
        text_rect = text_surface.get_rect(center = key_rect.center)
        SCREEN.blit(text_surface, text_rect)

def draw_grid(SCREEN, grid_data, grid_results, current_row, shake_offset_x, 
              is_animating, animation_tile_index, animation_start_time):
    for row in range(const.GRID_ROWS):
        for col in range(const.GRID_COLS):
            current_shake = 0
            if row == current_row and shake_offset_x != 0:
                current_shake = shake_offset_x
            
            # Position of current tile
            x = const.START_X + col * (const.TILE_SIZE + const.MARGIN) + current_shake
            y = const.START_Y + row * (const.TILE_SIZE + const.MARGIN)
            
            if is_animating and row == current_row:
                if col < animation_tile_index:
                    pass
                elif col == animation_tile_index:
                    current_time = pygame.time.get_ticks()
                    time_since_start = current_time - animation_start_time
                    
                    tile_elapsed = time_since_start % const.TILE_ANIMATION_TIME
                    
                    progress = tile_elapsed / const.TILE_ANIMATION_TIME
                    jump = math.sin(progress * math.pi) * const.JUMP_HEIGHT
                    y -= int(jump)
            
            # Tile's information to be drew on canvas
            tile_rect = pygame.Rect(x, y, const.TILE_SIZE, const.TILE_SIZE)
            
            tile_color = const.BLACK
            letter_color = const.WHITE
            border_color = const.TILE_BORDER_COLOR
            result = grid_results[row][col]
            
            if result == "green":
                tile_color = const.GREEN
                letter_color = const.WHITE
                border_color = const.GREEN
            elif result == "yellow":
                tile_color = const.YELLOW
                letter_color = const.WHITE
                border_color = const.YELLOW
            elif result == "grey":
                tile_color = const.GREY
                letter_color = const.WHITE
                border_color = const.GREY
            
            # Draw current tile onto canvas
            pygame.draw.rect(SCREEN, tile_color, tile_rect, border_radius = 3)
            if result == "empty":
                pygame.draw.rect(SCREEN, border_color, tile_rect, 2, border_radius = 3)
            
            letter = grid_data[row][col]
            if letter != " ":
                text_surface = LETTER_FONT.render(letter, True, letter_color)
                text_rect = text_surface.get_rect(center = tile_rect.center)
                
                SCREEN.blit(text_surface, text_rect)

def draw_game_over_screen(SCREEN, did_win, secret_word):
    overlay = pygame.Surface((const.WIDTH, const.HEIGHT))
    overlay.set_alpha(100)
    overlay.fill(const.WHITE)
    SCREEN.blit(overlay, (0, 0))
    
    if did_win:
        message = "You win!"
    else:
        message = f"You lose! Word was: {secret_word}"
    
    # Display main message
    text_surface = MESSAGE_FONT.render(message, True, const.BLACK)
    text_rect = text_surface.get_rect(center = (const.WIDTH // 2, const.HEIGHT // 2 - 40))
    SCREEN.blit(text_surface, text_rect)

    # Display "Play Again" option
    prompt_surface = MESSAGE_FONT.render("Press ENTER to Play Again", True, const.GREY)
    promp_rect = prompt_surface.get_rect(center = (const.WIDTH // 2, const.HEIGHT // 2 + 20))
    SCREEN.blit(prompt_surface, promp_rect)
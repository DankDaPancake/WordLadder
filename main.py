import pygame
import sys
import os
import math

import game_logic
import constants as const 
import drawing

def main():
    
    pygame.init()
    ## Generate main window
    SCREEN = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
    pygame.display.set_caption("DankDaPancake's Wordle")
    
    # Loads words
    try:
        word_list = game_logic.load_word_list(os.path.join(os.path.dirname(__file__), "dictionary.txt"))
    except FileNotFoundError:
        print("ERROR. wordlist.txt not found! Exiting.")
        sys.exit()
        
    key_rects = drawing.create_key_rects()
    
    (secret_word, grid_data, grid_results, 
    current_row, current_col,
    game_over, did_win, key_status,
    is_animating, animation_start_time, animation_tile_index, 
    current_guess_results, current_guess_word,
    is_shaking, shake_start_time) = game_logic.reset_game(word_list)
    
    running = True
    clock = pygame.time.Clock()
    # Game loop
    while running:
        shake_offset_x = 0
        if is_shaking:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - shake_start_time
            if elapsed > const.SHAKE_DURATION:
                is_shaking = False
            else:
                progress = elapsed / const.SHAKE_DURATION
                sine_wave = math.sin(progress * math.pi * const.SHAKE_FREQUENCY) # x = sin(t * 3.14 * f)
                shake_offset_x = int(sine_wave * const.SHAKE_MAGNITUDE)
                
        if is_animating:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - animation_start_time
            
            # Current tile to flip
            current_tile_to_reveal = elapsed_time // const.TILE_ANIMATION_TIME
            
            while animation_tile_index <= current_tile_to_reveal and animation_tile_index < const.GRID_COLS:
                letter = grid_data[current_row][animation_tile_index]
                result = current_guess_results[animation_tile_index]
                
                # Update mid-animation tile state
                grid_results[current_row][animation_tile_index] = result
                
                status_priority = {"green": 3, "yellow": 2, "grey": 1, "empty": 0}
                current_priority = status_priority[key_status[letter]]
                new_priority = status_priority[result]
                if new_priority > current_priority:
                    key_status[letter] = result
                
                animation_tile_index += 1
                
            if animation_tile_index >= const.GRID_COLS:
                is_animating = False
                
                if current_guess_word == secret_word:
                    game_over = True
                    did_win = True
                
                current_row += 1
                current_col = 0
                
                if current_row == const.GRID_ROWS and not did_win:
                    game_over = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not is_animating and not is_shaking:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not game_over:
                        for char, rect in key_rects.items():
                            # Check if clicking position collides with key's rect
                            if rect.collidepoint(event.pos):
                                if char == "ENTER":
                                    if current_col == const.GRID_COLS:
                                        current_guess_word = "".join(grid_data[current_row])
                                        if current_guess_word not in word_list: 
                                            is_shaking = True
                                            shake_start_time = pygame.time.get_ticks()
                                        else:
                                            is_animating = True
                                            animation_start_time = pygame.time.get_ticks()
                                            animation_tile_index = 0
                                            current_guess_results = game_logic.check_guess(current_guess_word, secret_word)
                                
                                elif char == "DEL":
                                    if current_col > 0:
                                        current_col -= 1
                                        grid_data[current_row][current_col] = " "
                                
                                else: # Letters
                                    if current_col < const.GRID_COLS:
                                        grid_data[current_row][current_col] = char
                                        current_col += 1
                                    
                                
                if event.type == pygame.KEYDOWN:
                    
                    # Player pressed BACKSPACE:
                    if event.key == pygame.K_BACKSPACE:
                        if current_col > 0:
                            current_col -= 1
                            grid_data[current_row][current_col] = " "
                    
                    # Player pressed ENTER
                    elif event.key == pygame.K_RETURN:
                        if game_over:
                            (secret_word, grid_data, grid_results, 
                            current_row, current_col, 
                            game_over, did_win, key_status,
                            is_animating, animation_start_time, animation_tile_index, 
                            current_guess_results, current_guess_word,
                            is_shaking, shake_start_time) = game_logic.reset_game(word_list)
                            
                        elif current_col == const.GRID_COLS:                        
                            # Get the entered guess word
                            current_guess_word = "".join(grid_data[current_row])
                            
                            if current_guess_word not in word_list:
                                is_shaking = True
                                shake_start_time = pygame.time.get_ticks()
                            else:                                
                                is_animating = True
                                animation_start_time = pygame.time.get_ticks()
                                animation_tile_index = 0
                                current_guess_results = game_logic.check_guess(current_guess_word, secret_word)
                    
                    # Player pressed a letter
                    elif event.unicode.isalpha() and not game_over:
                        char = event.unicode.upper()
                        if char in key_rects:
                            if current_col < const.GRID_COLS:
                                grid_data[current_row][current_col] = char
                                current_col += 1
        
        SCREEN.fill(const.BLACK)
        drawing.draw_grid(SCREEN, grid_data, grid_results, current_row, shake_offset_x, 
                          is_animating, animation_tile_index, animation_start_time)
        
        drawing.draw_keyboard(SCREEN, key_rects, key_status)
        
        if game_over:
            drawing.draw_game_over_screen(SCREEN, did_win, secret_word)
        
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
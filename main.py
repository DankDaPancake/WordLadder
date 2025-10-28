import pygame
import sys
import os

import game_logic
import constants as const 
import drawing

def main():
    
    pygame.init()
    drawing.initialize_fonts()
    ## Generate main window
    SCREEN = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
    pygame.display.set_caption("DankDaPancake's Wordle")
    
    # Loads words
    try:
        word_list = game_logic.load_word_list(os.path.join(os.path.dirname(__file__), "wordlist.txt"))
    except FileNotFoundError:
        print("ERROR. wordlist.txt not found! Exiting.")
        sys.exit()
        
    key_rects = drawing.create_key_rects()
    
    (start_word, target_word, grid_data, grid_results, 
    current_row, current_col,
    game_over, did_win, key_status,
    hints_left) = game_logic.reset_game(word_list)
    
    running = True
    clock = pygame.time.Clock()
    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if const.HINT_BUTTON_RECT.collidepoint(event.pos) and hints_left > 0:
                    previous_word = "".join(grid_data[current_row - 1])
                    hint_word = game_logic.find_next_step(previous_word, target_word, word_list)
                    
                    if hint_word:
                        hints_left -= 1
                        
                        grid_data[current_row] = list(hint_word)
                        
                        enter_event = pygame.event.Event(pygame.KEYDOWN, key = pygame.K_RETURN)
                        pygame.event.post(enter_event)
                
                else:    
                    for char, rect in key_rects.items():
                        # Check if clicking position collides with key's rect
                        if rect.collidepoint(event.pos):
                            if char == "ENTER":
                                key_event = pygame.event.Event(pygame.KEYDOWN, key = pygame.K_RETURN)
                            
                            elif char == "DEL":
                                key_event = pygame.event.Event(pygame.KEYDOWN, key = pygame.K_BACKSPACE)
                            
                            else: # Letters
                                key_event = pygame.event.Event(pygame.KEYDOWN, unicode = char)
                            
                            pygame.event.post(key_event)
                                        
            if event.type == pygame.KEYDOWN:
                
                # Player pressed BACKSPACE:
                if event.key == pygame.K_BACKSPACE and not game_over:
                    if current_col > 0:
                        current_col -= 1
                        grid_data[current_row][current_col] = " "
                
                # Player pressed ENTER
                elif event.key == pygame.K_RETURN:
                    if game_over:
                        (start_word, target_word, grid_data, grid_results, 
                        current_row, current_col, 
                        game_over, did_win, key_status,
                        hints_left) = game_logic.reset_game(word_list)
                        
                    elif current_col == const.GRID_COLS:                        
                        # Get the entered guess word
                        new_guess = "".join(grid_data[current_row])
                        previous_word = "".join(grid_data[current_row - 1])
                        
                        if game_logic.is_valid_step(previous_word, new_guess, word_list):
                            results = game_logic.get_color_hints(new_guess, target_word)
                            grid_results[current_row] = results
                            
                            status_priority = {"green": 3, "yellow": 2, "grey": 1, "empty": 0}
                            for i, letter in enumerate(new_guess):
                                new_status = results[i]
                                
                                if letter in key_status:
                                    current_priority = status_priority[key_status[letter]]
                                    new_priority = status_priority[new_status]
                                    if new_priority > current_priority:
                                        key_status[letter] = new_status
                                
                            if new_guess == target_word:
                                game_over = True
                                did_win = True
                            elif current_row == const.GRID_ROWS - 1:
                                game_over = True
                                did_win = False
                            else:
                                current_row += 1
                                current_col = 0
                            
                # Player pressed a letter
                elif event.unicode.isalpha() and not game_over:
                    char = event.unicode.upper()
                    if char in key_status:
                        if current_col < const.GRID_COLS:
                            grid_data[current_row][current_col] = char
                            current_col += 1
        
        SCREEN.fill(const.BLACK)
        
        drawing.draw_target_display(SCREEN, start_word, target_word)
        drawing.draw_grid(SCREEN, grid_data, grid_results)
        drawing.draw_keyboard(SCREEN, key_rects, key_status)
        drawing.draw_hint_button(SCREEN, hints_left)
        
        if game_over:
            drawing.draw_game_over_screen(SCREEN, did_win, target_word)
        
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
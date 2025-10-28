import pygame
import sys

import game_logic
import constants as const 
import drawing

STATE_MAIN_MENU = "main_menu"
STATE_SELECT_LENGTH = "select_length"
STATE_IN_GAME = "in_game"

def main_app():
    
    pygame.init()
    drawing.initialize_fonts()
    ## Generate main window
    SCREEN = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
    pygame.display.set_caption("DankDaPancake's Wordle")
    clock = pygame.time.Clock()
    
    game_state = STATE_MAIN_MENU
    current_word_length = 5
    running = True

    # Game loop
    while running:
        if game_state == STATE_MAIN_MENU:
            new_state, running = run_main_menu(SCREEN, clock)
            game_state = new_state
        
        elif game_state == STATE_SELECT_LENGTH:
            new_state, new_length = run_length_selector(SCREEN, clock)
            game_state = new_state
            if new_length:
                current_word_length = new_length
        
        elif game_state == STATE_IN_GAME:
            new_state = run_game_loop(SCREEN, clock, current_word_length)
            game_state = new_state
        
    pygame.quit()
    sys.exit()

def run_main_menu(SCREEN, clock):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_MAIN_MENU, False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if const.PLAY_BUTTON_RECT.collidepoint(event.pos):
                    return STATE_SELECT_LENGTH, True
                
                if const.QUIT_BUTTON_RECT.collidepoint(event.pos):
                    return STATE_MAIN_MENU, False
        
        drawing.draw_main_menu(SCREEN)
        pygame.display.flip()
        clock.tick(60)

def run_length_selector(SCREEN, clock):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_MAIN_MENU, None

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(const.LENGTH_BUTTON_RECTS):
                    if rect.collidepoint(event.pos):
                        selected_length = i + 4
                        return STATE_IN_GAME, selected_length
                
                if not any(rect.collidepoint(event.pos) for rect in const.LENGTH_BUTTON_RECTS):
                    return STATE_MAIN_MENU, None
    
        drawing.draw_length_selector(SCREEN)
        pygame.display.flip()
        clock.tick(60)

def run_game_loop(SCREEN, clock, word_length):
    word_list = game_logic.load_word_list(word_length)
    if not word_list:
        print(f"Error: word_list_{word_length}.txt not found.")
        return STATE_MAIN_MENU

    key_rects = drawing.create_key_rects()

    (start_word, target_word, grid_data, grid_results, 
    current_row, current_col,
    game_over, did_win, key_status,
    hints_left) = game_logic.reset_game(word_list, word_length)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_MAIN_MENU
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if const.BACK_BUTTON_RECT.collidepoint(event.pos):
                    return STATE_MAIN_MENU
                
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
                        hints_left) = game_logic.reset_game(word_list, word_length)
                        
                    elif current_col == word_length:                        
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
                        if current_col < word_length:
                            grid_data[current_row][current_col] = char
                            current_col += 1
        
        SCREEN.fill(const.BLACK)
        
        drawing.draw_target_display(SCREEN, start_word, target_word)
        drawing.draw_hint_button(SCREEN, hints_left)
        drawing.draw_back_button(SCREEN)        

        drawing.draw_grid(SCREEN, grid_data, grid_results)
        drawing.draw_keyboard(SCREEN, key_rects, key_status)
        
        if game_over:
            drawing.draw_game_over_screen(SCREEN, did_win, target_word)
        
        pygame.display.flip()
        clock.tick(60)
        
if __name__ == "__main__":
    main_app()
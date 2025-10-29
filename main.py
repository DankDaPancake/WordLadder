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

    # Menu layouts
    menu_config = {
        "PLAY_BUTTON_RECT": pygame.Rect(const.WIDTH // 2 - 200, 300, 400, 100),
        "QUIT_BUTTON_RECT": pygame.Rect(const.WIDTH // 2 - 200, 420, 400, 100)
    }
    length_config = drawing.create_length_selector_rects()

    # Game loop
    while running:
        if game_state == STATE_MAIN_MENU:
            new_state, running = run_main_menu(SCREEN, clock, menu_config)
            game_state = new_state
        
        elif game_state == STATE_SELECT_LENGTH:
            new_state, new_length = run_length_selector(SCREEN, clock, length_config)
            game_state = new_state
            if new_length:
                current_word_length = new_length
        
        elif game_state == STATE_IN_GAME:
            new_state = run_game_loop(SCREEN, clock, current_word_length)
            game_state = new_state
        
    pygame.quit()
    sys.exit()

def run_main_menu(SCREEN, clock, menu_config):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_MAIN_MENU, False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_config["PLAY_BUTTON_RECT"].collidepoint(event.pos):
                    return STATE_SELECT_LENGTH, True
                
                if menu_config["QUIT_BUTTON_RECT"].collidepoint(event.pos):
                    return STATE_MAIN_MENU, False
        
        drawing.draw_main_menu(SCREEN, menu_config)
        pygame.display.flip()
        clock.tick(60)

def run_length_selector(SCREEN, clock, length_config):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_MAIN_MENU, None

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(length_config["BUTTON_RECTS"]):
                    if rect.collidepoint(event.pos):
                        selected_length = i + 4
                        return STATE_IN_GAME, selected_length
                
                # if not any(rect.collidepoint(event.pos) for rect in const.LENGTH_BUTTON_RECTS):
                #     return STATE_MAIN_MENU, None
                if length_config["BACK_BUTTON_RECT"].collidepoint(event.pos):
                    return STATE_MAIN_MENU, None
    
        drawing.draw_length_selector(SCREEN, length_config)
        pygame.display.flip()
        clock.tick(60)

def run_game_loop(SCREEN, clock, word_length):
    # Generate dynamic game config
    game_config = {}
    
    game_config["GRID_ROWS"] = word_length + 3
    game_config["GRID_COLS"] = word_length
    
    game_area_height = const.HEIGHT - const.TOP_MARGIN_PX - const.BOTTOM_MARGIN_PX
    
    tile_size = game_area_height / (game_config["GRID_ROWS"] * (1 + const.MARGIN_RATIO))
    margin = tile_size * const.MARGIN_RATIO
    
    game_config["TILE_SIZE"] = int(tile_size)
    game_config["MARGIN"] = int(margin)
    
    grid_width = (word_length * tile_size) + ((word_length - 1) * margin)
    game_config["START_X"] = int((const.WIDTH - grid_width) // 2)
    game_config["START_Y"] = const.TOP_MARGIN_PX
    
    key_width = const.KEY_WIDTH
    key_height = const.KEY_HEIGHT
    game_config["KEY_WIDTH"] = int(key_width)
    game_config["KEY_HEIGHT"] = int(key_height)
    game_config["SPECIAL_KEY_WIDTH"] = int(const.SPECIAL_KEY_WIDTH)
    game_config["KEY_MARGIN"] = const.KEY_MARGIN
    game_config["KEYBOARD_START_Y"] = const.TOP_MARGIN_PX + (tile_size + margin) * game_config["GRID_ROWS"]
    
    game_config["HINT_BUTTON_RECT"] = pygame.Rect(const.WIDTH - 220, 150, 200, 80)
    game_config["BACK_BUTTON_RECT"] = pygame.Rect(20, const.HEIGHT - 100, 200, 80)
    
    # Game core initialization
    word_list = game_logic.load_word_list(word_length)
    if not word_list:
        print(f"Error: word_list_{word_length}.txt not found.")
        return STATE_MAIN_MENU

    key_rects = drawing.create_key_rects(game_config)

    (start_word, target_word, grid_data, grid_results, 
    current_row, current_col,
    game_over, did_win, key_status,
    hints_left, solution_path) = game_logic.reset_game(word_list, word_length, game_config)
    
    # Dictionary hint state
    current_hint_word = None
    current_hint_definition = None
    hint_loading = False
    
    # Timer system
    import time
    start_time = time.time()
    completion_time = None  # Will be set when game ends
    best_time = game_logic.get_best_time(word_length)
    is_new_record = False
    
    # Animation system
    animation_state = None  # "jumping" or "shaking" or None
    animation_start_time = 0
    animation_row = -1  # Which row is animating
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_MAIN_MENU
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_config["BACK_BUTTON_RECT"].collidepoint(event.pos):
                    return STATE_MAIN_MENU
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if game_config["HINT_BUTTON_RECT"].collidepoint(event.pos) and hints_left > 0:
                    previous_word = "".join(grid_data[current_row - 1])
                    
                    # Start loading the dictionary hint
                    hint_loading = True
                    
                    # Get dictionary hint from pre-generated path (this might take a moment due to API call)
                    hint_word, definition_data = game_logic.get_dictionary_hint_from_path(previous_word, solution_path)
                    
                    # If path-based hint fails, use fallback method
                    if not hint_word:
                        hint_word, definition_data = game_logic.get_dictionary_hint(previous_word, target_word, word_list)
                    
                    if hint_word and definition_data:
                        hints_left -= 1
                        current_hint_word = hint_word
                        current_hint_definition = definition_data
                        hint_loading = False
                    elif hint_word:  # Fallback if API fails but we have a word
                        hints_left -= 1
                        current_hint_word = hint_word
                        current_hint_definition = {"word": hint_word, "meanings": [{"partOfSpeech": "unknown", "definition": "Dictionary unavailable - try this word!"}]}
                        hint_loading = False
                    else:
                        hint_loading = False
                        
                elif not any([game_config["HINT_BUTTON_RECT"].collidepoint(event.pos), 
                              game_config["BACK_BUTTON_RECT"].collidepoint(event.pos)]):
                    for char, rect in key_rects.items():
                        if rect.collidepoint(event.pos):
                            # Post a "fake" keyboard event
                            key_to_post = None
                            if char == "ENTER": key_to_post = pygame.K_RETURN
                            elif char == "DEL": key_to_post = pygame.K_BACKSPACE
                            elif len(char) == 1: key_to_post = char
                            
                            if key_to_post:
                                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, 
                                    key=(key_to_post if isinstance(key_to_post, int) else None),
                                    unicode=(key_to_post if isinstance(key_to_post, str) else '')))
                                        
            if event.type == pygame.KEYDOWN:
                # Player pressed BACKSPACE:
                if event.key == pygame.K_BACKSPACE and not game_over:
                    if current_col > 0:
                        current_col -= 1
                        grid_data[current_row][current_col] = " "
                
                # Player pressed ENTER
                elif event.key == pygame.K_RETURN:
                    if game_over:
                        return STATE_MAIN_MENU
                        
                    elif current_col == word_length:                        
                        # Get the entered guess word
                        new_guess = "".join(grid_data[current_row])
                        previous_word = "".join(grid_data[current_row - 1])
                        
                        if game_logic.is_valid_step(previous_word, new_guess, word_list):
                            # Valid word - start jumping animation
                            animation_state = "jumping"
                            animation_start_time = pygame.time.get_ticks()
                            animation_row = current_row
                            
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
                                # Record completion time and check for new record
                                completion_time = time.time() - start_time
                                is_new_record = game_logic.update_best_time(word_length, completion_time)
                            elif current_row == game_config["GRID_ROWS"] - 1:
                                game_over = True
                                did_win = False
                            else:
                                current_row += 1
                                current_col = 0
                        else:
                            # Invalid word - start shaking animation
                            animation_state = "shaking"
                            animation_start_time = pygame.time.get_ticks()
                            animation_row = current_row
                            
                # Player pressed a letter
                elif hasattr(event, 'unicode') and event.unicode.isalpha() and not game_over:
                    char = event.unicode.upper()
                    if char in key_status:
                        if current_col < word_length:
                            grid_data[current_row][current_col] = char
                            current_col += 1
        
        # Update animations
        current_time = pygame.time.get_ticks()
        if animation_state:
            animation_elapsed = current_time - animation_start_time
            if ((animation_state == "jumping" and animation_elapsed >= const.JUMP_ANIMATION_DURATION) or
                (animation_state == "shaking" and animation_elapsed >= const.SHAKE_ANIMATION_DURATION)):
                animation_state = None
                animation_row = -1
        
        SCREEN.fill(const.HALLOWEEN_BACKGROUND)
        drawing.draw_bat_swarm_overlay(SCREEN)
        
        drawing.draw_target_display(SCREEN, start_word, target_word, game_config)
        drawing.draw_hint_button(SCREEN, hints_left, game_config)
        drawing.draw_back_button(SCREEN, game_config)        

        # Pass animation info to draw_grid
        animation_info = {
            "state": animation_state,
            "start_time": animation_start_time,
            "row": animation_row,
            "current_time": current_time
        }
        drawing.draw_grid(SCREEN, grid_data, grid_results, game_config, animation_info)
        drawing.draw_keyboard(SCREEN, key_rects, key_status, game_config)
        
        # Draw timer panel on the right
        if game_over and completion_time is not None:
            # Use stored completion time when game is over
            display_time = completion_time
        else:
            # Use current elapsed time during gameplay
            display_time = time.time() - start_time
        
        drawing.draw_timer_panel(SCREEN, display_time, best_time, word_length, is_new_record and game_over)
        
        # Draw dictionary hint if available
        if hint_loading:
            drawing.draw_hint_loading(SCREEN, side="left")
        elif current_hint_word and current_hint_definition:
            drawing.draw_dictionary_hint(SCREEN, current_hint_word, current_hint_definition, side="left")
        
        if game_over:
            drawing.draw_game_over_screen(SCREEN, did_win, target_word, game_config, completion_time if did_win else None, is_new_record)
        
        pygame.display.flip()
        clock.tick(60)
        
if __name__ == "__main__":
    main_app()
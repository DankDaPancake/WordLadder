import random
from collections import Counter

import constants as const

def load_word_list(filename):
    with open(filename) as f:
        words = [line.strip().upper() for line in f if len(line) == const.GRID_ROWS]
            
    return words

def check_guess(guess_word, secret_word):
    results = ["grey"] * 5
    
    secret_counts = Counter(secret_word)
    
    # Check for "green" matches
    for i in range(len(guess_word)):
        if guess_word[i] == secret_word[i]:
            results[i] = "green"
            secret_counts[guess_word[i]] -= 1
    
    # Check for "yellow" matches
    for i in range(len(guess_word)):
        if results[i] == "green":
            continue
        
        if guess_word[i] in secret_counts and secret_counts[guess_word[i]] > 0:
            results[i] = "yellow"
            secret_counts[guess_word[i]] -= 1
    
    return results

def reset_game(word_list):
    # Initialize data for new game
    secret_word = random.choice(word_list)
    
    grid_results = [["empty" for _ in range(const.GRID_COLS)] for _ in range(const.GRID_ROWS)]
    grid_data = [["" for _ in range(const.GRID_COLS)] for _ in range(const.GRID_ROWS)]
    
    current_row = 0
    current_col = 0
    game_over = False
    did_win = False
    
    key_status = {}
    for row in const.KEYBOARD_LAYOUT:
        for key in row:
            key_status[key] = "empty"
    
    # Initialize animation states
    is_animating = False
    animation_start_time = 0
    animation_tile_index = 0
    current_guess_results = []
    current_guess_word = ""
    
    # Initialize shaking state
    is_shaking = False
    shake_start_time = 0
    
    return (secret_word, grid_data, grid_results, 
            current_row, current_col, 
            game_over, did_win, key_status,
            is_animating, animation_start_time, animation_tile_index, 
            current_guess_results, current_guess_word,
            is_shaking, shake_start_time)
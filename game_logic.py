import random
from collections import Counter

import constants as const

def load_word_list(filename):
    with open(filename) as f:
        words = [line.strip().upper() for line in f if len(line) == const.GRID_COLS]
            
    return words

def is_one_letter_diff(word_a, word_b):
    if len(word_a) != len(word_b):
        return False
    
    diff_count = 0
    for i in range(len(word_a)):
        diff_count += word_a[i] != word_b
    return diff_count == 1

def is_valid_step(previous_word, new_guess, word_list):
    if new_guess not in word_list:
        print(f"'{new_guess}' is not a valid word.")
        return False
    
    if not is_one_letter_diff(previous_word, new_guess):
        print(f"'{new_guess}' must be one letter difference from '{previous_word}'")
        return False
    
    return True

def get_color_hints(guess_word, target_word):
    results = ["grey"] * const.GRID_COLS
    secret_counts = Counter(target_word)
    
    for i in range(len(guess_word)):
        if guess_word[i] == target_word[i]:
            results[i] = "green"
            secret_counts[guess_word[i]] -= 1
    
    for i in range(len(guess_word)):
        if results[i] == "green":
            continue
        if guess_word[i] in secret_counts and secret_counts[guess_word[i]] > 0:
            results[i] = "yellow"
            secret_counts[guess_word[i]] -= 1
    
    return results

def reset_game(word_list):
    # Initialize data for new game
    start_word = random.choice(word_list)
    while len(start_word) != const.GRID_COLS:
        start_word = random.choice(word_list)
    
    target_word = random.choice(word_list)
    while start_word == target_word or len(start_word) != target_word:
        target_word = random.choice(word_list)
        
    print(f"Start: {start_word} | Target: {target_word}")
    
    grid_data = [["" for _ in range(const.GRID_COLS)] for _ in range(const.GRID_ROWS)]
    grid_results = [["empty" for _ in range(const.GRID_COLS)] for _ in range(const.GRID_ROWS)]

    grid_data[0] = list(start_word)
    grid_results[0] = get_color_hints(start_word, target_word)
    
    current_row = 1
    current_col = 0
    game_over = False
    did_win = False
    
    key_status = {}
    for row in const.KEYBOARD_LAYOUT:
        for key in row:
            key_status[key] = "empty"
    
    status_priority = {"green": 3, "yellow": 2, "grey": 1, "empty": 0}
    for i, letter in enumerate(start_word):
        new_status = grid_results[0][i]
        current_priority = status_priority[key_status[letter]]
        new_priority = status_priority[new_status]
        
        if new_priority > current_priority:
            key_status[letter] = new_status
    
    # Initialize animation states
    is_animating = False
    animation_start_time = 0
    animation_tile_index = 0
    current_guess_results = []
    current_guess_word = ""
    
    # Initialize shaking state
    is_shaking = False
    shake_start_time = 0
    
    return (start_word, target_word, grid_data, grid_results, 
            current_row, current_col, 
            game_over, did_win, key_status,
            is_animating, animation_start_time, animation_tile_index, 
            current_guess_results, current_guess_word,
            is_shaking, shake_start_time)
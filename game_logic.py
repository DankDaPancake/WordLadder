import random
import string
import os
from collections import Counter

import constants as const

def load_word_list(filename):
    with open(filename) as f:
        for line in f:
            lenfile = "wordlist" + str(len(line)) + ".txt"
            with open(os.path.join(os.path.dirname(__file__), lenfile), 'w') as out:
                out.write(line.strip().upper())
        # words = [line.strip().upper() for line in f]
    # return words
    return None

def get_color_hints(guess_word, target_word):
    results = ["grey"] * const.GRID_COLS
    target_counts = Counter(target_word)
    
    for i in range(len(guess_word)):
        if guess_word[i] == target_word[i]:
            results[i] = "green"
            target_counts[guess_word[i]] -= 1
    
    for i in range(len(guess_word)):
        if results[i] == "green":
            continue
        if guess_word[i] in target_counts and target_counts[guess_word[i]] > 0:
            results[i] = "yellow"
            target_counts[guess_word[i]] -= 1
    
    return results

def is_one_letter_diff(word_a, word_b):
    if len(word_a) != len(word_b):
        return False
    
    diff_count = 0
    for i in range(len(word_a)):
        if word_a[i] != word_b[i]:
            diff_count += 1
            
    return diff_count == 1

def is_valid_step(previous_word, new_guess, word_list):
    if new_guess.upper() not in word_list:
        print(f"'{new_guess}' is not a valid word.")
        return False
    
    if not is_one_letter_diff(new_guess, previous_word):
        print(f"'{new_guess}' must be one letter difference from '{previous_word}'")
        return False
    
    return True

def reset_game(word_list):
    # Initialize data for new game
    
    start_word = random.choice(word_list)
    while len(start_word) != const.GRID_COLS:
        start_word = random.choice(word_list)
    
    target_word = random.choice(word_list)
    while start_word == target_word:
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
    
    hints_left = 10
    
    key_status = {key: "empty" for row in const.KEYBOARD_LAYOUT for key in row}
    status_priority = {"green": 3, "yellow": 2, "grey": 1, "empty": 0}
    
    for i, letter in enumerate(start_word):
        new_status = grid_results[0][i]
        current_priority = status_priority[key_status[letter]]
        new_priority = status_priority[new_status]
        
        if new_priority > current_priority:
            key_status[letter] = new_status
    
    return (start_word, target_word, grid_data, grid_results, 
            current_row, current_col, 
            game_over, did_win, key_status, 
            hints_left)
    
def find_next_step(previous_word, target_word, word_list):
    alphabet = string.ascii_uppercase
    
    possible_steps = []
    
    for i in range(len(previous_word)):
        original_char = previous_word[i]
        
        for letter in alphabet:
            if letter in original_char:
                continue
            
            new_guess = list(previous_word)
            new_guess[i] = letter
            new_guess = "".join(new_guess)
            
            if new_guess in word_list:
                possible_steps.append(new_guess)
    
    if not possible_steps:
        return None
    
    best_step = None
    best_score = -1
    
    for step in possible_steps:
        if step == target_word:
            return step
        
        hints = get_color_hints(step, target_word)
        score = 0
        for hint in hints:
            if hint == "green":
                score += 2
            elif hint == "yellow":
                score += 1
                
        if score > best_score:
            best_score = score
            best_step = step
            
    return best_step
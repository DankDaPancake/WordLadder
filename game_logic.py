import random
import string
import requests
import json
import os
import time
from collections import Counter

import constants as const

def load_word_list(word_length):
    
    filename = f"word_data/wordlist_{word_length:02d}.txt"
    
    with open(filename) as f:
        words = [line.strip().upper() for line in f]
    # return words
    return words

def get_color_hints(guess_word, target_word):
    results = ["grey"] * len(target_word)
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

def get_min_path_length(word_length):
    """Return the minimum required path length for the given word length."""
    if word_length >= 10:  # Long words need shorter minimum paths
        return 2
    else:  # Shorter words need longer minimum paths
        return 3

def reset_game(word_list, word_length, game_config):
    # Initialize data for new game
    print("Generating new ladder...")
    start_word = random.choice(word_list)
    
    # Calculate appropriate path length based on word length for playability
    # New rule: shorter words can have longer paths, longer words get shorter paths
    if word_length <= 4:
        path_length = random.randint(3, 6)  # 4-letter words: moderate to long paths
    elif word_length <= 6:
        path_length = random.randint(4, 7)  # 5-6 letter words: longer paths allowed
    elif word_length <= 8:
        path_length = random.randint(4, 8)  # 7-8 letter words: longest paths
    elif word_length == 9:
        path_length = random.randint(3, 6)  # 9-letter words: medium paths
    elif word_length >= 10:  # 10+ letters
        path_length = random.randint(2, 4)  # Long words: short paths only (2-4 steps)
    
    current_word = start_word
    path = [start_word]
    
    max_retries = const.MAX_PATH_GENERATION_RETRIES
    retry_count = 0
    
    while retry_count < max_retries:
        current_word = start_word
        path = [start_word]
        success = True
        
        for step in range(path_length):
            valid_next_steps = find_all_step(current_word, word_list)
            valid_next_steps = [step for step in valid_next_steps if step not in path]
            
            if not valid_next_steps:
                print(f"Hit dead end at step {step + 1}/{path_length}, retry {retry_count + 1}")
                success = False
                break
                        
            current_word = random.choice(valid_next_steps)
            path.append(current_word)
        
        if success:
            break
        
        retry_count += 1
        # Reduce path length for retries to increase success chance
        min_path = get_min_path_length(word_length)
        path_length = max(min_path, path_length - 1)
    
    if retry_count >= max_retries:
        print("Multiple dead ends encountered, using shorter path")
        # Last resort: very short path
        current_word = start_word
        path = [start_word]
        valid_next_steps = find_all_step(current_word, word_list)
        if valid_next_steps:
            current_word = random.choice(valid_next_steps)
            path.append(current_word)
        else:
            # Extremely rare case - regenerate with different start word
            return reset_game(word_list, word_length, game_config)
    
    target_word = path[-1]  # Use the last word in the path as target
    
    # Ensure we meet minimum path length requirement for this word length
    min_required_length = get_min_path_length(word_length)
    if len(path) < min_required_length:
        print(f"Path too short ({len(path)} steps, need {min_required_length}), regenerating ladder...")
        return reset_game(word_list, word_length, game_config)
    
    print(f"Successfully generated path: {path}")
    print(f"Start: {start_word} | Target: {target_word} | Path length: {len(path)} steps")
    
    grid_data = [["" for _ in range(game_config["GRID_COLS"])] for _ in range(game_config["GRID_ROWS"])]
    grid_results = [["empty" for _ in range(game_config["GRID_COLS"])] for _ in range(game_config["GRID_ROWS"])]

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
        if letter in key_status:
            current_priority = status_priority[key_status[letter]]
            new_priority = status_priority[new_status]
            
            if new_priority > current_priority:
                key_status[letter] = new_status
    
    return (start_word, target_word, grid_data, grid_results, 
            current_row, current_col, 
            game_over, did_win, key_status, 
            hints_left, path)
    
def find_next_step(previous_word, target_word, word_list):
    possible_steps = find_all_step(previous_word, word_list)
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

def find_all_step(previous_word, word_list):
    alphabet = string.ascii_uppercase
    
    possible_steps = set()
    
    for i in range(len(previous_word)):
        original_char = previous_word[i]
        for letter in alphabet:
            if letter == original_char:
                continue
            
            new_guess = list(previous_word)
            new_guess[i] = letter
            new_guess = "".join(new_guess)
            
            if new_guess in word_list:
                possible_steps.add(new_guess)
    
    return list(possible_steps)

def fetch_word_definition(word):
    """
    Fetch word definition from dictionary API.
    Returns a dictionary with parsed definition data or None if failed.
    """
    try:
        url = f"{const.DICTIONARY_API_URL}{word.lower()}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return parse_definition_data(data[0])
        
        return None
    except (requests.RequestException, json.JSONDecodeError, KeyError):
        return None

def parse_definition_data(word_data):
    """
    Parse the JSON response from dictionary API into a simplified format.
    Returns a dictionary with word, phonetic, and meanings.
    """
    try:
        parsed = {
            "word": word_data.get("word", ""),
            "phonetic": word_data.get("phonetic", ""),
            "meanings": []
        }
        
        # Extract up to 3 meanings to avoid overwhelming the screen
        meanings = word_data.get("meanings", [])[:3]
        
        for meaning in meanings:
            part_of_speech = meaning.get("partOfSpeech", "")
            definitions = meaning.get("definitions", [])[:2]  # Max 2 definitions per part of speech
            
            for definition in definitions:
                def_text = definition.get("definition", "")
                example = definition.get("example", "")
                
                # Truncate long definitions
                if len(def_text) > const.MAX_DEFINITION_LENGTH:
                    def_text = def_text[:const.MAX_DEFINITION_LENGTH] + "..."
                
                parsed["meanings"].append({
                    "partOfSpeech": part_of_speech,
                    "definition": def_text,
                    "example": example[:60] + "..." if len(example) > 60 else example
                })
        
        return parsed
    except (KeyError, AttributeError):
        return None

def get_dictionary_hint_from_path(previous_word, solution_path):
    """
    Get the next step word from the pre-generated solution path and fetch its dictionary definition.
    Returns tuple: (hint_word, definition_data)
    """
    try:
        # Find the current position in the path
        current_index = solution_path.index(previous_word)
        
        # Get the next word in the path if it exists
        if current_index + 1 < len(solution_path):
            hint_word = solution_path[current_index + 1]
            definition = fetch_word_definition(hint_word)
            return hint_word, definition
        else:
            # We're at the end of the path (shouldn't happen normally)
            return None, None
            
    except ValueError:
        # previous_word not found in path, fall back to old method
        print(f"Warning: {previous_word} not found in solution path, using fallback hint")
        return None, None

def get_dictionary_hint(previous_word, target_word, word_list):
    """
    Get the next step word and fetch its dictionary definition.
    Returns tuple: (hint_word, definition_data)
    """
    hint_word = find_next_step(previous_word, target_word, word_list)
    
    if hint_word:
        definition = fetch_word_definition(hint_word)
        return hint_word, definition
    
    return None, None

# Timer and Personal Best System
BEST_TIMES_FILE = "best_times.json"

def load_best_times():
    """Load personal best times from JSON file."""
    try:
        if os.path.exists(BEST_TIMES_FILE):
            with open(BEST_TIMES_FILE, 'r') as f:
                return json.load(f)
        else:
            return {}
    except (json.JSONDecodeError, IOError):
        return {}

def save_best_times(best_times):
    """Save personal best times to JSON file."""
    try:
        with open(BEST_TIMES_FILE, 'w') as f:
            json.dump(best_times, f, indent=2)
    except IOError:
        print("Failed to save best times")

def update_best_time(word_length, completion_time):
    """Update best time for a specific word length if it's a new record."""
    best_times = load_best_times()
    key = str(word_length)
    
    # Round completion time to 2 decimal places
    rounded_time = round(completion_time, 2)
    
    if key not in best_times or rounded_time < best_times[key]:
        best_times[key] = rounded_time
        save_best_times(best_times)
        return True  # New record!
    return False

def get_best_time(word_length):
    """Get the best time for a specific word length."""
    best_times = load_best_times()
    return best_times.get(str(word_length), None)

def format_time(seconds):
    """Format time in MM:SS format."""
    if seconds is None:
        return "--:--"
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


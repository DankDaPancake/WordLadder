# 🎃 Halloween Word Ladder 🦇

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)

A spooky Halloween-themed Word Ladder puzzle game built with Python and Pygame! Transform one word into another by changing exactly one letter at a time, with each step creating a valid English word. Features atmospheric Halloween visuals, intelligent hint system, and personal best time tracking.

---

## 🎮 Game Features

### Core Word Ladder Mechanics
* **Word Transformation:** Change one letter at a time to transform the start word into the target word
* **Valid Word Validation:** Every intermediate step must be a valid English word
* **Multiple Word Lengths:** Choose from 4-15 letter words for varying difficulty levels
* **Path Generation:** Intelligent algorithm ensures solvable puzzles with optimal path lengths

### Halloween Theme 🎃
* **Spooky Atmosphere:** Dark purple backgrounds with bat swarm overlays
* **Halloween Colors:** Pumpkin orange, spooky greens, and blood red accents
* **Themed Assets:** Corgi pumpkin mascots, decorative pumpkins, and flying bats
* **Custom Font:** SpookyHalloweenPersonalUse font for authentic Halloween feel

### Smart Hint System 🔮
* **Dictionary Integration:** Real-time word definitions from online dictionary API
* **Path-Based Hints:** Intelligent hints derived from the optimal solution path
* **Limited Usage:** Strategic hint system encourages thoughtful gameplay
* **Side Panel Display:** Hints appear in atmospheric side panels

### Timer & Progress Tracking ⏱️
* **Live Timer:** Real-time gameplay timer with millisecond precision
* **Personal Bests:** Automatic tracking and saving of best completion times
* **JSON Storage:** Persistent best time records stored locally
* **Performance Display:** View your best times for each word length

---

## 🎯 How to Play

1. **Start the Game:** Choose your desired word length (4-15 letters)
2. **Transform Words:** Change exactly one letter per step to create valid words
3. **Reach the Target:** Transform the start word into the target word
4. **Use Hints Wisely:** Get dictionary definitions or path hints when stuck
5. **Beat Your Time:** Try to complete puzzles faster than your personal best!

### Example Word Ladder:
```
CAT → COT → COG → DOG
(CAT to DOG in 3 steps)
```

## 🚀 Getting Started

### Prerequisites

* **Python 3.10 or newer** - [Download Python](https://www.python.org/downloads/)
* **Internet Connection** - Required for dictionary API hints
* **Windows/macOS/Linux** - Cross-platform compatibility

### Installation Steps

---

1. **Clone the Repository**
    ```bash
    git clone https://github.com/DankDaPancake/WordLadder.git
    cd WordLadder
    ```

2. **Create Virtual Environment (Recommended)**
    ```bash
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Game**
    ```bash
    python main.py
    ```

## 🎮 Controls

* **Mouse:** Navigate menus and click buttons
* **Keyboard:** Type letters to fill the word grid
* **Enter:** Submit your word attempt
* **Backspace:** Delete the last letter
* **Hint Button:** Get dictionary definitions or path hints
* **Back Button:** Return to main menu

---

## 📁 Project Structure

```
WordLadder/
├── assets/                    # Game assets and media files
│   ├── Cute-Corgi-Pumpkin.png       # Left mascot image
│   ├── corg-removebg.png            # Right mascot image  
│   ├── bat swarm.png               # Background overlay
│   ├── easy pumpkin.png            # Decorative pumpkin
│   └── SpookyHalloweenPersonalUse.ttf # Halloween font
├── word_data/                 # Word lists for different lengths
│   ├── wordlist_04.txt             # 4-letter words
│   ├── wordlist_05.txt             # 5-letter words
│   └── ... (wordlist_06.txt to wordlist_15.txt)
├── main.py                   # Main game loop and state management
├── constants.py              # Game constants (colors, sizes, layouts)
├── drawing.py                # All rendering and UI functions  
├── game_logic.py             # Game logic, path generation, hints
├── best_times.json           # Personal best time storage (auto-generated)
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🎯 Game Mechanics Deep Dive

### Word Ladder Rules
1. Start with the given starting word
2. Change exactly **one letter** to create a new valid word
3. Repeat until you reach the target word
4. Every intermediate word must be valid English

### Difficulty Scaling
* **4-6 letters:** Beginner friendly, shorter paths
* **7-9 letters:** Intermediate challenge, moderate paths  
* **10-12 letters:** Advanced difficulty, longer paths
* **13-15 letters:** Expert level, complex transformations

### Hint System Details
* **Dictionary Hints:** Real definitions from api.dictionaryapi.dev
* **Path Hints:** Strategic hints from the optimal solution
* **Limited Use:** Encourages strategic thinking
* **Smart Timing:** Hints adapt based on progress

## 🛠️ Technical Features

* **Cross-Platform:** Works on Windows, macOS, and Linux
* **Modular Design:** Clean separation of concerns across files
* **API Integration:** Real-time dictionary lookups
* **Data Persistence:** JSON-based best time storage
* **Scalable Assets:** Automatic image scaling and optimization
* **Error Handling:** Robust fallback systems for network issues

## 🎨 Customization

The game's Halloween theme can be customized by modifying:
* **Colors:** Edit values in `constants.py`
* **Images:** Replace files in `assets/` directory
* **Word Lists:** Add custom word files to `word_data/`
* **Fonts:** Change font paths in the drawing module

## 📝 License

Created by DankDaPancake - Feel free to fork and modify!

## 🎃 Happy Halloween! 🦇

Enjoy this spooky twist on the classic Word Ladder puzzle game!
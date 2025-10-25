# Pygame Wordle Clone

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

A recreation of the famous game Wordle that took the internet by storm in late 2021. This project is a complete, playable desktop application built from scratch using Python and the Pygame library.

This version functions as a "Wordle Unlimited," allowing you to play as many rounds as you'd like.

---

## Features

This clone includes all the core features of the original, plus several enhancements to improve the user experience:

* **Core Wordle Logic:** Guesses are evaluated and tiles change color based on the original rules:
    * **Green:** Correct letter in the correct position.
    * **Yellow:** Correct letter in the wrong position.
    * **Grey:** Letter not in the secret word.
* **Unlimited Play:** When a game ends, you can press **ENTER** to immediately reset the game and play again with a new secret word.
* **Virtual Keyboard:** A full on-screen keyboard allows the game to be played with only a mouse. It includes clickable **"ENTER"** and **"DEL"** keys.
* **Invalid Word Animation:** If you submit a word that isn't in the game's dictionary, the current row will shake to provide instant feedback.
* **Reveal Animation:** When a valid word is submitted, each letter "jumps" as its color is revealed one by one.

---

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### 1. Prerequisites: Install Python

This project requires **Python 3.10 or newer**.

* Go to the official Python website: [python.org/downloads](https://www.python.org/downloads/)
* Download the installer for your operating system (Windows, macOS, or Linux).
* **Important (Windows Only):** During the installation, make sure to check the box that says **"Add Python to PATH"**.

### 2. Environment Setup (Recommended)

It is highly recommended to use a **Python Virtual Environment (`venv`)** to manage your project's dependencies.

A `venv` is a self-contained directory that holds a specific Python interpreter and all the libraries your project needs. This prevents conflicts between projects and keeps your global Python installation clean.

---

## Installation & Running

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/DankDaPancake/Wordle.git](https://github.com/DankDaPancake/Wordle.git)
    cd pygame-wordle
    ```
    or 
    ```bash
    git clone https://github.com/DankDaPancake/Wordle.git
    cd pygame-wordle
    ```

2.  **Create and Activate Your Virtual Environment**

    * On **macOS / Linux**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    * On **Windows**:
        ```bash
        py -m venv venv
        .\venv\Scripts\activate
        ```
    *(Your terminal prompt should now have a `(venv)` prefix)*

3.  **Install Dependencies**

    This project requires the `pygame` library. A `requirements.txt` file is included to install it easily.
    ```bash
    pip install -r requirements.txt
    ```
    *(**Note:** If you haven't created this file, activate your venv, run `pip install pygame`, and then run `pip freeze > requirements.txt` to create it.)*

4. **Download the source dictionary**
    The game runs based on my modified dictionary, please download and paste into Wordle/
    Link: https://drive.google.com/drive/folders/1BdnN2-PLw5gN-PWRA-oh2_Cd6HFwRsX6?usp=sharing

5.  **Run the Game!**
    ```bash
    python main.py
    ```
    or just click the "Run code" button.

---

## Project Structure

The project is organized into several modules for a clean separation of concerns:

```
pygame-wordle/ 
├── .venv/          # The virtual environment directory (ignored by git) 
├── main.py         # Main game loop, state machine, and event handling 
├── constants.py    # All game constants (colors, sizes, layout)
├── drawing.py      # All functions that draw to the screen 
├── game_logic.py   # Game state functions (reset, check_guess, etc.) 
├── wordlist.txt    # The dictionary of valid words 
├── requirements.txt # Project dependencies 
└── README.md
```

### Note
The project's progress can be tracked from my github's Multiple-Python-Projects, where I finished the project before cloning to their own repositories:
https://github.com/DankDaPancake/Multiple-Python-Projects
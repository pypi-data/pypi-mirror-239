# PyGameBox

[![CI / CD](https://github.com/software-students-fall2023/3-python-package-exercise-prime-order/actions/workflows/build-release.yml/badge.svg)](https://github.com/software-students-fall2023/3-python-package-exercise-prime-order/actions/workflows/build-release.yml)
![Version](https://img.shields.io/github/v/tag/software-students-fall2023/3-python-package-exercise-prime-order?label=Version)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/software-students-fall2023/3-python-package-exercise-prime-order/blob/main/LICENSE)

## Team Members

* [Aavishkar Gautam](https://github.com/aavishkar6)
* [Avaneesh Devkota](https://github.com/avaneeshdevkota)
* [Soyuj Jung Basnet](https://github.com/basnetsoyuj)

## Description

PyGameBox is a versatile Python package that simplifies the development of several popular text-based games.
It abstracts away the intricate details of game logic, allowing you to effortlessly import and integrate the following
games into your own projects:

* [Guess the Number](#guess-the-number)
* [Rock, Paper, Scissors](#rock-paper-scissors)
* [Word Scramble](#word-scramble)
* [Hangman](#hangman)
* [Wordle](#wordle)

# Getting Started

## Prerequisites

Before you start, make sure you have Python 3.7 or higher installed on your system. You can download Python from
the [official website](https://www.python.org/downloads/).

## Installation

You can install the package via pip:

```bash
pip install pygamebox
```

Check out `pygamebox` package on PYPI: [https://pypi.org/project/pygamebox](https://pypi.org/project/pygamebox/).

## Usage

After installing the package, import PyGameBox to your program.

```python
from pygamebox import *
```

PyGameBox consists of the game classes: `GuessTheNumber`, `RockPaperScissors`, `WordScramble`, `Hangman`, and `Wordle`.

> **Note**: If you want to implement any one of these games, you can simply import it, instantiate a game object, and
> call `play()`
> on the game object. PyGameBox will handle all the game logic.
>
> However, if you wish to handle the game logic yourself,
> PyGameBox also provides you with a host of helper functions designed to make the implementation as simple as use.

## Example use case

Check out `examples/play.py` to see how to run the games using the `pygamebox` package.

You can run the demo using:

```bash
python examples/play.py
```

## Guess The Number

```python
from pygamebox import GuessTheNumber

game = GuessTheNumber()
game.play()
```

### Screenshot

![](https://github.com/software-students-fall2023/3-python-package-exercise-prime-order/blob/main/images/GuessTheNumber.png?raw=True)

### Class Attributes

* `DEFAULT_START` (`int`): The default start of the range for the number to guess (inclusive), which is `1`.
* `DEFAULT_END` (`int`): The default end of the range for the number to guess (inclusive), which is `100`.

### Methods

1. `__init__(self, start: int = DEFAULT_START, end: int = DEFAULT_END) -> None`
    * **Description**: Creates an instance the game with a specified start and end range.
    * **Parameters**:
        * `start` (`int`, optional): The start of the range for the number to be guessed. Defaults to `DEFAULT_START`.
        * `end` (`int`, optional): The end of the range for the number to be guessed. Defaults to `DEFAULT_END`.

2. `reset(self) -> None`
    * **Description**: Resets the game by generating a new random number and setting the number of guesses to `0`.

3. `get_user_guess(self) -> str`
    * **Description**: Gets the user's guess as a string.
    * **Returns**: The user's guess as a string.

4. `validate_input(self, guess: Union[str, int]) -> bool`
    * **Description**: Validates the user's guess.
    * **Parameters**:
        * `guess` (`Union[str, int]`): The user's guess.
    * **Returns**: `True` if the guess is valid; `False` otherwise.

5. `guess(self, user_guess: int) -> int`
    * **Description**: Checks if the user's guess is correct.
    * **Parameters**:
        * `user_guess` (`int`): The user's guess.
    * **Returns**:
        * `-1` if the guess is too low.
        * `1` if the guess is too high.
        * `0` if the guess is correct.

6. `turn(self, user_guess: Union[str, int]) -> bool`
    * **Description**: Runs a turn of the game.
    * **Parameters**:
        * user_guess (Union[str, int]): The user's guess.
    * **Returns**: `True` if the user guessed the number, `False` otherwise.

7. `play(self) -> None`
    * **Description**: Plays the game. Takes guesses from the user and checks until the user guesses the correct number.

## Rock, Paper, Scissors

```python
from pygamebox import RockPaperScissors

game = RockPaperScissors()
game.play()
```

### Screenshot

![](https://github.com/software-students-fall2023/3-python-package-exercise-prime-order/blob/main/images/RPS.png?raw=True)

### Class Attributes

* `DEFAULT_ROUNDS` (`int`): The default number of rounds to play, which is `1`.

### Methods

1. `__init__(self) -> None`
    * **Description**: Creates an instance of the rock, paper, scissors game.
2. `get_user_throw(self) -> int`
    * **Description**: Prompts the user to choose a move (Rock, Paper, or Scissors).
    * **Returns**: An `int` (**0**: Rock, **1**: Paper, **2**: Scissors).
3. `validate_input(self, user_input: Union[str, int])` -> bool`
    * **Description**: Checks if the user's input is valid.
    * **Parameters**:
        * `user_input` (`Union[str, int]`): The user's input.
    * **Returns**: `True` if the input is valid (1, 2, or 3). `False` otherwise.
4. `throw() -> int`
    * **Description**: Generates a random choice for the computer (Rock, Paper, or Scissors).
    * **Returns**: The computer's choice as an `int` (**0**: Rock, **1**: Paper, **2**: Scissors).
5. `round(user_throw: int, computer_throw: int) -> int`
    * **Description**: Determines the result of a round based on the user's and computer's choices.
    * **Parameters**:
        * `user_throw` (`int`): The user's choice.
        * `computer_throw` (`int`): The computer's choice.
    * **Returns**:
        * `1` if the user wins.
        * `-1` if the computer wins.
        * `0` if it's a draw.
6. `validate_round_input(rounds: int) -> bool`
    * **Description**: Validates the user's input to ensure it's a valid number of rounds (1 or greater).
    * **Parameters**:
        * `rounds` (`int`): The number of rounds to play.
    * **Returns**: `True` if the input is valid, `False` otherwise.
7. `play(self, rounds: int = DEFAULT_ROUNDS) -> None`
    * **Description**: Runs the Rock, Paper, Scissors game for a specified number of rounds.
    * **Parameters**:
        * `rounds` (`int`, optional): The number of rounds to play (defaults to `DEFAULT_ROUNDS`).

## Word Scramble

```python
from pygamebox import WordScramble

game = WordScramble()
game.play()
```

### Screenshot

![](https://github.com/software-students-fall2023/3-python-package-exercise-prime-order/blob/main/images/WordScramble.png?raw=True)

### Class Attributes

* `DEFAULT_DIFFICULTY` (`str`): The default difficulty level, which is `'easy'`.
* `DEFAULT_ATTEMPTS` (`int`): The default number of attempts allowed, which is `3`.

### Methods:

1. `__init__(self) -> None`
    * **Description**: Creates an instance of the Word Scramble game by importing list of words for different
      difficulty levels.
2. `reset(self, difficulty: str = DEFAULT_DIFFICULTY, attempts: int = DEFAULT_ATTEMPTS) -> None`
    * **Description**: Resets the game to the specified difficulty level and number of attempts. Samples a random word
      from the corresponding difficulty list and scrambles it.
    * **Parameters**:
        * `difficulty` (`str`, optional): A difficulty level (`'easy'`, `'medium'`, `'hard'`) (defaults
          to `DEFAULT_DIFFICULTY`).
        * `attempts` (`int`, optional): The number of attempts allowed (defaults to `DEFAULT_ATTEMPTS`)
3. `scramble_word(word: str) -> str`
    * **Description**: Scrambles a given word.
    * **Parameters**:
        * `word` (`str`): The word to scramble.
    * **Returns**: The scrambled word.
4. `get_word_list(self, difficulty: str) -> list[str]`
    * **Description**: Retrieves a list of words based on the specified difficulty level.
    * **Parameters**:
        * `difficulty` (`str`): A difficulty level (`'easy'`, `'medium'`, `'hard'`)
    * **Returns**: A list of words for the given difficulty.
5. `validate_input(self, user_input: str) -> bool`
    * **Description**: Validates the user's input to ensure it contains the same number of characters as the scrambled
      word.
    * **Parameters**:
        * `user_input` (`str`): The user's input.
    * **Returns**: `True` if the input is valid, `False` otherwise.
6. `guess(self, user_input: str) -> bool`
    * **Description**: Checks if the user's guess is correct and updates `attempts`.
    * **Parameters**:
        * `user_input` (`str`): The user's input.
    * **Returns**: `True` if the guess is correct, `False` otherwise.
7. `play(self, difficulty: str = DEFAULT_DIFFICULTY, attempts: int = DEFAULT_ATTEMPTS) -> None`
    * **Description**: Starts a game session for a specified difficulty level and number of attempts.
    * **Parameters**:
        * `difficulty` (`str`, optional): A difficulty level (`'easy'`, `'medium'`, `'hard'`) (defaults
          to `DEFAULT_DIFFICULTY`).
        * `attempts` (`int`, optional): The number of attempts allowed (defaults to `DEFAULT_ATTEMPTS`)

## Hangman

```python
from pygamebox import Hangman

game = Hangman()
game.play()
```

### Screenshot

![](https://github.com/software-students-fall2023/3-python-package-exercise-prime-order/blob/main/images/Hangman.png?raw=True)

### Class Attributes

* `DEFAULT_DIFFICULTY` (`str`): The default difficulty level, which is `'easy'`.
* `DEFAULT_ATTEMPTS` (`int`): The default number of attempts allowed, which is `10`.

### Methods:

1. `__init__(self) -> None`
    * **Description**: Creates an instance of the Hangman game with a set of words for different difficulty levels.

2. `reset(self, difficulty: str = DEFAULT_DIFFICULTY, attempts: int = DEFAULT_ATTEMPTS) -> None`
    * **Description**: Resets the game to the specified difficulty level and number of attempts, and chooses a random
      word from the list.
    * **Parameters**:
        * `difficulty` (`str`, optional): A difficulty level (`'easy'`, `'medium'`, `'hard'`) (defaults
          to `DEFAULT_DIFFICULTY`).
        * `attempts` (`int`, optional): The number of attempts allowed (defaults to `DEFAULT_ATTEMPTS`)

3. `get_word_list(self, difficulty: str) -> list[str]`
    * **Description**: Retrieves a list of words based on the `difficulty` level.
    * **Parameters**:
        * `difficulty` (`str`): A difficulty level (`'easy'`, `'medium'`, `'hard'`)
    * **Returns**: A list of words for the given difficulty.

4. `validate_input(self, user_input: str) -> bool`
    * **Description**: Validates the user's input to ensure it is a single letter and that it hasn't been guessed.
    * **Parameters**:
        * `user_input` (`str`): The user's input.
    * **Returns**: `True` if the input is valid, `False` otherwise.

5. `guess(self, user_input: str) -> bool`
    * **Description**: Checks if the user's guess is correct and updates the game status (remaining attempts and guessed
      letters).
    * **Parameters**:
        * `user_input` (`str`): The user's guess.
    * **Returns**: `True` if the user has guessed the entire word, `False` otherwise.

6. `print_partial(self) -> None`
    * **Description**: Prints the word with the guessed letters filled in and displays the letters remaining to guess.

7. `play(self, difficulty: str = DEFAULT_DIFFICULTY, attempts: int = DEFAULT_ATTEMPTS) -> None`
    * **Description**: Starts a Hangman game session.
    * **Parameters**:
        * `difficulty` (`str`, optional): A difficulty level (`'easy'`, `'medium'`, `'hard'`) (defaults
          to `DEFAULT_DIFFICULTY`).
        * `attempts` (`int`, optional): The number of attempts allowed (defaults to `DEFAULT_ATTEMPTS`)

## Wordle

```python
from pygamebox import Wordle

game = Wordle()
game.play()
```

### Screenshot

![](https://github.com/software-students-fall2023/3-python-package-exercise-prime-order/blob/main/images/Wordle.png?raw=True)

### Methods:

1. `__init__(self) -> None`
    * **Description**: Initializes the Wordle game with a list of possible words, valid words, and game parameters, such
      as
      the current word, guesses, and attempts.
2. `reset(self, attempts: int = DEFAULT_ATTEMPTS) -> None`
    * **Description**: Resets the game, generating a new word to guess and resetting the guesses and attempts.
    * **Parameters**:
        * `attempts` (`int`, optional): The number of attempts allowed (defaults to `DEFAULT_ATTEMPTS`).
3. `get_user_input() -> str`
    * **Description**: Gets the user's input (the guessed word).
    * **Returns**: The user's input as a string.
4. `validate_input(self, guess: str) -> bool`
    * **Description**: Ensures guessed word is in the list of valid words.
    * **Parameters**:
        * `guess` (`str`): The user's input (guessed word).
    * **Returns**: `True` if the word is valid, `False` otherwise.
5. `check_win(self, guess: str) -> bool`
    * **Description**: Checks if the user's guess is correct (equals the hidden word).
    * **Parameters**:
        * `guess` (`str`): The user's input (guessed word).
    * **Returns**: `True` if the guess is correct, `False` otherwise.
6. `check_guess(self, guess: str) -> list[int]`
    * **Description**: Checks what characters in the guess are in the correct positions, are misplaced, or not present.
    * **Parameters**:
        * `guess` (`str`): The user's input (guessed word).
    * **Returns**: A list of integers representing the status of each character in the guess (**0**: Correct, **1**:
      Misplaced, **-1**: Not present).
7. `print_output(self) -> None`
    * **Description**: Prints the Wordle game state, including feedback on previous guesses.
8. `play(self, attempts: int = DEFAULT_ATTEMPTS) -> None`
    * **Description**: Starts a Wordle game session for a specified number of attempts.
    * **Parameters**:
        * `attempts` (`int`, optional): The number of attempts allowed (defaults to `DEFAULT_ATTEMPTS`).

---

# Contributing

If you'd like to contribute to the PyGameBox project, follow these steps to set up your development environment:

* Fork the repository or clone it directly:
    ```bash
    git clone https://github.com/software-students-fall2023/3-python-package-exercise-prime-order.git
    ```

* `cd` to the folder and create/activate virutal environment:
    ```bash
    pipenv shell
    ```

* Download and install dependencies.
    ```bash
    pipenv install
    ```

* You can work on the module, add other games, or resolve existing issues. Create unit tests for your functions to test
  them
  in [`tests/`](https://github.com/software-students-fall2023/3-python-package-exercise-prime-order/blob/main/tests).

  Run the tests using:
    ```bash
    python -m pytest
    ```

* Push your code changes, create a pull request and contribute to the project's development.

import random
from typing import Union


class GuessTheNumber:
    """
    Implementation of a simple Guess the Number game. It generates a random number and the player guesses what it is.
    The game will tell the player if a guess is too low or too high and count how many guesses have been made.
    """
    DEFAULT_START = 1
    DEFAULT_END = 100

    def __init__(self, start: int = DEFAULT_START, end: int = DEFAULT_END) -> None:
        self.start = start
        self.end = end
        self.number = 0
        self.guesses = 0
        self.reset()

    def reset(self) -> None:
        """
        Resets the game by generating a new random number and setting the number of guesses to 0.

        :return: None
        """
        self.number = random.randint(self.start, self.end)
        self.guesses = 0

    def get_user_guess(self) -> str:
        """
        Gets the user's guess as a string.

        :return: The user's guess as a string.
        """
        return input(f'Guess a number between {self.start} and {self.end}\n> ').strip()

    def validate_input(self, guess: Union[str, int]) -> bool:
        """
        Validates the user's guess.

        :param guess: The user's guess.
        :return: True if the guess is valid, False otherwise.
        """
        try:
            guess = int(guess)
            if guess < self.start or guess > self.end:
                raise ValueError
        except (ValueError, TypeError):
            print('Please enter a valid number within the range.')
            return False
        return True

    def guess(self, user_guess: int) -> int:
        """
        Checks if the user's guess is correct.

        :param user_guess: The user's guess.
        :return: -1 if the guess is too low, 1 if the guess is too high, 0 if the guess is correct.
        """
        self.guesses += 1
        if user_guess < self.number:
            return -1
        elif user_guess > self.number:
            return 1
        else:
            return 0

    def turn(self, user_guess: Union[str, int]) -> bool:
        """
        Runs a turn of the game.

        :param user_guess: The user's guess.
        :return: True if the user guessed the number, False otherwise.
        """
        if self.validate_input(user_guess):
            user_guess = int(user_guess)
            result = self.guess(user_guess)
            if result == -1:
                print('Too low')
            elif result == 1:
                print('Too high')
            else:
                print(f'Correct! You got it in {self.guesses} guesses!')
                return True
        return False

    def play(self) -> None:
        """
        Plays the game.

        :return: None
        """
        self.reset()
        while True:
            user_guess = self.get_user_guess()
            if self.turn(user_guess):
                break

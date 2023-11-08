import collections
import random

from .utils import read_words_file, get_random_word


class WordScramble:
    """
    Implementation of a simple Word Scramble game.
    The player is given a scrambled word and must guess the original word.
    """
    DEFAULT_ATTEMPTS = 3
    DEFAULT_DIFFICULTY = 'easy'

    def __init__(self) -> None:
        words = read_words_file()
        self.words = {
            'easy': list(filter(lambda x: len(x) <= 4, words)),
            'medium': list(filter(lambda x: 5 <= len(x) <= 7, words)),
            'hard': list(filter(lambda x: len(x) >= 8, words))
        }
        self.word = ''
        self.scrambled_word = ''
        self.attempts = 0
        self.reset()

    def reset(self, difficulty: str = DEFAULT_DIFFICULTY, attempts: int = DEFAULT_ATTEMPTS) -> None:
        """
        Resets the game.

        :param difficulty: The difficulty level.
        :param attempts: The number of attempts.
        :return: None
        """
        word_list = self.get_word_list(difficulty)
        self.word = get_random_word(word_list)
        self.scrambled_word = self.scramble_word(self.word)
        self.attempts = attempts

    @staticmethod
    def scramble_word(word: str) -> str:
        """
        Scrambles a word.

        :param word: The word to scramble.
        :return: The scrambled word.
        """
        while True:
            word_chars = list(word)
            random.shuffle(word_chars)
            shuffled_word = ''.join(word_chars)
            if shuffled_word != word:
                return shuffled_word

    def get_word_list(self, difficulty: str) -> list[str]:
        """
        Gets a list of words based on the difficulty level.

        :param difficulty: The difficulty level.
        :return: A list of words.
        """
        if difficulty not in self.words:
            raise ValueError(f"Difficulty level must be one of {list(self.words.keys())}")
        return self.words[difficulty]

    def validate_input(self, user_input: str) -> bool:
        """
        Validates the user's input.

        :param user_input: The user's input.
        :return: True if the user input contains same characters as the scrambled word, False otherwise.
        """
        if collections.Counter(user_input) == collections.Counter(self.scrambled_word):
            return True
        return False

    def guess(self, user_input: str) -> bool:
        """
        Checks if the user's guess is correct.

        :param user_input: The user's input.
        :return: True if the guess is correct, False otherwise.
        """
        if user_input == self.word:
            print(f"You got it! The word was: {self.word}")
            return True

        self.attempts -= 1
        if self.attempts:
            print(f"Incorrect. You have {self.attempts} attempt(s) left. Good Luck!")
        else:
            print(f"Incorrect. You have no attempts left. The word was {self.word}.")
        return False

    def play(self, difficulty: str = DEFAULT_DIFFICULTY, attempts: int = DEFAULT_ATTEMPTS) -> None:
        """
        Plays the game.

        :param difficulty: The difficulty level.
        :param attempts: The number of attempts.
        :return: None
        """
        self.reset(difficulty=difficulty, attempts=attempts)

        print(f"Welcome to Word Scramble Level {difficulty.capitalize()}! You have {attempts} attempts.")
        print("Unscramble the word:", self.scrambled_word)

        while self.attempts:
            user_input = input('> ').lower().strip()
            if self.validate_input(user_input):
                if self.guess(user_input):
                    break
            else:
                print("Guess must contain the same characters as the scrambled word.")

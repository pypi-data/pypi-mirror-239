import string

from colorama import Back, Style

from .utils import read_words_file, get_random_word


class Hangman:
    """
    Implementation of a simple Hangman game.
    The player guesses letters to try to figure out the word.
    """
    DEFAULT_ATTEMPTS = 10
    DEFAULT_DIFFICULTY = 'easy'

    def __init__(self) -> None:
        words = read_words_file()
        self.words = {
            'easy': list(filter(lambda x: len(x) <= 4, words)),
            'medium': list(filter(lambda x: 5 <= len(x) <= 7, words)),
            'hard': list(filter(lambda x: len(x) >= 8, words))
        }
        self.word = ''
        self.attempts = 0
        self.guessed_letters = set()
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
        self.attempts = attempts
        self.guessed_letters.clear()

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
        :return: True if the input is valid, False otherwise.
        """
        if len(user_input) == 1 and user_input.isalpha() and user_input not in self.guessed_letters:
            return True
        return False

    def guess(self, user_input: str) -> bool:
        """
        Checks if the user's guess is correct.

        :param user_input: The user's guess.
        :return: True if the user guessed the entire word, False otherwise.
        """
        self.guessed_letters.add(user_input)

        if user_input not in self.word:
            self.attempts -= 1
            if self.attempts:
                print(f"Incorrect. You have {self.attempts} attempt(s) left. Good luck!")
            else:
                print(f"Incorrect. You have no attempts left. The word was: {self.word.upper()}.")
        else:
            print(f"Correct! The word has {self.word.count(user_input)} '{user_input.upper()}'.")

        return set(self.word).issubset(self.guessed_letters)

    def print_partial(self) -> None:
        """
        Prints the word with the guessed letters filled in and the letters remaining to guess.

        :return: None
        """
        print(' ' * (3 * 13 - len(self.word)), end='')
        for letter in self.word:
            if letter in self.guessed_letters:
                print(letter.upper(), end=' ')
            else:
                print('_', end=' ')
        print()

        # words remaining to guess
        for c in string.ascii_lowercase:
            if c not in self.guessed_letters:
                print(f' {c.upper()} ', end='')
            elif c in self.word:
                print(Back.GREEN + f' {c.upper()} ', end='')
            else:
                print(Back.RED + f' {c.upper()} ', end='')
            print(Style.RESET_ALL, end='')
        print()

    def play(self, difficulty: str = DEFAULT_DIFFICULTY, attempts: int = DEFAULT_ATTEMPTS) -> None:
        """
        Plays the game.

        :param difficulty: The difficulty.
        :param attempts: The number of attempts.
        :return: None
        """
        self.reset(difficulty=difficulty, attempts=attempts)

        print(f"Welcome to Hangman Level {difficulty.capitalize()}! You have {attempts} attempts.")
        print("Guess the letters in the word.")

        while self.attempts:
            self.print_partial()
            user_input = input('> ').lower().strip()
            if self.validate_input(user_input):
                if self.guess(user_input):
                    self.print_partial()
                    print("Congratulations! You win!")
                    break
            else:
                print("Input must be a single letter that hasn't been guessed.")

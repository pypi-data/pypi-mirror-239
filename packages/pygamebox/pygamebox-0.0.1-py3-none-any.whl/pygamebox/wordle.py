from colorama import Back, Style

from .utils import read_file, get_random_word


class Wordle:
    """
    Implementation of a simple Wordle game.
    The player guesses letters to try to figure out the word.
    """
    DEFAULT_ATTEMPTS = 6

    def __init__(self) -> None:
        # all possible wordle words
        self.words_list = read_file('wordle_possibilities.txt')

        # all valid words that can be guessed
        self.words_set = set(read_file('valid_wordle_words.txt'))
        self.words_set.update(self.words_list)

        self.guesses: list[str] = []
        self.word = ''
        self.attempts = 0
        self.reset()

    def reset(self, attempts: int = DEFAULT_ATTEMPTS) -> None:
        """
        Resets the game.

        :param attempts: The number of attempts.
        :return: None
        """
        self.word = get_random_word(self.words_list)
        self.guesses = []
        self.attempts = attempts

    @staticmethod
    def get_user_input() -> str:
        """
        Gets the user's input.

        :return: The user's input.
        """
        return input('> ').strip().lower()

    def validate_input(self, guess: str) -> bool:
        """
        Validates the user's input.

        :param guess: The user's input.
        :return: True if the word is in the wordle list, False otherwise.
        """
        if guess not in self.words_set:
            print('Please enter a valid word.')
            return False
        return True

    def check_win(self, guess: str) -> bool:
        """
        Checks if the user's guess is correct.

        :param guess: The user's guess.
        :return: True if the guess is correct, False otherwise.
        """
        if guess == self.word:
            return True
        return False

    def check_guess(self, guess: str) -> list[int]:
        """
        Check what characters in the guess are in the correct position, misplaced, or not present.

        :param guess: The user's guess.
        :return: A list of integers representing the status of each character in the guess.
                 (0: Correct, 1: Misplaced, -1: Not present)
        """
        count = {c: 0 for c in self.word}
        for c in self.word:
            count[c] += 1

        result = [-1 for _ in range(len(guess))]
        for i, c in enumerate(guess):
            if c == self.word[i]:
                result[i] = 0
                count[c] -= 1

        for i, c in enumerate(guess):
            if result[i] == -1 and count.get(c):
                result[i] = 1
                count[c] -= 1

        return result

    def print_output(self) -> None:
        """
        Prints the wordle game state.

        :return: None
        """
        for word in self.guesses:
            result = self.check_guess(word)
            for i, c in enumerate(word):
                if result[i] == 0:
                    print(Back.GREEN, end='')
                elif result[i] == 1:
                    print(Back.YELLOW, end='')
                else:
                    print(Back.LIGHTBLACK_EX, end='')
                print(f' {c.upper()} ', end='')
                print(Style.RESET_ALL, end='')
            print()

    def play(self, attempts: int = DEFAULT_ATTEMPTS) -> None:
        """
        Plays the game.

        :param attempts: The number of attempts.
        :return: None
        """
        self.reset(attempts=attempts)

        i = 0
        while self.attempts > 0:
            self.print_output()
            user_word = self.get_user_input()
            if self.validate_input(user_word):
                self.guesses.append(user_word)
                if self.check_win(user_word):
                    self.print_output()
                    print('You win!')
                    return
                else:
                    self.attempts -= 1
                    i += 1
        print('You lose! The word was', self.word.upper())

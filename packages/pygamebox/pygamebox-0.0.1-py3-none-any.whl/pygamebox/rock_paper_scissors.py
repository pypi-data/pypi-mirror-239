import random
from typing import Union


class RockPaperScissors:
    """
    Implementation of a simple Rock Paper Scissors game. The player chooses a throw and the computer chooses a throw.
    The game will tell the player if they won, lost, or drew.
    """
    DEFAULT_ROUNDS = 3

    def __init__(self) -> None:
        self.playable = ["Rock", "Paper", "Scissors"]
        self.results = {
            1: "Player Wins",
            -1: "Computer Wins",
            0: "Draw"
        }

    def get_user_throw(self) -> int:
        """
        Gets the user's throw.

        :return: The user's throw as an integer (0: Rock, 1: Paper, 2: Scissors).
        """
        print("\nChoose your throw:")
        for i, label in enumerate(self.playable, start=1):
            print(f'{i}. {label}')
        while True:
            user_input = input("> ")
            if self.validate_input(user_input):
                return int(user_input) - 1
            else:
                print("Please enter a valid choice.")

    @staticmethod
    def validate_input(user_input: Union[str, int]) -> bool:
        """
        Validates the user's input.

        :param user_input: The user's input.
        :return: True if the input is valid, False otherwise.
        """
        if isinstance(user_input, str) and user_input.isdigit():
            user_input = int(user_input)

        if isinstance(user_input, int) and 1 <= user_input <= 3:
            return True

        return False

    @staticmethod
    def throw():
        """
        Generates a random throw for the computer.

        :return: The computer's throw as an integer (0: Rock, 1: Paper, 2: Scissors).
        """
        return random.randint(0, 2)

    @staticmethod
    def round(user_throw: int, computer_throw: int) -> int:
        """
        Checks if the user's throw beats the computer's throw.

        :param user_throw: The user's throw.
        :param computer_throw: The computer's throw.
        :return: 1 if the user wins, -1 if the computer wins, 0 if it's a draw.
        """
        if user_throw == (computer_throw + 1) % 3:
            result = 1
        elif computer_throw == (user_throw + 1) % 3:
            result = -1
        else:
            result = 0
        return result

    @staticmethod
    def validate_round_input(round_input: int) -> bool:
        """
        Validates the user's input.

        :param round_input: The user's input.
        :return: True if the input is valid, False otherwise.
        """
        return round_input >= 1

    def play(self, rounds: int = DEFAULT_ROUNDS) -> None:
        """
        Runs the game for a specified number of rounds.

        :param rounds: The number of rounds to play.
        :return: None
        """
        counter = 0
        if self.validate_round_input(rounds):
            for i in range(rounds):
                # terminate early if the game is already decided
                if abs(counter) > rounds / 2:
                    break

                user_throw = self.get_user_throw()
                computer_throw = self.throw()
                result = self.round(user_throw, computer_throw)

                print(f"You threw {self.playable[user_throw]}")
                print(f"Computer threw {self.playable[computer_throw]}")
                print(f"Round {i + 1}: {self.results[result]}")

                counter += result

            if counter:
                counter = int(counter / abs(counter))
            print(f"\nGame Result: {self.results[counter]}")
        else:
            print("Please enter a valid number of rounds to play.")

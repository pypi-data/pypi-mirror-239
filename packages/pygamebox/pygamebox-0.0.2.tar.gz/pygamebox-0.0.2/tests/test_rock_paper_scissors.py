from pygamebox import RockPaperScissors

ROCK = 0
PAPER = 1
SCISSORS = 2


def test_validate_input():
    game = RockPaperScissors()

    assert game.validate_input(1) is True  # 1 is a valid choice
    assert game.validate_input(2) is True  # 2 is a valid choice
    assert game.validate_input(3) is True  # 3 is a valid choice

    assert game.validate_input('1') is True  # '1' is a valid choice
    assert game.validate_input('2') is True  # '2' is a valid choice
    assert game.validate_input('3') is True  # '3' is a valid choice

    # Invalid input tests

    assert game.validate_input(0) is False  # 0 is not a valid choice
    assert game.validate_input(4) is False  # 4 is not a valid choice
    assert game.validate_input('a') is False  # 'a' is not a valid choice


def test_throw():
    game = RockPaperScissors()

    # Ensure the throw method returns an integer between 0 and 2
    assert isinstance(game.throw(), int)
    assert 0 <= game.throw() <= 2


def test_round():
    game = RockPaperScissors()

    # Tests for different game scenarios
    assert game.round(user_throw=ROCK, computer_throw=ROCK) == 0  # Draw
    assert game.round(user_throw=ROCK, computer_throw=PAPER) == -1  # Computer wins
    assert game.round(user_throw=ROCK, computer_throw=SCISSORS) == 1  # Player wins

    assert game.round(user_throw=PAPER, computer_throw=ROCK) == 1  # Player wins
    assert game.round(user_throw=PAPER, computer_throw=PAPER) == 0  # Draw
    assert game.round(user_throw=PAPER, computer_throw=SCISSORS) == -1  # Computer wins

    assert game.round(user_throw=SCISSORS, computer_throw=ROCK) == -1  # Computer wins
    assert game.round(user_throw=SCISSORS, computer_throw=PAPER) == 1  # Player wins
    assert game.round(user_throw=SCISSORS, computer_throw=SCISSORS) == 0  # Draw


def test_validate_round_input():
    game = RockPaperScissors()

    # Valid round input tests
    assert game.validate_round_input(1) is True  # 1 is valid
    assert game.validate_round_input(10) is True  # 10 is valid

    # Invalid round input tests
    # Non-Positive values are not valid
    assert game.validate_round_input(0) is False
    assert game.validate_round_input(-10) is False

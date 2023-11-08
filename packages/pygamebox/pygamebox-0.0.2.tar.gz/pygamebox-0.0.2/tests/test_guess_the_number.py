from pygamebox import GuessTheNumber


def test_random_number_init():
    game = GuessTheNumber(start=11, end=23)

    # check that number is an integer
    assert isinstance(game.number, int)

    # check that number generated is within range
    assert game.start <= game.number <= game.end


def test_validate_input():
    game = GuessTheNumber(start=1, end=100)

    # in range values
    assert game.validate_input("50") is True
    assert game.validate_input(50) is True

    # out of range values
    assert game.validate_input("-100") is False
    assert game.validate_input(-100) is False

    assert game.validate_input("200") is False
    assert game.validate_input(200) is False

    # non-numeric values
    assert game.validate_input("hello") is False
    assert game.validate_input("!@%^$&!#*34") is False


def test_guess():
    game = GuessTheNumber(start=1, end=100)
    game.number = 50

    # lower than number
    assert game.guess(1) == -1
    # guesses counter should increment
    assert game.guesses == 1

    # higher than number
    assert game.guess(100) == 1
    # guesses counter should increment
    assert game.guesses == 2

    # equal to number
    assert game.guess(50) == 0
    # guesses counter should increment
    assert game.guesses == 3


def test_turn():
    game = GuessTheNumber(start=1, end=100)
    game.number = 50

    # wrong guess should not terminate game
    assert game.turn(1) is False
    # guesses counter should increment
    assert game.guesses == 1

    assert game.turn(100) is False
    assert game.guesses == 2

    # correct guess should terminate game
    assert game.turn(50) is True
    assert game.guesses == 3

    # reset should reset guesses counter
    game.reset()
    assert game.guesses == 0

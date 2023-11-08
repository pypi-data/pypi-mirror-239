from pygamebox import Wordle


def test_initialization():
    game = Wordle()

    # Assert that words_list returns a list of words
    assert isinstance(game.words_list, list)

    # Assert that self.words_list contains words
    assert len(game.words_list) > 0

    # Assert that a word is returned
    assert isinstance(game.word, str)

    # Assert that words is an empty list at first.
    assert game.guesses == []

    # Assert that number of attempts is DEFAULT_ATTEMPTS
    assert game.attempts == game.DEFAULT_ATTEMPTS


def test_validate_input():
    game = Wordle()

    # Assert that validate_input returns true for valid 5 letter wordle words
    assert game.validate_input('apple') is True
    assert game.validate_input('hello') is True

    # Assert that validate_input returns false for invalid words
    assert game.validate_input(' ') is False
    assert game.validate_input('ab123') is False
    assert game.validate_input('qqqqq') is False

    # Assert that validate_input returns false for words that are not 5 letters
    assert game.validate_input('apples') is False


def test_guess():
    game = Wordle()
    game.word = 'apple'

    # Assertion when all the characters are not present in the word
    assert game.check_guess('south') == [-1, -1, -1, -1, -1]

    # Assertion when all the characters are present in correct position
    assert game.check_guess('apple') == [0, 0, 0, 0, 0]

    # Assertion when one character is not present
    assert game.check_guess('apply') == [0, 0, 0, 0, -1]

    game.word = 'alpha'

    # Assertion for misplaced characters
    assert game.check_guess('again') == [0, -1, 1, -1, -1]

    # Duplication of characters should be handled correctly
    # In this case, first and last 'a' are in right position, but the middle 'a' is not present
    assert game.check_guess('abaca') == [0, -1, -1, -1, 0]


def test_win():
    game = Wordle()
    game.word = 'apple'

    # Assert check_win returns true if the word is correct.
    assert game.check_win('apple') is True

    # Assert check_win returns false if the word is incorrect.
    assert game.check_win('mango') is False

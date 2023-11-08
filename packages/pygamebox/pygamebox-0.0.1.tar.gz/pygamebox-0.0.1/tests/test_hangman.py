import pytest

from pygamebox import Hangman


def test_get_word_list():
    game = Hangman()

    # Assert that all words in the easy list have a length less than or equal to 4
    easy_words = game.get_word_list('easy')
    assert all(len(word) <= 4 for word in easy_words)

    # Assert that all words in the medium list have a length between 5 and 7
    medium_words = game.get_word_list('medium')
    assert all(5 <= len(word) <= 7 for word in medium_words)

    # Assert that all words in the hard list have a length greater than or equal to 8
    hard_words = game.get_word_list('hard')
    assert all(len(word) >= 8 for word in hard_words)

    # Assert that an invalid difficulty level raises a ValueError
    with pytest.raises(ValueError):
        game.get_word_list('invalid')


def test_validate_input():
    game = Hangman()
    game.reset('medium', 5)
    game.word = 'apple'

    # Assert that the user's input should contain single alphabetic characters
    assert game.validate_input('b') is True
    assert game.validate_input('asdf') is False
    assert game.validate_input('1') is False
    assert game.validate_input('@') is False

    # Assert that the user's input should not be a letter that has already been guessed
    # True because 'a' has not been guessed yet
    assert game.validate_input('a') is True

    game.guess('a')

    # False because 'a' has already been guessed
    assert game.validate_input('a') is False


def test_guess():
    game = Hangman()
    game.reset('medium', 5)
    game.word = 'apple'

    # assert that guess returns False until the user has guessed the entire word
    # also assert attempts is decremented only when the user guesses incorrectly
    assert game.guess('a') is False
    assert game.attempts == 5

    assert game.guess('p') is False
    assert game.attempts == 5

    assert game.guess('x') is False
    assert game.attempts == 4

    assert game.guess('l') is False
    assert game.attempts == 4

    # assert that guess returns True when the user has guessed the entire word
    assert game.guess('e') is True

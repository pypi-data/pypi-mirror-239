from collections import Counter

import pytest

from pygamebox import WordScramble


def test_scramble_word():
    game = WordScramble()

    # scramble a word
    test_word = 'apple'
    scrambled_word = game.scramble_word(test_word)

    # Assert that the scrambled word contains the same characters as the original word
    assert Counter(test_word) == Counter(scrambled_word)

    # Assert that the scrambled word is not the same as the original word
    assert test_word != scrambled_word


def test_get_word_list():
    game = WordScramble()

    # Get word lists for easy, medium, and hard difficulty levels
    easy_words = game.get_word_list('easy')
    medium_words = game.get_word_list('medium')
    hard_words = game.get_word_list('hard')

    # Assert that all words in the easy list have a length less than or equal to 4
    assert all(len(word) <= 4 for word in easy_words)

    # Assert that all words in the medium list have a length between 5 and 7
    assert all(5 <= len(word) <= 7 for word in medium_words)

    # Assert that all words in the hard list have a length greater than or equal to 8
    assert all(len(word) >= 8 for word in hard_words)

    # Assert that an invalid difficulty level raises a ValueError
    with pytest.raises(ValueError):
        game.get_word_list('invalid')


def test_validate_input():
    game = WordScramble()
    game.reset('easy', 5)
    game.word = 'apple'
    game.scrambled_word = 'pplea'

    # Assert that the user's input should contain the same characters as the scrambled word
    assert game.validate_input('appel') is True
    assert game.validate_input('aple') is False
    assert game.validate_input('applee') is False
    assert game.validate_input('mango') is False


def test_guess():
    game = WordScramble()
    game.reset('easy', 5)
    game.word = 'apple'
    game.scrambled_word = 'pplea'

    # Assert that wrong guess returns False
    assert game.guess('appel') is False

    # assert number of attempts left decreases
    assert game.attempts == 4

    # Assert that correct guess returns True
    assert game.guess('apple') is True


def test_reset():
    game = WordScramble()
    game.reset('medium', 10)
    assert 5 <= len(game.word) <= 7
    assert game.attempts == 10

    # Assert that the game is reset
    game.reset('easy', 5)
    assert len(game.word) <= 4
    assert game.attempts == 5

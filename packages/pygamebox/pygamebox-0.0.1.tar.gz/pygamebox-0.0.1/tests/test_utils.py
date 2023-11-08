from pygamebox.utils import read_words_file, get_random_word


def test_get_random_word():
    word_list = ['apple', 'banana', 'orange']
    word = get_random_word(word_list)
    assert word in word_list


def test_read_words_file():
    words = read_words_file()

    # assert that there are words
    assert len(words) > 0

    # assert that all words are alphabetic
    assert all(word.isalpha() for word in words)

    # assert that there are words for each difficulty level
    assert any(len(word) <= 4 for word in words)
    assert any(5 <= len(word) <= 7 for word in words)
    assert any(len(word) >= 8 for word in words)

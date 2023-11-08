import pathlib
import random
from typing import Union

DATA_DIR = pathlib.Path(__file__).parent.absolute() / "data"


def read_file(file_path: Union[pathlib.Path, str]) -> list[str]:
    """
    Read a file and return a list of lines.

    :param file_path: Path to the file.
    :return: A list of lines.
    """
    file_path = pathlib.Path(DATA_DIR / file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip().lower() for line in file]


def read_words_file() -> list[str]:
    """
    Read the words file and return a list of all the words.

    :return: A list of all the words.
    """
    return read_file(DATA_DIR / 'words.txt')


def get_random_word(word_list: list[str]) -> str:
    """
    Get a random word from a list of words.

    :param word_list: A list of words.
    :return: A random word from the list.
    """
    return random.choice(word_list)

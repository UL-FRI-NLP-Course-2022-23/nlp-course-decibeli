import json
from enum import Enum

DATA_PATH = '../data/character_data_new.json'


def read_json(input_file):
    with open(input_file, 'r') as json_file:
        character_data = json.load(json_file)

    return character_data


class Book(Enum):
    FIRST = 'A Game of Thrones'
    SECOND = 'A Clash of Kings'
    THIRD = 'A Storm of Swords '
    FORTH = 'A Feast for Crows'
    FIFTH = 'A Dance with Dragons'


def get_characters_from_book(book_title, characters=None):
    """
    :param book_title: string value of the book
    :param characters: is a dictionary converted from json in data folder
    :return: new dictionary containing same structure of data as given but containing only data from a specific book
    """
    if characters is None:
        characters = read_json(DATA_PATH)
    characters_in_book = {}

    for character_name in characters.keys():
        is_in_book = False
        if 'Books' in characters[character_name]:
            if 'values' in characters[character_name]['Books']:
                is_in_book = any(
                    character_book.startswith(book_title)
                    for character_book in characters[character_name]['Books']['values'])
            else:
                is_in_book = any(
                    character_book.startswith(book_title) for character_book in characters[character_name]['Books'])
        elif 'Book' in characters[character_name]:
            if 'value' in characters[character_name]['Book']:
                is_in_book = characters[character_name]['Book']['value'].startswith(book_title)
            else:
                is_in_book = characters[character_name]['Book'][0].startswith(book_title)

        if is_in_book:
            characters_in_book[character_name] = characters[character_name].copy()

    return characters_in_book

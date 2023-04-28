from typing import List
import nltk
import json
from enum import Enum
import re
import csv

DATA_PATH = "data/character_data_new.json"
nltk.download("punkt")


class Book(Enum):
    A_GAME_OF_THRONES = {"title": "A Game of Thrones", "file_name": "got1.txt"}
    A_CLASH_OF_KINGS = {"title": "A Clash of Kings", "file_name": "got2.txt"}
    A_STORM_OF_SWORDS = {"title": "A Storm of Swords", "file_name": "got3.txt"}
    A_FEAST_FOR_CROWS = {"title": "A Feast for Crows", "file_name": "got4.txt"}
    A_DANCE_WITH_DRAGONS = {"title": "A Dance with Dragons", "file_name": "got5.txt"}


class RELATIONSHIP(Enum):
    FATHER = "father"
    MOTHER = "mother"
    SPOUSE = "spouse"


def read_json(input_file):
    with open(input_file, "r") as json_file:
        character_data = json.load(json_file)

    return character_data


def read_csv(input_file):
    with open(input_file, "r") as file:
        parsed_data = list(csv.reader(file, delimiter=";"))

    return parsed_data


def save_json(output_file, relations):
    with open(output_file, "w") as outfile:
        json.dump(relations, outfile, indent=4)


def read_book(book_file):
    lines = None
    with open(f"data/books/{book_file}", "r", encoding="utf-8") as f:
        lines = f.read()

    return lines


def save_processed_book(output_file, txt):
    with open(f"data/{output_file}", "w") as f:
        f.write(txt)


def save_triplets(output_file, triplets):
    with open(f"data/{output_file}", "w") as f:
        for triplet in triplets:
            subject, relation, object_ = triplet
            f.write(f"{subject};{relation};{object_}\n")


def get_text_between_words(text, word1, word2):
    regex = re.compile(rf"{word1}(.+?){word2}")
    match = regex.search(text)
    if match:
        return match.group(1)
    return None


def preprocess_book(book_txt: str, remove_chapter_title=False):
    # Get the text between the prologue and appendix
    book_txt = book_txt.split("PROLOGUE")[-1]
    book_txt = book_txt.split("APPENDIX")[0]

    # Remove multiple empty lines
    book_txt = re.sub(r"\n{2,}", "\n", book_txt)

    if remove_chapter_title:
        # Remove all words in all caps followed by a new line
        book_txt = re.sub(r"\b[A-Z]+\b\n", "", book_txt)

    # Replace smart double quotes with normal double quotes
    book_txt = re.sub(r"[“”]", '"', book_txt)
    # Replace smart single quotes with normal single quotes
    book_txt = re.sub(r"[‘’]", "'", book_txt)
    # Replace '—' with normal '-'
    book_txt = re.sub(r"—", "-", book_txt)
    # Remove all occurances of '. . .'
    book_txt = re.sub(r"\s*\. \. \.", "...", book_txt)

    return book_txt


def split_book_into_sentences(book_txt: str):
    sentences = nltk.sent_tokenize(book_txt)
    return sentences


def split_book_into_chapters(book_txt: str):
    return re.split(r"\b[A-Z]+\b\n", book_txt)


def split_text_by_length(text: str, n: int) -> list:
    # tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # initialize variables
    parts = []
    current_part = ""

    # iterate through the sentences
    for sentence in sentences:
        # if adding the sentence to the current part would exceed the length n, add the current part to the parts list and start a new part
        if len(current_part) + len(sentence) + 1 > n:
            parts.append(current_part.strip())
            current_part = ""

        # add the sentence to the current part
        current_part += sentence + " "

    # add the last part to the parts list
    parts.append(current_part.strip())

    return parts


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
        if "Books" in characters[character_name]:
            if "values" in characters[character_name]["Books"]:
                is_in_book = any(
                    character_book.startswith(book_title)
                    for character_book in characters[character_name]["Books"]["values"]
                )
            else:
                is_in_book = any(
                    character_book.startswith(book_title)
                    for character_book in characters[character_name]["Books"]
                )
        elif "Book" in characters[character_name]:
            if "value" in characters[character_name]["Book"]:
                is_in_book = characters[character_name]["Book"]["value"].startswith(
                    book_title
                )
            else:
                is_in_book = characters[character_name]["Book"][0].startswith(
                    book_title
                )

        if is_in_book:
            characters_in_book[character_name] = characters[character_name].copy()

    return characters_in_book


def get_character_aliases(character_name, characters=None):
    if characters is None:
        characters = read_json(DATA_PATH)

    character_aliases = []

    if "Aliases" in characters[character_name]:
        if "values" in characters[character_name]["Aliases"]:
            character_aliases = characters[character_name]["Aliases"]["values"]
        else:
            character_aliases = characters[character_name]["Aliases"]

    return character_aliases


def replace_character_aliases(character_name, aliases, text: str):
    for alias in aliases:
        text = re.sub(rf"\b{alias}\b", character_name, text)
    return text


def replace_all_aliases(text: str, characters=None):
    if characters is None:
        characters = read_json(DATA_PATH)

    for character_name in characters.keys():
        character_aliases = get_character_aliases(character_name, characters)
        text = replace_character_aliases(character_name, character_aliases, text)

    return text


def parse_gt_relationships():
    characters = read_json(DATA_PATH)
    chars_rels = {}

    for character in characters:
        char_key = character.lower()
        chars_rels[char_key] = {}

        if "Spouse" in characters[character]:
            chars_rels[char_key][RELATIONSHIP.SPOUSE] = parse_character_relationships(
                "Spouse", character, characters
            )

        if "Spouses" in characters[character]:
            chars_rels[char_key][RELATIONSHIP.SPOUSE] = parse_character_relationships(
                "Spouses", character, characters
            )

        if "Father" in characters[character]:
            chars_rels[char_key][RELATIONSHIP.FATHER] = parse_character_relationships(
                "Father", character, characters
            )

        if "Fathers" in characters[character]:
            chars_rels[char_key][RELATIONSHIP.FATHER] = parse_character_relationships(
                "Fathers", character, characters
            )

        if "Mother" in characters[character]:
            chars_rels[char_key][RELATIONSHIP.MOTHER] = parse_character_relationships(
                "Mother", character, characters
            )

        if "Mothers" in characters[character]:
            chars_rels[char_key][RELATIONSHIP.MOTHER] = parse_character_relationships(
                "Mothers", character, characters
            )

        # Filter unknowns:
        for relationship in chars_rels[char_key]:
            chars_rels[char_key][relationship] = list(
                filter(
                    lambda x: ("unknown" not in x and "Unknown" not in x),
                    chars_rels[char_key][relationship],
                )
            )

        # Convert to lower:
        for relationship in chars_rels[char_key]:
            chars_rels[char_key][relationship] = list(
                map(
                    lambda x: x.lower(),
                    chars_rels[char_key][relationship],
                )
            )

    return chars_rels


def parse_character_relationships(rel_str, character, characters):
    if type(characters[character][rel_str]) == list:
        return characters[character][rel_str]
    else:
        if "value" in list(characters[character][rel_str].keys()):
            return [characters[character][rel_str]["value"]]
        elif "values" in list(characters[character][rel_str].keys()):
            return characters[character][rel_str]["values"]


def parse_predicted_relationships():
    raw_csw = read_csv("data/family_triplets.csv")
    chars_rels = {}

    for row in raw_csw:
        char_key = row[0].lower()

        if "his" in char_key or "her" in char_key:
            continue

        chars_rels[char_key] = {}

        relationship_name = row[1].split(":")[1].lower()

        chars_rels[char_key][relationship_name] = row[2].lower()

    return chars_rels


def substring_in_array(s: str, arr: List[str]) -> bool:
    """Finds if string s is a substring of any of the strings in arr

    Args:
        s (str): string for which we need to check if it is contained as a substring in array
        arr (List[str]): list of strings that may contain string s as substring

    Returns:
        bool: True if s is a substring of any of the elements in arr
    """
    for check_str in arr:
        if s in check_str:
            return True

    return False

import re
import codecs
import sys

sys.path.append("./src")
from FRE.core_nlp import CoreNLPExtractor

from FRE.luke import LukeExtractor
from utils import (
    read_book,
    Book,
    get_characters_from_book,
    replace_all_aliases,
    save_processed_book,
    split_book_into_sentences,
    split_text_by_length,
    save_triplets,
    preprocess_book,
    split_book_into_chapters,
    read_coref_book,
)

# from coreference_resolution.neuralc import NeuralC

from tqdm import tqdm


def pipeline(book_file_name: str, coreference_filename: str = None):
    if coreference_filename == None:
        pass
        # # Coreference resolution has to be done before relationship extraction

        # # Load book txt
        # book_txt = read_book(book_file_name)

        # # Preprocessing of the book (removing the contents at the start, appendix at the end, etc.)
        # book_txt = preprocess_book(book_txt, remove_chapter_title=False)
        # # print(len(book_txt))

        # # Replace aliases with character names (could also be done after Correference resloution?) - probably should replace also with titles?
        # characters = get_characters_from_book(Book.A_GAME_OF_THRONES.value["title"])
        # book_txt = replace_all_aliases(book_txt, characters)
        # # print(len(book_txt))
        # save_processed_book(f"preprocessed_{book_file_name}", book_txt)

        # # Correference resolution
        # # parts = split_text_by_length(book_txt, 100_000)
        # parts = split_book_into_chapters(book_txt)
        # ncoref = NeuralC()
        # book_parts_processed = []
        # for part in tqdm(parts):
        #     book_part_txt = ncoref.coreference_res(part)
        #     book_parts_processed.extend(book_part_txt)
        # book_txt = "".join(book_parts_processed)
        # save_processed_book("corref.txt", book_txt)
    else:
        # Read the content of a file that includes coreferenece resolved book
        book_txt = read_coref_book(coreference_filename)

    # TODO: Named Entity Recognition (is it even needed if we use CoreNLP for relation extraction? - maybe for some improvements?)

    # Relation extraction between entities
    # book_txt = read_book('corref_got1_1.txt')
    sentences = split_book_into_sentences(book_txt)

    print(len(sentences))

    all_relations = []
    fre = LukeExtractor(
        "/home/anze/faks/nlp/nlp-course-decibeli/src/FRE/family_relations_words.csv"
    )
    for sentence in tqdm(sentences):
        triplets = fre.get_family_relations_triplets(sentence)
        all_relations.extend(triplets)
        # try:
        #     triplets = fre.get_family_relations_triplets(sentence)
        #     all_relations.extend(triplets)
        # except:
        #     print("Error occured!")

    # print(all_relations)
    save_triplets("family_triplets_luke.csv", all_relations)


if __name__ == "__main__":
    pipeline(f'{Book.A_GAME_OF_THRONES.value["file_name"]}', "corref_lg_z_narek.txt")

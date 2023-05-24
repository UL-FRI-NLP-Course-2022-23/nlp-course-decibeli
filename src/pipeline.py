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

from coreference_resolution.neuralc import NeuralC

from tqdm import tqdm


def pipeline(book, coreference_filename: str = None):
    if coreference_filename == None:
        # Coreference resolution has to be done before relationship extraction

        book_filename = book.value["file_name"]
        book_title = book.value["title"]
        # Load book txt
        book_txt = read_book(book_filename)

        # Preprocessing of the book (removing the contents at the start, appendix at the end, etc.)
        book_txt = preprocess_book(book_txt, remove_chapter_title=False, remove_dialog=True)
        # print(len(book_txt))

        # Replace aliases with character names (could also be done after Correference resloution?) - probably should replace also with titles?
        characters = get_characters_from_book(book_title)
        book_txt = replace_all_aliases(book_txt, characters)
        # print(len(book_txt))
        save_processed_book(f"preprocessed_{book_filename}", book_txt)
        
        # Correference resolution
        # parts = split_text_by_length(book_txt, 100_000)
        parts = split_book_into_chapters(book_txt)
        ncoref = NeuralC()
        book_parts_processed = []
        for part in tqdm(parts):
            book_part_txt = ncoref.coreference_res(part)
            book_parts_processed.append(book_part_txt)

        book_txt = "CHAPTER\n".join(book_parts_processed)
        save_processed_book(f"corref_{book_filename}", book_txt)
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
        "/mnt/d/Faks/Magisterij/NATURAL LANGUAGE PROCESSING/nlp-course-decibeli/src/FRE/family_relations_words.csv"
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
    save_triplets(f"triplets/family_triplets_luke_{book_filename[:-4]}.csv", all_relations)


if __name__ == "__main__":
    pipeline(Book.A_CLASH_OF_KINGS)

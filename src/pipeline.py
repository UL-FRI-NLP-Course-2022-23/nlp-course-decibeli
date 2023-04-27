from utils import read_book, Book, get_characters_from_book, replace_all_aliases, save_processed_book, split_book_into_sentences, split_text_by_length, save_triplets
from coreference_resolution.neuralc import NeuralC
from FRE.coreNLP import FamilyRelationExtractor

from tqdm import tqdm


def pipeline(book_file_name: str):
    # Load book txt
    book_txt = read_book(book_file_name)
    book_txt = book_txt.replace('\n\n', '\n')
    save_processed_book('corref_got1.txt', book_txt)

    print(len(book_txt))
    # TODO: Preprocessing of the book (removing the contents at the start etc.)
    # Replace aliases with character names (could also be done after Correference resloution?) - probably should replace also with titles?
    characters = get_characters_from_book(
        Book.A_GAME_OF_THRONES.value["title"])
    book_txt = replace_all_aliases(book_txt, characters)
    print(len(book_txt))

    # Correference resolution
    parts = split_text_by_length(book_txt, 100_000)
    ncoref = NeuralC()
    book_parts_processed = []
    for part in tqdm(parts):
        book_part_txt = ncoref.coreference_res(part)
        book_parts_processed.extend(book_part_txt)
    book_txt = ''.join(book_parts_processed)
    save_processed_book('corref_got1.txt', book_txt)
    # TODO: Named Entity Recognition (is it even needed if we use CoreNLP for relation extraction? - maybe for some improvements?)

    # Relation extraction between entities
    # book_txt = read_book('corref_got1.txt')
    sentences = split_book_into_sentences(book_txt)

    all_relations = []
    for sentence in tqdm(sentences):
        try:
            fre = FamilyRelationExtractor()
            triplets = fre.get_family_relations_triplets(sentence)
            all_relations.extend(triplets)
        except:
            print('Error occured!')

    # print(all_relations)
    save_triplets('triplets.txt', all_relations)


if __name__ == '__main__':
    pipeline(f'{Book.A_GAME_OF_THRONES.value["file_name"]}')

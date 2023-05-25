import sys


sys.path.append("./src")
from NER.ner_spacy import Ner_Spacy
from NER.ner_stanza import Ner_Stanza
from NER.ner_nltk import Ner_Nltk
from transformers import AutoTokenizer, LukeForEntityPairClassification
from FRE.family_rel_extractor import FamilyRelationExtractor
import re


class LukeExtractor(FamilyRelationExtractor):
    def get_family_relations_triplets(self, text, annotations=None):
        if not self.includes_relationship(text):
            return []

        entities = self.ner_entities(text)

        if len(entities) < 2:
            return []

        if len(entities) > 2:
            entities = self.best_entites(entities, text)

        # if len(best_entities) < 2:
        #     return []
        # else:
        #     entities = best_entities

        # print(text)
        # print(entities)

        entity_spans = self.word_indexes(entities, text)
        inputs = self.tokenizer(text, entity_spans=entity_spans, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        predicted_class = self.model.config.id2label[predicted_class_idx]

        if predicted_class in self.family_relations:
            triplet = entities[0], predicted_class, entities[1]
            return [triplet]
        else:
            return []

    def includes_relationship(self, sentence: str):
        pattern = (
            r"\b(" + "|".join(map(re.escape, self.relationship_stop_words)) + r")\b"
        )
        return re.compile(pattern, re.IGNORECASE).search(sentence)

    def best_entites(self, entities, sentence):
        pattern = (
            r"\b(" + "|".join(map(re.escape, self.relationship_stop_words)) + r")\b"
        )
        matches = re.finditer(pattern, sentence, flags=re.IGNORECASE)
        positions_stopwords = []
        for match in matches:
            position = match.start()
            positions_stopwords.append(position)

        # if len(positions_stopwords) < 1:
        #     return []

        positions_entities = self.word_indexes(entities, sentence)
        pos_stopword = positions_stopwords[0]

        positions_entities = [
            (entities[i], positions_entities[i]) for i in range(len(positions_entities))
        ]

        entities_lengths = []

        for entity, (start, end) in positions_entities:
            if end < pos_stopword:
                entities_lengths.append((entity, pos_stopword - end))
            if start > pos_stopword:
                entities_lengths.append((entity, start - pos_stopword))

        entities_lengths.sort(key=lambda x: x[1])
        return [entities_lengths[0][0], entities_lengths[1][0]]

    def ner_entities(self, sentence: str):
        entities_dict = self.ner.predict(sentence)
        entities = []

        if len(entities_dict) > 1:
            entities = [entity for entity in entities_dict.keys()]

        return entities

    def word_indexes(self, words, text):
        ixs = []
        for word in words:
            start = text.find(word)
            if start < 0:
                raise Exception(f'Word "{word}" not found in "{text}"')
            else:
                ixs.append((start, start + len(word)))

        return ixs

    def __init__(self, relationship_words_filename: str, ner="nltk"):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(
            "studio-ousia/luke-large-finetuned-tacred"
        )
        self.model = LukeForEntityPairClassification.from_pretrained(
            "studio-ousia/luke-large-finetuned-tacred"
        )

        if ner == "spacy":
            self.ner = Ner_Spacy()
        elif ner == "stanza":
            self.ner = Ner_Stanza()
        elif ner == "nltk":
            self.ner = Ner_Nltk()
        else:
            raise Exception(f'Named Entity Recognizer "{ner}" not implemented')

        with open(relationship_words_filename) as fp:
            self.relationship_stop_words = [line.rstrip()[:-1] for line in fp]
        # self.relationship_stop_words = [
        #     "father",
        #     "mother" "spouse",
        #     "husband",
        #     "son",
        #     "daughter" "wife",
        #     "child",
        #     "brother",
        #     "sister",
        #     "sibling",
        # ]


# # text = "John Snow is the son of Aegon Targaryen."
# # fre = LukeExtractor()
# # print(fre.get_family_relations_triplets(text, ["John Snow", "Aegon Targaryen"]))
# with open("./src/FRE/family_relations_words.csv") as fp:
#     a = [line.rstrip()[:-1] for line in fp]

# print(a)

import sys


sys.path.append("./src")
from NER.ner_spacy import Ner_Spacy
from transformers import AutoTokenizer, LukeForEntityPairClassification
from FRE.family_rel_extractor import FamilyRelationExtractor
import re


class LukeExtractor(FamilyRelationExtractor):
    def get_family_relations_triplets(self, text, annotations=None):
        if not self.includes_relationship(text):
            return []

        entities = self.ner_entities(text)
        if len(entities) != 2:
            return []

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
        return re.compile("|".join(self.relationship_stop_words), re.IGNORECASE).search(
            sentence
        )

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

    def __init__(self):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(
            "studio-ousia/luke-large-finetuned-tacred"
        )
        self.model = LukeForEntityPairClassification.from_pretrained(
            "studio-ousia/luke-large-finetuned-tacred"
        )
        self.ner = Ner_Spacy()
        self.relationship_stop_words = [
            "father",
            "mother" "spouse",
            "husband",
            "son",
            "daughter" "wife",
            "child",
            "brother",
            "sister",
            "sibling",
        ]


# text = "John Snow is the son of Aegon Targaryen."
# fre = LukeExtractor()
# print(fre.get_family_relations_triplets(text, ["John Snow", "Aegon Targaryen"]))

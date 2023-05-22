from transformers import AutoTokenizer, LukeForEntityPairClassification
from family_rel_extractor import FamilyRelationExtractor


class LukeExtractor(FamilyRelationExtractor):
    def __init__(self):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(
            "studio-ousia/luke-large-finetuned-tacred"
        )
        self.model = LukeForEntityPairClassification.from_pretrained(
            "studio-ousia/luke-large-finetuned-tacred"
        )

    def get_family_relations_triplets(self, text, entities=None, annotations=None):
        if entities is None:
            raise Exception("Entities must be provided for LUKE.")

        entity_spans = self.word_indexes(entities, text)

        inputs = self.tokenizer(text, entity_spans=entity_spans, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        predicted_class = self.model.config.id2label[predicted_class_idx]

        if self.family_relations in predicted_class:
            return f"{entities[0]};{predicted_class};{entities[1]}"
        else:
            return ""

    def word_indexes(self, words, text):
        ixs = []
        for word in words:
            start = text.find(word)
            if start < 0:
                raise Exception(f'Word "{word}" not found in "{text}"')
            else:
                ixs.append((start, start + len(word)))

        return ixs


# text = "John Snow is the son of Aegon Targaryen."
# fre = LukeRelationExtractor()
# print(fre.get_family_relations_triplets(text, ["John Snow", "Aegon Targaryen"]))

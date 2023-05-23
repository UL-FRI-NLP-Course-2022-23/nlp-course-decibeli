from abc import ABC, abstractmethod


class FamilyRelationExtractor(ABC):
    def __init__(self):
        self.family_relations = [
            "per:children",
            "per:parents",
            "per:siblings",
            "per:spouse",
        ]

    @abstractmethod
    def get_family_relations_triplets(self, text, annotations):
        pass

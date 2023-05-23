import json
import requests

from FRE.family_rel_extractor import FamilyRelationExtractor


class CoreNLPExtractor(FamilyRelationExtractor):
    # TODO: add some arguments for different annotators
    def __init__(
        self,
        server_url='http://172.28.0.1:9000/?properties={"annotators":"tokenize,ssplit,kbp","outputFormat":"json"}',
    ) -> None:
        super().__init__()
        self.server_url = server_url
        self.headers = {"Content-type": "text/plain; charset=utf-8"}

    def get_family_relations_triplets(self, text, annotations=None):
        if annotations is None:
            annotations = requests.post(self.server_url, data=text).json()

        triplets = []
        for sentence in annotations["sentences"]:
            kbp = sentence["kbp"]
            for relation_info in kbp:
                subject = relation_info["subject"]
                relation = relation_info["relation"]
                object = relation_info["object"]

                if relation in self.family_relations:
                    triplet = subject, relation, object
                    triplets.extend([triplet])

        return triplets

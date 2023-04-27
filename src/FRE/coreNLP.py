import json
import requests


class FamilyRelationExtractor:

    # TODO: add some arguments for different annotators
    def __init__(self, server_url='http://172.28.0.1:9000/?properties={"annotators":"tokenize,ssplit,kbp","outputFormat":"json"}') -> None:
        self.server_url = server_url
        self.headers = {'Content-type': 'text/plain; charset=utf-8'}

        self.family_realtions = ['per:children',
                                 'per:parents', 'per:siblings', 'per:spouse']

    def get_relations(self, text):
        annotations = requests.post(self.server_url,
                                    data=text.encode('utf-8'),
                                    headers=self.headers).json()
        relations = {}

        for sentence in annotations['sentences']:
            kbp = sentence['kbp']
            for relation in kbp:
                if relation['subject'] not in relations.keys:
                    relations[relation['subject']] = []

                relations[relation['subject']].extend(relation)

        return relations

    def get_relations_triplets(self, text, annotations=None):

        if annotations is None:
            annotations = requests.post(self.server_url, data=text).json()

        triplets = []
        for sentence in annotations['sentences']:
            kbp = sentence['kbp']
            for relation_info in kbp:
                subject = relation_info['subject']
                relation = relation_info['relation']
                object = relation_info['object']
                triplet = subject, relation, object
                triplets.extend([triplet])

        return triplets

    def get_family_relations_triplets(self, text, annotations=None):

        if annotations is None:
            annotations = requests.post(self.server_url, data=text).json()

        triplets = []
        for sentence in annotations['sentences']:
            kbp = sentence['kbp']
            for relation_info in kbp:
                subject = relation_info['subject']
                relation = relation_info['relation']
                object = relation_info['object']

                if relation in self.family_realtions:
                    triplet = subject, relation, object
                    triplets.extend([triplet])

        return triplets


# text = "John Snow is the son of Aegon Targaryen. Lord Stark has son Robert."
# fre = FamilyRelationExtractor()
# print(fre.get_family_relations(text))
# # print(fre.get_family_relations_triplets(text))

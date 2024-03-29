# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from nltk.tokenize import sent_tokenize
from collections import defaultdict
import re

class Ner_Spacy:
    def __init__(self):
        self.nlp = en_core_web_sm.load()

    def predict(self, text):
        """
        Function executes NER on input text and returns a dictionary of found characters with a number of occurences
        
        Parameters:
            text (str): Input text
        Returns:
            defaultdict: Dictionary of found characters with a number of occurences
        """

        sentences = sent_tokenize(text)
        names_dict = defaultdict(lambda: 0)

        for s in sentences:
            sentence = self.nlp(s)
            for entity in sentence.ents:
                if entity.label_ == 'PERSON':
                    names_dict[entity.text] += 1
                    
        return names_dict
    
    def replace_ners(self, text, replace_str):
        """
        Function replaces each Named Entity found in text with given replace_str and returns whole text with replaced NE
        """
        sentences = sent_tokenize(text)
        for s in sentences:
            sentence = self.nlp(s)
            for entity in sentence.ents:
                if entity.label_ == "PERSON":
                    text = re.sub(rf"\b{entity.text}\b", replace_str, text)

        return text

# text = 'john is talking to me. luka is talking to him. Jon is tall. The King Of The North is here. This is John Cena.'
# ner = Ner_Spacy()
# ner.predict(text)
# print(ner.replace_ners(text, "P"))
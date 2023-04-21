# pip install stanza
from nltk.tokenize import sent_tokenize
from collections import defaultdict
import stanza
stanza.download('en')

class Ner_Stanza:
    def __init__(self):
        self.nlp = stanza.Pipeline('en', processors='tokenize,ner')

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

        for sentence in sentences:
            doc = self.nlp(sentence)
            # print(doc.sentences)
            for sent in doc.sentences:
                for ent in sent.ents:
                    if ent.type == 'PERSON':
                        print(ent.text, ent.type)
                        names_dict[ent.text] += 1
                    
        return names_dict

# text = 'Jon is talking to cersei. Cersei is talking to eddard.'
# ner = Ner_Stanza()
# ner.predict(text)
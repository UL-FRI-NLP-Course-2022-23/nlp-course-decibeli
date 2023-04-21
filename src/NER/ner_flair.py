from flair.data import Sentence
from flair.nn import Classifier
from flair.models import SequenceTagger
from collections import defaultdict
from flair.splitter import SegtokSentenceSplitter
from nltk.tokenize import sent_tokenize

class Ner_Flair:
    def __init__(self):
        self.tagger = SequenceTagger.load('ner') # ner-large

    def predict(self, text):
        """
        Function executes NER on input text and returns a dictionary of found characters with a number of occurences

        Parameters:
            text (str): Input text
        Returns:
            defaultdict: Dictionary of found characters with a number of occurences
        """
        
        # Split text into sentences
        sentences = sent_tokenize(text)
        names_dict = defaultdict(lambda: 0)
        
        for s in sentences:
            sentence = Sentence(s)
            self.tagger.predict(sentence)
            for entity in sentence.get_spans('ner'):
                # print(entity)
                if entity.tag == 'PER':
                    name = entity.text
                    names_dict[name] += 1

        # for key in names_dict.keys():
        #     print(key + ': ' + str(names_dict[key]))

# text = 'Jon is talking to cersei. Cersei is talking to eddard.'
# ner = Ner_Flair()
# ner.predict(text)
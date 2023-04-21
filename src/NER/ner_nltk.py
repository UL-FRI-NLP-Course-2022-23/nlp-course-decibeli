from nltk.tokenize import sent_tokenize
from collections import defaultdict
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

class Ner_Nltk:
    def __init__(self):
        pass

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
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))):
                if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                    name = ' '.join(c[0] for c in chunk)
                    # print(chunk.label(), name)
                    names_dict[name] += 1
                    
        return names_dict

# text = 'john is talking to me. luka is talking to him. Jon is tall. The King Of The North is here. This is John Cena.'
# ner = Ner_Nltk()
# ner.predict(text)
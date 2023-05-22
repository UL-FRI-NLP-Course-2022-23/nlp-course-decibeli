# conda create --name onj-projekt -c anaconda python=3.7
# conda activate onj-projekt
# pip install spacy==2.1.0
# pip install neuralcoref
# python -m spacy download en

import spacy
import neuralcoref

class NeuralC:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        neuralcoref.add_to_pipe(self.nlp)

    def coreference_res(self, text):
        """
        Function executes coreference resolution on input text and returns modified text

        Parameters:
            text (str): Input text
        Returns:
            str: Result of coreference resolution
        """
        
        doc = self.nlp(text) 

        # print(doc._.coref_clusters)
        # print(doc._.coref_resolved)
        return doc._.coref_resolved

# text = "Joseph Robinette Biden Jr. is an American politician who is the 46th and\
#     current president of the United States. A member of the Democratic Party, \
#     he served as the 47th vice president from 2009 to 2017 under Barack Obama and\
#     represented Delaware in the United States Senate from 1973 to 2009."
# coref = NeuralC()
# coref.coreference_res(text)
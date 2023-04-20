# conda create --name onj-projekt -c anaconda python=3.7
# conda activate onj-projekt
# pip install spacy==2.1.0
# pip install neuralcoref
# python -m spacy download en

import spacy
import neuralcoref

def coreference_res(text):
    nlp = spacy.load('en_core_web_sm')  # load the model
    neuralcoref.add_to_pipe(nlp)

    doc = nlp(text)  # get the spaCy Doc (composed of Tokens)

    print(doc._.coref_clusters)  # You can see cluster of similar mentions
    print(doc._.coref_resolved)
    return doc._.coref_resolved

# text = "Joseph Robinette Biden Jr. is an American politician who is the 46th and\
#     current president of the United States. A member of the Democratic Party, \
#     he served as the 47th vice president from 2009 to 2017 under Barack Obama and\
#     represented Delaware in the United States Senate from 1973 to 2009."
# coreference_res(text)
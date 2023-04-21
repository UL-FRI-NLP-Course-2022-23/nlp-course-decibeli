# https://docs.allennlp.org/main/#installing-via-pip
# pip install allennlp==2.9.3
# pip install allennlp-models==2.9.3
# pip install cached-path==1.1.2

from allennlp.predictors.predictor import Predictor

class Allen:
    def __init__(self):
        model_url = "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2020.02.27.tar.gz"
        self.predictor = Predictor.from_path(model_url)

    def coreference_res(self, text):
        """
        Function executes coreference resolution on input text and returns modified text

        Parameters:
            text (str): Input text
        Returns:
            str: Result of coreference resolution
        """

        prediction = self.predictor.predict(document=text)
        # print("Clsuters:-")
        # for cluster in prediction['clusters']:
        #     print(cluster) 
        # print('\n\n')
        # print('Coref resolved: ', self.predictor.coref_resolved(text)) 
        return self.predictor.coref_resolved(text)

# text = "Joseph Robinette Biden Jr. is an American politician who is the 46th and\
#     current president of the United States. A member of the Democratic Party, \
#     he served as the 47th vice president from 2009 to 2017 under Barack Obama and\
#     represented Delaware in the United States Senate from 1973 to 2009."
# coref = Allen()
# coref.coreference_res(text)
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tag import untag, str2tuple, tuple2str
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import string

class Preprocessor:
    def __init__(self, text_filename):
        self.text_filename = text_filename

    def do_preprocessing(self):
        tokens = self.get_tokens()
        tokens = self.remove_stopwords(tokens)
        tokens = self.pos_tagging(tokens)
        tokens = self.lemmatization(tokens)

        return tokens
    

    def get_tokens(self):
        with open(self.text_filename, 'r') as shakes:
            text = shakes.read().lower()
            # remove punctuation
            table = text.maketrans({key: None for key in string.punctuation})
            text = text.translate(table)      
            tokens = word_tokenize(text)
            return tokens
        
    def remove_stopwords(self, tokens):
        stop_w = stopwords.words('english')
        return list(filter(lambda x: x not in stop_w, tokens))
    
    def pos_tagging(self, tokens):
        return pos_tag(tokens)
    
    def lemmatization(self, pos_tagged_tokens):
        from nltk.stem import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        lemmas = [lemmatizer.lemmatize(token, self.get_wordnet_pos(pos)) for (token, pos) in pos_tagged_tokens]
        return lemmas

    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            #Default (noun), or dont preform lemmatization?
            return wordnet.NOUN


def main():
    
    p = Preprocessor('./data/001ssb.txt')

    print(p.do_preprocessing()[:50])

if __name__ == "__main__":
    main()
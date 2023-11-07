import pandas as pd
import re
from unidecode import unidecode
import treetaggerwrapper
import importlib.resources as resources


class NLP:
    def __init__(self):
        resource_path_fr = "packagenlp/data/stopWords_spacy_fr.csv"
        resource_path_en = "packagenlp/data/stopWords_spacy_en.csv"

        # Accédez aux fichiers de stopwords dans les sous-dossiers.
        with resources.open_text('packagenlp', resource_path_fr) as file:
            self.stopwords_fr = pd.read_csv(file, sep=';', encoding='utf-8')['word'].tolist()
        with resources.open_text('packagenlp', resource_path_en) as file:
            self.stopwords_en = pd.read_csv(file, sep=';', encoding='utf-8')['word'].tolist()

    def cleanStopWord(self, text, langue = '', add_stopwords=[], remove_stopwords=[]):
        if langue == 'fr' :             
            stopwords = [
                word for word in self.stopwords_fr if word not in remove_stopwords]
        elif langue == 'en' : 
            stopwords = [
                word for word in self.stopwords_en if word not in remove_stopwords]
        else : 
            raise ValueError("Invalid langue for text.")
        stopwords.extend(add_stopwords)
        tokens = text.split(' ')
        return ' '.join([token for token in tokens if token.lower() not in stopwords])

    def cleanText(self, text, keep_numbers=True, exception='', remove_accent=True, lowercase=True):

        if remove_accent:
            text = unidecode(text)

        if lowercase:
            text = text.lower()

        if keep_numbers and exception:
            pattern = re.compile('[^A-Za-z0-9\xe0-\xff '+exception+']')
        elif keep_numbers:
            pattern = re.compile('[^A-Za-z0-9\xe0-\xff]')
        elif exception:
            pattern = re.compile('[^A-Za-z\xe0-\xff '+exception+']')
        else:
            pattern = re.compile('[^A-Za-z\xe0-\xff]')

        cleaned_text = pattern.sub(' ', text)

        cleaned_text = cleaned_text.strip()

        return cleaned_text


    def lemmatisation(self, text, lemma_exclu, langue='', keep_numbers=True, keep_type_word=[]):
        if langue == 'fr':
            tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR='C:\TreeTagger\TreeTagger')
        elif langue == 'en':
            tagger = treetaggerwrapper.TreeTagger(TAGLANG='en', TAGDIR='C:\TreeTagger\TreeTagger')
        else:
            raise ValueError("Invalid language for text.")
    
        tokenisation_majuscule = list()
        majuscule_tokenised = ''
        tags = tagger.tag_text(str(text), nosgmlsplit=True)
        for tag in tags:
            word, mottag, lemma = tag.split()
            if len(lemma.split('|')) > 1:
                lemma = lemma.split('|')[0]
            if word in lemma_exclu.keys():
                lemma = lemma_exclu[word]
            if keep_numbers:
                if mottag == 'NUM':
                    lemma = word
            pos = mottag.split(':')[0]
            if keep_type_word == []:
                majuscule_tokenised = majuscule_tokenised + ' ' + lemma
            else:
                if pos in keep_type_word:
                    majuscule_tokenised = majuscule_tokenised + ' ' + lemma

        tokenisation_majuscule.append(majuscule_tokenised)

        lemmatized_text = ' '.join(tokenisation_majuscule)
        return lemmatized_text.strip()  





import re
import string

import spacy
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
from unidecode import unidecode


class TextPreprocessor:
    # Pré-compilar expressões regulares e definir variáveis globais
    RE_PUNCTUATION = re.compile(rf"[{string.punctuation}]")
    RE_DIGITS = re.compile(r"\d+")
    STOP_WORDS = set(stopwords.words("portuguese"))

    def __init__(self):
        # Carregar modelo de língua portuguesa do spaCy
        self.nlp = spacy.load("pt_core_news_sm")

    @staticmethod
    def remove_consecutive_duplicates(tokens):
        # Retorna uma nova lista que contém todos os tokens, removendo elementos consecutivos duplicados.
        return [t for i, t in enumerate(tokens) if i == 0 or t != tokens[i - 1]]

    def preprocess_text(self, text, remove_accents=True, use_lemmatization=True, use_stemming=False):
        # Converter texto para minúsculas
        text = text.lower()

        # Remover pontuações e números usando expressões regulares pré-compiladas
        text = self.RE_PUNCTUATION.sub(" ", text)
        text = self.RE_DIGITS.sub("", text)

        # Tokenização
        tokens = word_tokenize(text)

        # Remover stopwords usando compreensão de lista e conjunto de stopwords
        filtered_tokens = [word for word in tokens if word not in self.STOP_WORDS]

        # Lematização
        if use_lemmatization and not use_stemming:
            lemmatized_text = " ".join(filtered_tokens)
            doc = self.nlp(lemmatized_text)
            filtered_tokens = [token.lemma_ for token in doc]

        # Stemming
        if use_stemming and not use_lemmatization:
            stemmer = RSLPStemmer()
            filtered_tokens = [stemmer.stem(word) for word in filtered_tokens]

        # Remover acentos
        if remove_accents:
            filtered_tokens = [unidecode(word) for word in filtered_tokens]

        # Remover palavras duplicadas consecutivas
        # (Não usar quando for fazer n-gram ou medir sequência de palavras)
        filtered_tokens = self.remove_consecutive_duplicates(filtered_tokens)

        # Junte as palavras de volta em uma string
        preprocessed_text = " ".join(filtered_tokens)

        return preprocessed_text

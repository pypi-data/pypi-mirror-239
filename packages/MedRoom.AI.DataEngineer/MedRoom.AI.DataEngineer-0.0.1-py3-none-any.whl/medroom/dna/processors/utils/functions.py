import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
import re
import string
from unidecode import unidecode

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn import preprocessing

class TextPreprocessor:
    # Pré-compilar expressões regulares e definir variáveis globais
    RE_PUNCTUATION = re.compile(rf'[{string.punctuation}]')
    RE_DIGITS = re.compile(r'\d+')
    STOP_WORDS = set(stopwords.words('portuguese'))
    
    def __init__(self):
        # Carregar modelo de língua portuguesa do spaCy
        self.nlp = spacy.load('pt_core_news_sm')
    
    @staticmethod
    def remove_consecutive_duplicates(tokens):
        # Retorna uma nova lista que contém todos os tokens, removendo elementos consecutivos duplicados.
        return [t for i, t in enumerate(tokens) if i == 0 or t != tokens[i-1]]
    
    def preprocess_text(self, text, remove_accents=True, use_lemmatization=True, use_stemming=False):
        # Converter texto para minúsculas
        text = text.lower()

        # Remover pontuações e números usando expressões regulares pré-compiladas
        text = self.RE_PUNCTUATION.sub(' ', text)
        text = self.RE_DIGITS.sub('', text)

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
        preprocessed_text = ' '.join(filtered_tokens)

        return preprocessed_text


class ModelEvaluator:
    @staticmethod
    def accuracy(y_true, y_pred):
        acc = accuracy_score(y_true, y_pred)
        print("Acurácia do modelo = %2.f%%" % (acc * 100.00))
    
    @staticmethod
    def classification_report(y_true, y_pred):
        report_df = pd.DataFrame(
            classification_report(y_true, y_pred, output_dict=True)
        ).T
        report_df = report_df.drop(columns=['support'])
        plt.subplots(figsize=(4, 3))
        sns.heatmap(report_df, cmap='Greens', linewidths=0.5, annot=True)
        plt.title('Classification Report')
        plt.show()
    
    @staticmethod
    def confusion_matrix(y_true, y_pred):
        # Criando a matriz de confusão
        report_df = pd.DataFrame(
            classification_report(y_true, y_pred, output_dict=True)
        ).T
        report_df = report_df.drop(columns=['support'])

        cnf_report_df = report_df.index[:-3]
        cnf_matrix = confusion_matrix(y_true, y_pred)
        cnf_matrix = pd.DataFrame(
            cnf_matrix, index=cnf_report_df.values, columns=cnf_report_df.values
        )
        cnf_matrix = cnf_matrix / cnf_matrix.sum(axis=1)[:, np.newaxis]  # Normalização em linha (recall)

        # Plotagem da matriz de confusão
        sns.heatmap(
            cnf_matrix,
            cmap='Greens',
            linecolor='white',
            linewidths=0.5,
            annot=True,
            fmt='.0%',
            cbar=False,
            square=True,
        )
        plt.title('Confusion Matrix')
        plt.show()
    
    @staticmethod
    def roc_auc(y_true, y_pred):
        # Converter rótulos para formato binário
        lb = preprocessing.LabelBinarizer()
        lb.fit(y_true)

        y_test = lb.transform(y_true)
        y_pred = lb.transform(y_pred)

        # Calcular a área sob a curva (AUC-ROC)
        auc_roc = roc_auc_score(y_test, y_pred, average='weighted', multi_class='ovr')
        print("ROC_AUC do modelo = %2.f%%" % (auc_roc * 100.00))
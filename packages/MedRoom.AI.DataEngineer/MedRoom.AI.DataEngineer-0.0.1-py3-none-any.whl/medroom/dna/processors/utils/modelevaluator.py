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
        cnf_matrix = cnf_matrix / cnf_matrix.sum(axis=1).values[:, np.newaxis]  # Normalização em linha (recall)

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
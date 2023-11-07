# MedRoom.AI.DataEngineer

O `MedRoom.AI.DataEngineer` é um pacote que encapsula funções comuns e genéricas, proporcionando uma solução padronizada para o pré-processamento de texto e avaliação de modelos de Machine Learning.

## :arrow_down: Instalação

### 1. Baixar o Pacote
Faça o download do pacote [aqui](https://drive.google.com/file/d/1tX5D9IxFW6y8kLxR2hRxHgp3nq0J8eT2/view?usp=sharing).

### 2. Instalar o Pacote
```bash
!pip install /path_to_your_downloaded_file/MedRoom.AI.DataEngineer-0.0.1-py3-none-any.whl
```
**Nota:** Substitua `/path_to_your_downloaded_file/` pelo caminho onde o arquivo `.whl` foi baixado.

## :book: Uso 

### :one: Pré-processamento de Texto 

#### Importar Bibliotecas Necessárias
```python
import nltk
import spacy

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')
spacy.cli.download("pt_core_news_sm")
```

#### Utilizando o Pré-processador de Texto
```python
from medroom.dna.processors.utils.textclean import TextPreprocessor

preprocessor = TextPreprocessor()
text = "Exemplo de não texto para preprocessamento classificação ando!"
processed_text = preprocessor.preprocess_text(text, use_lemmatization=True, use_stemming=False)

print(processed_text)
```

### :two: Avaliação de Modelos de Machine Learning

#### Importar e Usar a Classe de Avaliação
```python
from medroom.dna.processors.utils.evalmetrics import ModelEvaluator

# Suponha que `predictions` e `y_test` são suas predições e rótulos reais, respectivamente.
evalmetrics = ModelEvaluator()
```

#### Métricas de Avaliação Disponíveis

- **Acurácia**
  ```python
  evalmetrics.accuracy(y_test, predictions)
  ```
  
- **Relatório de Classificação**
  ```python
  evalmetrics.classification_report(y_test, predictions)
  ```
  
- **ROC-AUC**
  ```python
  evalmetrics.roc_auc(y_test, predictions)
  ```
  
- **Matriz de Confusão**
  ```python
  evalmetrics.confusion_matrix(y_test, predictions)
  ```
  
## :notebook: Tutorial Interativo

Para um aprendizado mais prático e interativo, oferecemos um tutorial em formato de Jupyter Notebook. Ele guia você através do uso prático das classes e funções disponíveis no `MedRoom.AI.DataEngineer`, abrangendo desde o pré-processamento de texto até a avaliação do modelo.

- [Acesse o Tutorial Interativo](https://github.com/MedRoomGitHub/MedRoom.AI.Notebooks/blob/develop/Tutoriais/Sprint11_MedRoomAIDataEngineer.ipynb)

Baixe o notebook e execute-o localmente, ou explore-o diretamente no GitHub para uma compreensão aprofundada das funcionalidades disponíveis no pacote `MedRoom.AI.DataEngineer`.

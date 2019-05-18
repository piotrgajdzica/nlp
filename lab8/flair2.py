import flair
import torch
from flair.data_fetcher import NLPTaskDataFetcher
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentLSTMEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from pathlib import Path

if __name__ == '__main__':
    # flair.device = torch.device('cpu')
    for dir in ['ten']:
        print(dir)
        corpus = NLPTaskDataFetcher.load_classification_corpus(Path('./'), test_file='validation/%s/labeled.txt' % dir, dev_file='testing/max_50/labeled.txt', train_file='training/max_50/labeled.txt')
        word_embeddings = [WordEmbeddings('glove'), FlairEmbeddings('news-forward-fast'), FlairEmbeddings('news-backward-fast', chars_per_chunk=64)]
        document_embeddings = DocumentLSTMEmbeddings(word_embeddings, hidden_size=256, reproject_words=True, reproject_words_dimension=256)
        classifier = TextClassifier(document_embeddings, label_dictionary=corpus.make_label_dictionary(), multi_label=False)
        trainer = ModelTrainer(classifier, corpus)
        trainer.train('./', max_epochs=10)

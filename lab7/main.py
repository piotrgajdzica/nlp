import time

import gensim.downloader as api
from gensim.models import KeyedVectors
from gensim.test.utils import datapath


def task1():

    start = time.time()
    word_vectors = KeyedVectors.load_word2vec_format(datapath('C:/Users/piotrek/Desktop/inf/nlp/lab1/repository/lab7/corpus'), binary=False)  # load pre-trained word-vectors from gensim-data

    middle = time.time()
    print(middle - start)
    words = [
        ['sąd::noun', 'wysoki::noun'], ['trybunał konstytucyjny'], ['kodeks cywilny'], ['kpk'], ['sąd rejonowy'],
        ['szkoda'], ['wypadek'], ['kolizja'], ['szkoda majątkowy'], ['nieszczęście'], ['rozwód']]

    for word in words:
        result = word_vectors.most_similar(positive=[word])
        for i in range(5):
            print("{}: {:.4f}".format(*result[i]))

    print(time.time() - middle)

if __name__ == '__main__':

    task1()

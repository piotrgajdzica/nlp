import json
from math import log

if __name__ == '__main__':
    unigrams = json.loads(open('../data/unigrams.json', encoding='utf-8').read())
    bigrams = json.loads(open('../data/bigrams.json', encoding='utf-8').read())

    bigram_normalizer = sum(bigrams.values())
    unigram_normalizer = sum(unigrams.values())
    bigram_pmi = {}

    for bigram in bigrams.keys():
        first_word, second_word = bigram.split()
        pmi = log(bigrams[bigram] / bigram_normalizer / (unigrams[first_word] / unigram_normalizer) / (unigrams[second_word] / unigram_normalizer), 2)
        if unigrams[second_word] > 4 and unigrams[first_word] > 4:
            bigram_pmi[bigram] = pmi

    for key, value in sorted(bigram_pmi.items(), key=lambda e: e[1], reverse=True)[:300]:
        print(key, value, bigrams[key], unigrams[key.split()[0]], unigrams[key.split()[1]])

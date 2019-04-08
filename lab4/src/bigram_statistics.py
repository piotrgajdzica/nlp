import json
from collections import defaultdict

import regex
import requests

from bills import bills


def is_bigram(token):
    r = regex.compile('^[a-ż]+( [a-ż]+)+$')
    return r.match(token) is not None


def is_unigram(token):
    r = regex.compile('^[a-ż]+$')
    return r.match(token) is not None

def get_bill_tokens(bill_id):
    tokens = requests.get('http://localhost:9200/bigram_index/_doc/%s/_termvectors?fields=custom_body' % bill_id).json()["term_vectors"]['custom_body']['terms']
    return {key: tokens[key]['term_freq'] for key in tokens.keys()}


def get_bill_frequencies(bill_id, unigrams, bigrams):
    tokens = get_bill_tokens(bill_id)
    for token in tokens.keys():
        if is_bigram(token):
            bigrams[token] += tokens[token]
        if is_unigram(token):
            unigrams[token] += tokens[token]



if __name__ == '__main__':

    unigram_frequency = defaultdict(lambda: 0)
    bigram_frequency = defaultdict(lambda: 0)

    for bill in bills():
        get_bill_frequencies(bill, unigram_frequency, bigram_frequency)
    open('../data/bigrams.json', 'w', encoding='utf-8').write(json.dumps(dict(bigram_frequency)))
    open('../data/unigrams.json', 'w', encoding='utf-8').write(json.dumps(dict(unigram_frequency)))

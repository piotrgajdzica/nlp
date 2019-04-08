import json
from math import log


def entropy(list):
    n = sum(list)
    return sum(k / n * log(k / n + (1 if k == 0 else 0), 2) for k in list)


def llr(list):
    return 2 * sum(list) * (entropy(list) - entropy([list[0] + list[2], list[1] + list[3]])
                            - entropy([list[0] + list[1], list[2] + list[3]]))


if __name__ == "__main__":
    unigrams = json.loads(open('../data/unigrams.json', encoding='utf-8').read())
    bigrams = json.loads(open('../data/bigrams.json', encoding='utf-8').read())

    bigram_normalizer = sum(bigrams.values())
    unigram_normalizer = sum(unigrams.values())
    print(bigram_normalizer)
    print(unigram_normalizer)
    bigram_llr = {}

    for bigram in bigrams.keys():

        first_word, second_word = bigram.split()

        a_and_b = bigrams[bigram]
        only_a = unigrams[first_word]
        only_b = unigrams[second_word]
        nor_a_nor_b = unigram_normalizer - only_a - only_b + a_and_b

        llr_value = llr([a_and_b, only_a, only_b, nor_a_nor_b])
        bigram_llr[bigram] = llr_value

    for key, value in sorted(bigram_llr.items(), key=lambda e: e[1], reverse=True)[:300]:
        print(key, value, bigrams[key], unigrams[key.split()[0]], unigrams[key.split()[1]])

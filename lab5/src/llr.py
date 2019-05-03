from collections import defaultdict
from math import log


def entropy(list):
    n = sum(list)
    return sum(k / n * log(k / n + (1 if k == 0 else 0), 2) for k in list)


def llr(list):
    return 2 * sum(list) * (entropy(list) - entropy([list[0] + list[2], list[1] + list[3]])
                            - entropy([list[0] + list[1], list[2] + list[3]]))


def is_correct_form(bigram):
    first, second = bigram.split('\t')
    return first.split()[1] == 'subst' and second.split()[1] in ['subst', 'adj']


if __name__ == '__main__':
    bigrams = defaultdict(lambda: 0)
    results = open('../data/results.txt', 'w', encoding='utf-8')
    for bigram in open('../data/bigrams.txt', encoding='utf-8').readlines():
        bigrams[bigram[:-1]] += 1

    prefix_frequencies = defaultdict(lambda: 0)
    sufix_frequencies = defaultdict(lambda: 0)
    total_event_count = 0
    llr_values = {}

    for bigram, frequency in bigrams.items():
        prefix, sufix = bigram.split('\t')
        prefix_frequencies[prefix] += frequency
        sufix_frequencies[sufix] += frequency
        total_event_count += frequency

    for bigram, frequency in bigrams.items():
        prefix, sufix = bigram.split('\t')
        total = total_event_count - prefix_frequencies[prefix] - sufix_frequencies[sufix] + frequency
        llr_values[bigram] = llr([frequency, prefix_frequencies[prefix], sufix_frequencies[sufix], total])


    for key, value in list(filter(lambda key: is_correct_form(key[0]), sorted(llr_values.items(), key=lambda e: e[1], reverse=True)))[:1000]:
        # print("{0:<50} {1:<20} {2:<10} {3:<10} {4:<10}".format(" ".join(key.split('\t')), value, bigrams[key], prefix_frequencies[key.split('\t')[0]], sufix_frequencies[key.split('\t')[1]]))
        print("{0:<50} {1:<20} {2:<10} {3:<10} {4:<10}".format(" ".join(key.split('\t')), value, bigrams[key], prefix_frequencies[key.split('\t')[0]], sufix_frequencies[key.split('\t')[1]]))
        # results.write("{0:<50} {1:<20} {2:<10} {3:<10} {4:<10}\n".format(" ".join(key.split('\t')), value, bigrams[key], prefix_frequencies[key.split('\t')[0]], sufix_frequencies[key.split('\t')[1]]))


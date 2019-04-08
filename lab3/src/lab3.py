import os
from collections import defaultdict

import regex
import requests
import matplotlib.pyplot as plt


def bills():
    data_dir = '../../lab1/data'
    for directory in os.listdir(data_dir):
        if directory.endswith('txt'):
            # print("directory: " + directory)

            bill = open(os.path.join(data_dir, directory), encoding='UTF-8').read()
            text = regex.sub(r"[ \t\r\f\v ][ \t\r\f\v ]+", "", bill)
            # print(text[:400])

            r = regex.match(
                r'\s*(Dz\.U\.\s*z\s*(?P<journal_year>\d+)\s*r\.\s*(N|n)r\s*(?P<journal_number>\d+),?\s*?poz.\s*(?P<position>\d+).?\s*)?([a-żA-Ż \d\.\(\)]*\s?){0,4}\s*(ustawa|USTAWA|U S T A W A|Ustawa|ustawA|USTAWa)[^\n]*\n[^\n]*\s*z\s*dnia\s*\d{1,2}\s*[a-żA-Ź]*\s*(?P<year>\d{4})\s*r\.\s*(?P<title>[\s\S]*?)\n\s*(Rozdział\s*(1|I)|Art.\s*(1|l)[^\d]|TYTUŁ\s*I|Dział\s*I|część\s*ogólna)',
                text)

            if not directory.startswith("2003_1187"):
                if r is None:
                    yield bill, "", "", "", "f"
                else:
                    yield bill, r.group("title"), r.group("journal_year"), r.group("position"), directory.split('.')[0]
                    # break


def get_document_tokens(id, d):
    res = requests.get(('http://localhost:9200/legislative_index/_doc/%s/_termvectors?fields=custom_body' % id)).json()[
        'term_vectors']['custom_body']['terms']

    p = regex.compile('^[a-Ź][a-Ź]+$')
    for key in res.keys():
        if p.match(key) is not None:
            d[key] += res[key]['term_freq']


def plot_terms(terms):
    plt.plot(range(len(terms)), [x for x in sorted(terms.values(), reverse=True)], 'o')
    # plt.xscale('log')
    # plt.yscale('log')
    plt.xlabel('rank')
    plt.ylabel('number of occurrences')
    plt.show()


def load_terms_to_file():
    f = open('../data/term_frequencies2.txt', 'w', encoding='utf-8')
    terms = defaultdict(lambda: 0)

    for bill, title, year, position, bill_id in bills():
        get_document_tokens(bill_id, terms)
    for key in sorted(terms.keys(), key=lambda x : terms[x]):
        f.write("%s %s\n" % (key, terms[key]))
        print(key, terms[key])


def retrieve_terms_from_file():
    terms = {}
    f = open('../data/term_frequencies.txt', encoding='utf-8')
    for line in f.readlines():
        key, value = line.split()
        terms[key] = int(value)
    return terms


def load_dictionary_to_file():
    dict = open('../data/dictionary.txt', 'w', encoding='utf-8')
    full_dict = open('../data/full_dictionary.txt', encoding='utf-8')
    words = set()
    for line in full_dict.readlines():
        word = line.split(';')[1]
        words.add(word.lower())

    for word in words:
        dict.write('%s\n' % word)

def load_dictionary_to_json():
    dict = open('../data/dictionary.json', 'w', encoding='utf-8')
    full_dict = open('../data/full_dictionary.txt', encoding='utf-8')
    words = {}

    p = regex.compile('^[a-Ź][a-Ź]+$')

    for line in full_dict.readlines():
        word = line.split(';')[1]
        if p.match(word) is not None:
            words[word.lower()] = 1

    terms = retrieve_terms_from_file()

    for term, frequency in terms.items():
        if term in words.keys():
            words[term] += frequency

    dict.write(str(words).replace(r"""'""", r'"'))


def first_part():
    terms = retrieve_terms_from_file()
    plot_terms(terms)


def retrieve_words_from_file():
    dict = open('../data/dictionary.txt', encoding='utf-8')
    words = set()

    for line in dict.readlines():
        words.add(line[:-1])
    return words


def find_30_words_highest_rank(words, terms):
    counter = 0
    for key, value in sorted(terms.items(), key=lambda item: item[1], reverse=True):
        if key not in words:
            print(key, value)
            counter += 1
            if counter >= 30:
                break


def find_30_words_3_occurrences(words, terms):
    counter = 0
    for key, value in filter(lambda item: item[1] == 2, sorted(terms.items(), key=lambda item: item[0], reverse=False)):
        if key not in words:
            print(key)
            counter += 1
            if counter >= 30:
                break


def correction(spellchecker, word):
    spellchecker.unknown([word])

    for dist in range(1, 5):
        spellchecker.distance = dist
        ret = spellchecker.correction(word)
        if ret == word:
            pass
        else:
            return ret
    return None


def find_30_words_3_occurrences_levelstein():

    from spellchecker import SpellChecker

    spell = SpellChecker(local_dictionary='../data/dictionary.json')
    terms = retrieve_terms_from_file()
    words = retrieve_words_from_file()

    # find those words that may be misspelled
    # misspelled = spell.unknown(['ustawf'])

    for word in ['ustawf']:
        # Get the one `most likely` answer
        print(spell.correction(word))

        # Get a list of `likely` options
        print(spell.candidates(word))
    counter = 0
    for key, value in filter(lambda item: item[1] == 2, sorted(terms.items(), key=lambda item: item[0], reverse=False)):
        if key not in words:
            print(key, correction(spell, key))
            counter += 1
            if counter >= 30:
                break


# GET legislative_index/_search


if __name__ == '__main__':
    # load_dictionary_to_json()
    # find_30_words_3_occurrences_levelstein()
    # load_terms_to_file()
    # load_dictionary_to_file()
    terms = retrieve_terms_from_file()
    words = retrieve_words_from_file()
    find_30_words_highest_rank(words, terms)
    # find_30_words_3_occurrences(words, terms)
    # find_30_words_3_occurrences_levelstein()

    # load_terms_to_file()

    # for word in words:
    #     print(word)

    # load_terms_to_file()
    # load_dictionary_to_file()

# Find 30 words with the highest ranks that do not belong to the dictionary.

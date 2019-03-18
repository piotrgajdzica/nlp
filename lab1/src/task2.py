import os
from collections import defaultdict

from regex import regex


def bills():
    data_dir = '../data'
    for directory in os.listdir(data_dir):
        if directory.endswith('txt'):
            print("directory: " + directory)
            yield open(os.path.join(data_dir, directory), encoding='UTF-8').read()


print("hello")

bill = open("../data/1994_344.txt", encoding='UTF-8').read()

counter = 0
texts = {0: 'whole text', 1: 'article_number', 2: 'article_text'}
last_article_number = 0
article_number = 0
whole_text = ''
bill_text = ''
bill_references = defaultdict(lambda: 0)
article_references = defaultdict(lambda: 0)

def is_int(s):
    try:
        int(s)
        return True
    except:
        return False

def process_bill(article_number, bill_number, bill_text):

    if 'wprowadza się następujące zmiany' not in bill_text and 'dodaje się art' not in bill_text and 'racą moc' not in bill_text:
        r = regex.findall(r'(art\.(\d+\w?(-\s*\d+\w?)?(?!\))|pkt|ust\.|§|\si\s|oraz|,|\s|z\szastrzeżeniem)*)', bill_text, multiline=True)
        # r = regex.findall(r'art\.', bill_text, multiline=True)
        for el in r:


            current_choice = None
            current_number = 0
            current_bill = 0
            current_article = 0

            reference = el[0]
            # print(reference)

            match = regex.findall(r'(\d+|-\d+|art\.|ust\.|§|pkt)', reference)
            for el in match:
                if el == 'art.':
                    current_choice = 'art'
                elif el == 'ust.' or el == '§':
                    current_choice = 'ust'
                elif el.startswith('-'):
                    if is_int(el[1:]):
                        i = int(el[1:])
                        if current_choice == 'art':
                            for it in range(current_number + 1, i + 1):
                                article_references[it] += 1
                        elif current_choice == 'ust':
                            for it in range(current_number + 1, i + 1):
                                bill_references[(current_article, it)] += 1
                elif el == 'pkt':
                    current_choice = 'pkt'
                elif is_int(el):
                    current_number = int(el)
                    if current_choice == 'art':
                        current_article = int(el)
                        article_references[current_article] += 1
                    elif current_choice == 'ust':
                        bill_number = int(el)
                        bill_references[(current_article, bill_number)] += 1
            # print(match)
            # print("\n\n")

        r = regex.findall(r'((art\.)?(\d+\w?(-\s*\d+\w?)?(?!\))|pkt|ust\.|§|\si\s|oraz|,|\s|z\szastrzeżeniem)*ust\.\s*\d+(\d+\w?(-\s*\d+\w?)?(?!\))|pkt|ust\.|§|\si\s|oraz|,|\s|z\szastrzeżeniem)*)', bill_text, multiline=True)
        for el2 in r:
            if 'art.' not in el2[0]:
                current_choice = None
                current_number = 0
                current_bill = 0
                current_article = article_number

                reference = el2[0]
                print(reference)
                print(article_number)

                match = regex.findall(r'(\d+|-\d+|art\.|ust\.|§|pkt)', reference)
                for el in match:
                    if el == 'ust.' or el == '§':
                        current_choice = 'ust'
                    elif el.startswith('-'):
                        if is_int(el[1:]):
                            i = int(el[1:])
                            if current_choice == 'ust':
                                for it in range(current_number + 1, i + 1):
                                    bill_references[(article_number, it)] += 1
                    elif el == 'pkt':
                        current_choice = 'pkt'
                    elif is_int(el):
                        current_number = int(el)
                        if current_choice == 'ust':
                            bill_number = int(el)
                            bill_references[(article_number, bill_number)] += 1
                print(match)
                print("\n\n")
def process_article(whole_text, article_number, article_text):

    # print()
    # print(article_number)
    # print(article_text)
    # print()

    counter = 0
    bill_text = ''
    bill_number = 0
    whole_bill = ''

    # print("\n\narticle nr %d\n\n" % article_number)

    for el in regex.split(r'(?<=\n\s{0,2}?§? ?(?P<inner_nr>\d+)\.(?P<bill_text>[\s\S]*?))(?=\n\s{0,2}?\d+\.|$|n\s*Art\.?\s*\n?\d+[a-z]?\.?\s*\n)', article_text):

        if counter == 0:
            whole_bill = el
        elif counter == 1:
            bill_number = int(el)
        elif counter == 2:
            bill_text = el
        counter = (counter + 1) % 3

        if counter == 0:
            # print("bill nr: " + str(bill_number))
            # print("bill text: \n" + bill_text)
            process_bill(article_number, bill_number, bill_text)

    if bill_number == 0:
        # print("bill nr: " + "1")
        # print("bill text: \n" + article_text)
        process_bill(article_number, 1, article_text)

for el in regex.split(r'(?<=\n\s*Art\.?\s*\n?(?P<article_number>\d+)[a-z]?\.?\s*(?P<bill_text>\n[\s\S]*?\n\s*))(?=(Art\.?\s*\n?\d+[a-z]?\.?\s*\n|$))', bill, multiline=True):

    if counter == 0:
        whole_text = el
    elif counter == 1:
        last_article_number = article_number
        article_number = int(el)
    elif counter == 2:
        bill_text = el

    counter = (counter + 1) % 4
    if counter == 0 and last_article_number != article_number:
        process_article(whole_text, article_number, bill_text)

for key in sorted(article_references.keys(), key=lambda k: article_references[k]):
    print("article %s references: %s" % (key, article_references[key]))

for key in sorted(bill_references.keys(), key=lambda k: bill_references[k]):
    print("article %s bill %s references: %s" % (key[0], key[1], bill_references[key]))

# for key in sorted(mydict.iterkeys()):
#     print("%s: %s" % (key, mydict[key]))

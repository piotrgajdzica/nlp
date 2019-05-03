import requests
import os
import regex


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
                    yield bill, "f"
                else:
                    yield bill, directory.split('.')[0]


if __name__ == "__main__":

    output = open('../data/tags.txt', 'w', encoding='utf-8')

    for bill, directory in bills():
        print(directory)
        tags = str(requests.post("http://192.168.99.100:9200", data=bill.encode('utf-8')).content, encoding='utf-8')
        for tag in tags.split('\n\t')[1:]:
            word, tagged, _ = tag.split('\t', 2)
            output.write("%s %s\n" % (word, tagged.split(':')[0]))

import os

import requests
from regex import regex


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

            if r is None:
                yield bill, "", "", "", "f"
            else:
                yield bill, r.group("title"), r.group("journal_year"), r.group("position"), directory.split('.')[0]


def insert_bill_to_index(text, title, year, position, bill_id):
    host = 'http://localhost:9200'
    # http: // localhost: 9200 / legislative_index / _search
    endpoint = '/legislative_index/_doc/'
    json = {
        'custom_body': text,
        'title': title,
        'year': year,
        'position': position,
        'id': bill_id
    }
    r = requests.put(host + endpoint + bill_id, json=json)
    print(r.status_code)


if __name__ == '__main__':
    for bill, title, year, position, bill_id in bills():
        insert_bill_to_index(bill, title, year, position, bill_id)


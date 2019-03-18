import os

from regex import regex



def bills():
    data_dir = '../data'
    for directory in os.listdir(data_dir):
        if directory.endswith('txt'):
            # print("directory: " + directory)
            yield open(os.path.join(data_dir, directory), encoding='UTF-8').read()



if __name__ == '__main__':
    b = {}
    for year in range(1900, 2500):
        b[str(year)] = {}

    for bill in bills():

        text = regex.sub(r"[ \t\r\f\v ][ \t\r\f\v ]+", "", bill)
        # print(text[:400])

        r = regex.match(r'\s*(Dz\.U\.\s*z\s*(?P<journal_year>\d+)\s*r\.\s*(N|n)r\s*(?P<journal_number>\d+),?\s*?poz.\s*(?P<position>\d+).?\s*)?([a-żA-Ż \d\.\(\)]*\s?){0,4}\s*(ustawa|USTAWA|U S T A W A|Ustawa|ustawA|USTAWa)[^\n]*\n[^\n]*\s*z\s*dnia\s*\d{1,2}\s*[a-żA-Ź]*\s*(?P<year>\d{4})\s*r\.\s*(?P<title>[\s\S]*?)\n\s*(Rozdział\s*(1|I)|Art.\s*(1|l)[^\d]|TYTUŁ\s*I|Dział\s*I|część\s*ogólna)', text)
        # r = regex.match(r'\n*(Dz\.U\.z(?P<journal_year>\d+)r\.(N|n)r(?P<journal_number>\d+),?poz.(?P<position>\d+).?)?([a-żA-Ż\d\.\(\)]*\n?){0,4}\n*(ustawa|USTAWA|Ustawa|ustawA|USTAWa)[^\n]*\n[^\n]*\n*z\n?dnia\n?\d{1,2}\n?[a-żA-Ź]*\n?(?P<year>\d{4})\n?r\.\n*(?P<title>(.+\n)*?)\n*?(?P<title2>(.+\n)*?)\n*?(Rozdział(1|I)|Art.\n?(1|l)[^\d]|TYTUŁI|DziałI|częśćogólna)', text)
        # print(title.group())

        position = r.group("position")
        year = r.group("journal_year") or r.group("year")
        b[year][position] = {}
        b[year][position]["counter"] = 0
        b[year][position]["title"] = r.group("title")
        b[year][position]["journal_number"] = r.group("journal_number")
        b[year][position]["journal_year"] = r.group("journal_year")
        b[year][position]["year"] = r.group("year")
        b[year][position]["position"] = position

    counter = 0


    current_year = 0
    current_text = ''
    current_number = ''
    current_number_text = ''
    errors = 0

    for bill in bills():
        text = regex.sub(r"[ \t\r\f\v\n ]*", "", bill)
        r = regex.findall(
            r'(.{30}(?P<year>\d{4})r\.?.{30}|.{30}poz\.(?P<position>\d+).{30}|.{30}(N|n)r(?P<number>\d+).{30})',
            text, overlapped=True)

        for match in r:
            if match[2] != '':
                position = match[2]
                try:
                    b[current_year][position]["counter"] += 1
                    if current_number != b[current_year][position]["journal_number"] and int(current_year) < 2012:
                        # print("error")
                        # print(match)
                        # print(current_year)
                        # print(current_text)
                        # print(position)
                        # print(b[current_year][position]["journal_number"])
                        b[current_year][position]["journal_number"] = current_number
                        # print(current_number)
                        # print(current_number_text)
                        # print(b[current_year][position].get("journal_number_context", "empty"))
                        errors += 1
                    counter += 1
                except KeyError:
                    try:
                        b[current_year][position] = {}
                        b[current_year][position]["counter"] = 1
                        b[current_year][position]["position"] = position
                        b[current_year][position]["year"] = current_year
                        b[current_year][position]["journal_number"] = current_number
                        b[current_year][position]["journal_number_context"] = current_number_text
                    except KeyError:
                        errors += 1
                    # print("error: ")
                    # print(match)
                    # print(current_text)
                    # print(current_year)
                    # print(position)
            elif match[1] != '':
                current_text = match[0]
                current_year = match[1]
                current_number = None
                # print(current_year)
            else:
                current_number = match[4]
                current_number_text = match[0]
    #     print(r)
    # print(errors)
    # print(counter)

    values = []

    for year_group in b.values():
        for position in year_group.values():
            values.append(position)

    values = sorted(values, key=lambda x: x['counter'], reverse=False)

    for value in values:
        print('')
        print("title: %s" % value.get('title', 'unavailable'))
        print("year: %s" % value['year'])
        print("number: %s" % value['journal_number'])
        print("position: %s" % value['position'])
        print("number of references: %s" % value['counter'])
        print('')



    # Dz.U. z 1998 r. Nr 60, poz. 382
    #dz.u.z1996r.nr6,poz.40
    #dz.u.z1996r.nr6,poz.40
    # art l
    # art.l
    #
    #                                  USTAWA
    #                         z dnia 19 lutego 1998 r.
    #
    #                     o zmianie ustawy o rachunkowości

    # rok
    # pozycja
    # tytuł
    # numer dziennika
    # rok dziennika
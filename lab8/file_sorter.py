import os
import random
from shutil import copyfile
# import regex


# def bills():
#     data_dir = 'data'
#     for directory in os.listdir(data_dir):
#         if directory.endswith('txt'):
#             # print("directory: " + directory)
#
#             bill = open(os.path.join(data_dir, directory), encoding='UTF-8').read()
#             text = regex.sub(r"[ \t\r\f\v ][ \t\r\f\v ]+", "", bill)
#             # print(text[:400])
#
#             r = regex.match(
#                 r'\s*(Dz\.U\.\s*z\s*(?P<journal_year>\d+)\s*r\.\s*(N|n)r\s*(?P<journal_number>\d+),?\s*?poz.\s*(?P<position>\d+).?\s*)?([a-żA-Ż \d\.\(\)]*\s?){0,4}\s*(ustawa|USTAWA|U S T A W A|Ustawa|ustawA|USTAWa)[^\n]*\n[^\n]*\s*z\s*dnia\s*\d{1,2}\s*[a-żA-Ź]*\s*(?P<year>\d{4})\s*r\.\s*(?P<title>[\s\S]*?)\n\s*(Rozdział\s*(1|I)|Art.\s*(1|l)[^\d]|TYTUŁ\s*I|Dział\s*I|część\s*ogólna)',
#                 text)
#
#             if not directory.startswith("2003_1187"):
#                 if r is None:
#                     pass
#                 else:
#                     yield text, r.group("title"), r.group("journal_year"), r.group("position"), directory.split('.')[0]
#                     # break


# def split_two_changed():
#
#     title_checker = regex.compile(r'zmianie[\s\n]*ustawy')
#
#     changed_id = 0
#     not_changed_id = 0
#
#     for bill, title, *_ in bills():
#         try:
#             bill_text = bill.split(title)[1]
#         except ValueError:
#             bill_text = bill
#         if title_checker.search(title) is not None:
#             f = open('data_1/change%d.txt' % changed_id, 'w', encoding='utf-8')
#             changed_id += 1
#         else:
#             f = open('data_1/nchange%d.txt' % not_changed_id, 'w', encoding='utf-8')
#             not_changed_id += 1
#         f.write(bill_text)
#         f.close()


def split_validation_training():
    for file in os.listdir('data_1'):
        d = random.uniform(0.0, 1.0)
        if d < 0.6:
            dst = 'training'
        elif d < 0.8:
            dst = 'testing'
        else:
            dst = 'validation'
        copyfile(os.path.join('data_1', file), os.path.join(dst, file))


def prepare_slices():
    dirs = ['training', 'testing', 'validation']
    # slices = {
    #     'ten_percent': lambda l: l // 10,
    #     'one': lambda l: min(1, l),
    #     'ten': lambda l: min(10, l),
    #     'full_text': lambda l: l
    # }

    slices = {
        'max_50': lambda l: min(l, 50)
    }

    for slice in slices:
        for dir in dirs:
            output = open(os.path.join(dir, slice, 'labeled.txt'), 'w', encoding='utf-8')
            # output.write('text\tchanged\tnot_changed\n')
            for file in os.listdir(dir):
                print(file)
                if file.endswith('.txt'):
                    lines = list(filter(lambda line: line != '\n' and len(line) > 2, open(os.path.join(dir, file), encoding='utf-8').readlines()))
                    # line_indexes = sorted(random.sample(list(range(len(lines))), slices[slice](len(lines))))
                    line_indexes = list(range(slices[slice](len(lines))))
                    filtered_lines = [lines[i][:-1] for i in line_indexes]
                    output.write('__label__' + ('not_changed\t' if file.startswith('n') else 'changed\t') + " ".join(filtered_lines).replace('\n', " ") +'\n')
                    # changed = not file.startswith('n')
                    # output.write("%s\t%s\t%s\n" % ( " ".join(filtered_lines).replace('\n', " "), 1 if changed else 0, 0 if changed else 1 ))



if __name__ == '__main__':
    # split_two_changed()
    split_validation_training()
    prepare_slices()

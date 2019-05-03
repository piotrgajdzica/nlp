import regex


def is_word(word):
    try:
        word, tag = word.split()
        return tag not in ['interp', 'xxx', 'num'] and regex.compile('^[a-ż]+$').match(word) is not None
    except ValueError:
        return False

if __name__ == '__main__':
    input = open('../data/tags.txt', encoding='utf-8')
    output = open('../data/bigrams.txt', 'w', encoding='utf-8')

    keys = []
    previous_word = None
    for line in input.readlines():
        word = line[:-1]

        if previous_word is not None:
            if is_word(word) and is_word(previous_word):
                bigram = "%s\t%s\n" % (previous_word, word)
                # print(bigram)
                output.write(bigram)
        keys.append(word.split()[1])
        previous_word = word

    print(set(keys))
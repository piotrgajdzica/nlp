from collections import defaultdict

import regex

from lab1.task1 import bills

words = defaultdict(lambda: 0)

ust_sum = 0
for bill in bills():
    matches = regex.findall(r"(\b(u|U) ?(s|S) ?(t|T) ?(a|A) ?(w|W)( A)?(|a|A|ę|Ę|o|O|ą|Ą|ie|IE|y|Y|om|OM|ach|ACH|ami|AMI|ow)\b)", bill)

    for match in matches:
        words[match[0]] += 1

suma = 0

for key in sorted(words.keys(), key=lambda k: words[k]):
    print("%s: %s" % (key, words[key]))
    suma += words[key]
print('sum: %s' % suma)



if __name__ == '__main__':
    original = open('./testing/full_text/labeled.txt').readlines()
    predictions = open('/root/pexp').readlines()
    original_results = [line.split(" ")[0] for line in original]
    prediction_results = [line[:-1] for line in predictions]

    total = 0
    true_positive = 0
    fail_positive = 0
    fail_negative = 0
    true_negative = 0
    print(len(original_results))

    for i in range(len(original_results)):
        original_line = original_results[i]
        prediction_line = prediction_results[i]


        if prediction_line == '__label__changed' == original_line:
            true_positive += 1
        elif prediction_line == '__label__not_changed' == original_line:
            true_negative += 1
        elif prediction_line == '__label__not_changed' and original_line == '__label__changed':
            fail_negative += 1
        elif prediction_line == '__label__changed' and original_line == '__label__not_changed':
            fail_positive += 1
        else:
            print(prediction_line)
            print(original_line)

    print(true_negative, true_positive, fail_negative, fail_positive)

    P = true_positive / (true_positive + fail_positive)
    R = true_positive / (true_positive + fail_negative)
    F = 2 * P * R / (P + R)
    print('P: %f' % P)
    print('R: %f' % R)
    print('F: %f' % F)
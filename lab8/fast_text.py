import fasttext
from sklearn.metrics import confusion_matrix
import argparse
import numpy as np

def fast_text(input, test):
    classifier = fasttext.supervised(input, 'model', label_prefix='__label__')
    result = classifier.test(test)
    print('P@1:', result.precision)
    print('R@1:', result.recall)
    print('Number of examples:', result.nexamples)


def parse_labels(path):
    with open(path, 'r') as f:
        return np.array(list(map(lambda x: x[9:], f.read().split())))


def presicion():
    parser = argparse.ArgumentParser(description='Display confusion matrix.')
    parser.add_argument('test', help='Path to test labels')
    parser.add_argument('predict', help='Path to predictions')
    args = parser.parse_args()
    test_labels = parse_labels(args.test)
    pred_labels = parse_labels(args.predict)
    eq = test_labels == pred_labels
    print("Accuracy: " + str(eq.sum() / len(test_labels)))
print(confusion_matrix(test_labels, pred_labels))


if __name__ == '__main__':
    # split_two_changed()
    # split_validation_training()
    # prepare_slices()
    fast_text('./training/full_text/labeled.txt', 'testing/full_text/labeled.txt')
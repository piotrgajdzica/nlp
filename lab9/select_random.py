import os
import shutil
import random

if __name__ == '__main__':
    input_dir = '../lab1/data/'
    output_dir = './random_100_input/'
    files = list(filter(lambda file: file.endswith('.txt'), os.listdir(input_dir)))
    random.shuffle(files)
    files = files[:100]
    for file in files:
        shutil.copy(os.path.join(input_dir, file), os.path.join(output_dir, file))

import time
from concurrent.futures.thread import ThreadPoolExecutor
import os
from single_file import process_single_file

def long_blocking_function(id):
    for i in range(20):
        print("id: %d, iteration: %d" % (id, i))
        time.sleep(5)
    return id

#start 15:10

if __name__ == '__main__':
    ids = range(20)
    input_dir = '../lab1/data/'
    output_dir = './full_output/'
    files = os.listdir(input_dir)
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(process_single_file, os.path.join(input_dir, file), os.path.join(output_dir, file)) for file in files]
        for future in futures:
            print(future.result())

import multiprocessing
from time import time, process_time
from string import punctuation
from multiprocessing import Process, Manager

def read_file(file_name):
    words_list = []
    for line in open(file_name, 'r'):
        for word in line.translate(line.maketrans("", "", punctuation)).lower().split():
            words_list.append(word)

    return words_list


def write_file(word_counter, file_name):
    with open(file_name, 'w') as file:
        for (word, occurance) in word_counter.items():
            file.write('{:15} {:3}\n'.format(word, occurance))



class WordsCount(Process):
    lock = multiprocessing.Lock()

    def __init__(self, words_list):
        super().__init__()
        self.words_list = words_list


    def run(self):

        local_dict = {}
        for word in self.words_list:
            if word not in local_dict:
                local_dict[word] = 1
            else:
                local_dict[word] =+ 1

        WordsCount.lock.acquire()
        try:
            for i in local_dict.keys():
                if i in word_counter.keys():
                    word_counter[i] += local_dict[i]

                else:
                    word_counter[i] = local_dict[i]
        finally:
            WordsCount.lock.release()



with Manager() as manager:
    word_counter = manager.dict()
    processes = []
    input_list = read_file('text.txt')
    avg = len(input_list) / 10
    last = 0


    while last < len(input_list):
        processes.append(WordsCount(input_list[int(last):int(last + avg)]))
        last += avg

    start_time = time()

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print(process_time())
    print(word_counter)
    print('Got {} threads in {} seconds'.format(len(processes), time() - start_time))
    write_file(word_counter, 'result.txt')






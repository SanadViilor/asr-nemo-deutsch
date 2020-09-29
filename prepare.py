import os
import numpy as np
from tqdm import tqdm
from shutil import copyfile
from pathlib import Path

def read_tsv(filepath):
    samples=[]

    with open(str(filepath), 'r') as trainfile:
        filelines = trainfile.readlines()
        for fileline in tqdm(filelines):
            tokens = fileline.split('\t')
            file = tokens[1]
            transcript = tokens[2]
            element = [file, transcript]
            samples.append(element)
    
    return samples

def conditional_append(all_samples, path_of_clips, max_size):
    size_counter = 0
    selected_samples = []

    for i in all_samples:
        name, tr = i
        print(path_of_clips + name)
        if Path(path_of_clips + name).exists():
            
            size_counter += os.stat(path_of_clips + name).st_size

            if size_counter <= max_size:
                selected_samples.append(i)

    return selected_samples

def write_tsv(array, filepath):
    with open(str(filepath), 'a') as labelfile:
       for line in tqdm(array):
            linestr = str(line[0]) + '\t' + str(line[1]) + '\n'
            labelfile.write(linestr) 



if __name__ == '__main__':
    
    train_memory_limit = 8800000000
    test_memory_limit = 2200000000
    #sum: 11GB


    #create folder baseline_set and its subfolders: train, test
    rootpath = r'baseline_set'
    trainpath = r'baseline_set/train'
    testpath = r'baseline_set/test'

    if not os.path.exists(rootpath):
        os.makedirs(rootpath)
        os.makedirs(trainpath)
        os.makedirs(testpath)

    
    #read train.tsv and test.tsv to array
    train_samples = read_tsv(r'de/train.tsv')
    test_samples = read_tsv(r'de/test.tsv')


    np.random.shuffle(train_samples)
    np.random.shuffle(test_samples)


    #select elements of the arrays if the memory limit is not exceeded

    train_samples_baseline = conditional_append(train_samples, r'de/clips/', train_memory_limit)
    test_samples_baseline = conditional_append(test_samples, r'de/clips/', test_memory_limit)


    #iterate over these arrays and copy mp3s to the selected folder
    for i in train_samples_baseline:
        copyfile(r'de/clips/'+str(i[0]), r'baseline_set/train/'+str(i[0]))
        print('Copying training files')
    for j in test_samples_baseline:
        copyfile(r'de/clips/'+str(j[0]), r'baseline_set/test/'+str(j[0]))
        print('Copying testing files')



    #writing these arrays to tsvs in the destination folder
    write_tsv(train_samples_baseline, r'baseline_set/train/train.tsv')
    write_tsv(test_samples_baseline, r'baseline_set/test/test.tsv')

import os
import librosa
import json
import numpy

def read_tsv(filepath, path_to_data):
    samples=[]

    with open(str(filepath), 'r') as datafile:
        filelines = datafile.readlines()
        print(str(len(filelines)-1) + ' examples in total.')
        k = 0
        for fileline in filelines:
            tokens = fileline.split('\t')
            if 'path' not in tokens[1]:
                file = path_to_data + tokens[1]
                transcript = tokens[2]
                duration = librosa.core.get_duration(filename = file)
                element = [file, transcript, duration]
                samples.append(element)
                k = k + 1
                print(str(k) + ' of ' + str(len(filelines)-1) + ' lines read.')
    return samples

class HoursCounter():
    def __init__(self):
        self.counter = 0
    def count(self, num):
        self.counter = self.counter + num
        return int(self.counter/3600)




def conditional_append(all_samples, hours, alphabet):
    counter = HoursCounter()
    print('Sorting samples....')
    for j in all_samples:
        j[1] = j[1].lower().replace('\n', '').replace('?', '').replace('!', '').replace('\"', '').\
            replace(',', '').replace(':', '').replace('\'', '').replace(';', '').replace('-', '').\
                replace('„', '').replace('”', '').replace('»', '').replace('«', '').\
                    replace('…', '').replace('“', '').replace('‹', '').replace('›', '').\
                        replace('’', '').replace('–', '').replace('´', '').replace('á', 'a').\
                            replace('é', 'e').replace('.', '')
    selected_samples = [i for i in all_samples \
        if counter.count(i[2]) <= hours \
            if regstring(i[1], alphabet) == True]
    print('Sort done.')
    return selected_samples

def regstring(string, alphabet):
    for char in string:
        if char not in alphabet:
            return False
    return True

def write_json(array, json_path, alphabet):
    print('Writing ' + str(len(array)) + ' samples to ' + json_path)
    with open(json_path, 'w', encoding='utf8') as manifest:
        k = 0
        for j in array:
            metadata = {
                        "audio_filepath": j[0],
                        "duration": j[2],
                        "text": j[1]
                        }
            json.dump(metadata, manifest, ensure_ascii=False)
            manifest.write('\n')
            k = k + 1
            print('Wrote ' + str(k) + ' lines to manifest.')

def create_manifest(array, json_path, alphabet,  hours = float('Inf')):
    numpy.random.shuffle(array)
    modified_array = conditional_append(array, hours, alphabet)
    write_json(modified_array, json_path, alphabet)


if __name__ == '__main__':
    TSV_ROOT = '../../de/'
    DATA_ROOT = '../../de/clips/'
    german = 'aäbcdefghijklmnoöpqrsßtuüvwxyz '
    
    #CREATE TEST MANIFEST
#    print('\n\n\n\n CREATE TEST MANIFEST \n\n\n\n')
#    test_array = read_tsv(TSV_ROOT + 'test.tsv', DATA_ROOT)
#    create_manifest(test_array, 'test.json', german)
    #CREATE DEV MANIFEST
#    print('\n\n\n\n CREATE DEV MANIFEST \n\n\n\n')
#    dev_array = read_tsv(TSV_ROOT + 'dev.tsv', DATA_ROOT)
#    create_manifest(dev_array, 'dev.json', german)
    #CREATE TRAIN MANIFESTS
    print('\n\n\n\n CREATE TRAIN MANIFESTS \n\n\n\n')
    train_array = read_tsv(TSV_ROOT + 'train.tsv', DATA_ROOT)
    print('\n\n\n\n 20 HOURS \n\n\n\n')
    create_manifest(train_array, 'train_20.json', german, 20)
    print('\n\n\n\n 50 HOURS \n\n\n\n')
    create_manifest(train_array, 'train_50.json', german, 50)
    print('\n\n\n\n 100 HOURS \n\n\n\n')
    create_manifest(train_array, 'train_100.json', german, 100)
    print('\n\n\n\n 200 HOURS \n\n\n\n')
    create_manifest(train_array, 'train_200.json', german, 200)
    print('\n\n\n\n 500 HOURS \n\n\n\n')
    create_manifest(train_array, 'train_500.json', german, 500)
    print('\n\n\n\n 1000 HOURS \n\n\n\n')
    create_manifest(train_array, 'train_1000.json', german, 1000)
    print('\n\n\n\n INF HOURS \n\n\n\n')
    create_manifest(train_array, 'train_inf.json', german)


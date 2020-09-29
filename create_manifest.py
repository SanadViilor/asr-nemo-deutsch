import os
import librosa
import json
import numpy

def read_tsv(filepath, path_to_data):
    samples=[]

    with open(str(filepath), 'r') as datafile:
        filelines = datafile.readlines()
        print(str(len(filelines)) + ' examples in total.')
        for fileline in filelines:
            tokens = fileline.split('\t')
            file = path_to_data + tokens[0]
            transcript = tokens[1]
            duration = librosa.core.get_duration(filename=file)
            element = [file, transcript, duration]
            samples.append(element)
    return samples

class HoursCounter():
    def __init__(self):
        self.counter = 0
    def count(self, num):
        self.counter = self.counter + num
        return int(self.counter/3600)




def conditional_append(all_samples, hours, alphabet):
    counter = HoursCounter()
    for j in all_samples:
        i[1] = i[1].replace('\n', '').replace('?', '').replace('!', '').replace('\"', '').replace(',', '').replace(':', '').replace('\'', '').replace(';', '').replace('-', '').replace('„', '').replace('”', '').replace('»', '').replace('«', '').replace('…', '').replace('“', '').replace('‹', '').replace('›', '').replace('’', '').replace('–', '').replace('´', '')
    selected_samples = [i for i in all_samples if counter.count(i[2]) <= hours if regstring(i[1], alphabet) == True]
    return selected_samples

def regstring(string, alphabet):
    for char in string:
        if char not in alphabet:
            return False
    return True

def write_json(array, json_path, alphabet):
    with open(json_path, 'w', encoding='utf8') as manifest:
        k = 0
        for j in array:
            metadata = {
                        "audio_filepath": j[0],
                        "duration": j[2],
                        "text": j[1]
                        }
            json.dump(metadata, manifest)
            manifest.write('\n')
            k = k + 1
            print('Wrote ' + str(k) + ' lines to manifest.')



if __name__ == '__main__':
   PATH_TO_DATA = 'TODO'
   PATH_TO_TSV  = 'TODO'
   alphabet = 'aáäbcdeéfghijklmnoöpqrsßtuüvwxyz '
   array = read_tsv(PATH_TO_TSV, PATH_TO_DATA)
   numpy.random.shuffle(array)
   hundred_hours_array = conditional_append(array, 100, alphabet)
   write_json(hundred_hours_array, 'TODO')


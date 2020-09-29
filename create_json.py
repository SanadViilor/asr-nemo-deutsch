import os
import librosa
import json
import numpy

def read_tsv(filepath):
    samples=[]

    with open(str(filepath), 'r') as datafile:
        filelines = datafile.readlines()
        i = 0
        ab = int(2*len(filelines)/3)
        print(str(ab) + ' examples in total.')
        for fileline in filelines:
            tokens = fileline.split('\t')
            file = PATH_TO_DATA + tokens[0]
            transcript = tokens[1].lower().replace('.', '').replace(',', '')
            duration = librosa.core.get_duration(filename=file)
            element = [file, transcript, duration]
            samples.append(element)
            i = i + 1
            if i>= ab:
                break
            print('Already appended ' + str(i) + ' samples.')
    
    return samples

def write_json(array, json_path):
    with open(json_path, 'w') as manifest:
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






####
PATH_TO_DATA = 'clips/'
# test_samples = read_tsv('test.tsv')
# write_json(test_samples, 'test_manifest.json')

train_samples = read_tsv('train.tsv')
write_json(train_samples, 'train_manifest.json')




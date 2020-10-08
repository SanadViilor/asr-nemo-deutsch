#USED THIS CODE TO CHANGE FILE FORMATS (mp3 -> wav) IN MANIFEST FILES
import json
def write_json(array, json_path):
    print('Writing ' + str(len(array)) + ' samples to ' + json_path)
    with open(json_path, 'w', encoding='utf8') as manifest:
        k = 0
        for j in array:
            metadata = {
                        "audio_filepath": j["audio_filepath"],
                        "duration": j["duration"],
                        "text": j["text"]
                        }
            json.dump(metadata, manifest, ensure_ascii=False)
            manifest.write('\n')
            k = k + 1
            print('Wrote ' + str(k) + ' lines to manifest.')

#def read_json(json_path):
    

#TODO read manifest to list of dictionaries

files = ['train_20.json', 'train_50.json', 'train_100.json', 'train_200.json', 'train_500.json', 'train_1000.json', 'train_inf.json', 'test.json', 'dev.json']

for i in files:
    listOfDicts = []

    with open(i, 'r') as source:
        for line in source.readlines():
            dict = json.loads(line)
            n = dict["audio_filepath"].split("mp3")
            dict["audio_filepath"] = n[0] + "wav"
            print(dict["audio_filepath"])

            listOfDicts.append(dict)

    write_json(listOfDicts, 'wav_' + i)
    

#TODO change mp3 to wav
#TODO write manifest to the same file
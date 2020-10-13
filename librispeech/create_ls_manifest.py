from __future__ import absolute_import, division, print_function

import json
import os
import wave


def main(data_directory, output_file):
    labels = []
    durations = []
    keys = []
    for group in os.listdir(data_directory):
        if group.startswith('.'):
            continue
        speaker_path = os.path.join(data_directory, group)
        for speaker in os.listdir(speaker_path):
            if speaker.startswith('.'):
                continue
            labels_file = os.path.join(speaker_path, speaker,
                                       '{}-{}.trans.txt'
                                       .format(group, speaker))
            for line in open(labels_file):
                split = line.strip().split()
                file_id = split[0]
                label = ' '.join(split[1:]).lower()
                audio_file = os.path.join(speaker_path, speaker,
                                          file_id) + '.wav'
                audio = wave.open(audio_file)
                duration = float(audio.getnframes()) / audio.getframerate()
                audio.close()
                keys.append(audio_file)
                durations.append(duration)
                labels.append(label)
    with open(output_file, 'w') as out_file:
        for i in range(len(keys)):
            line = json.dumps({'audio_filepath': keys[i], 'duration': durations[i],
                              'text': labels[i]})
            out_file.write(line + '\n')


if __name__ == '__main__':
    main('../../LibriSpeech/test-clean', '../manifests/ls_test.json')
    main('../../LibriSpeech/train-clean-100', '../manifests/ls_train_100.json')


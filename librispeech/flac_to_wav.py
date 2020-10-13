
import os
from glob import glob
from pydub import AudioSegment

TRAIN_PATH = '../../LibriSpeech/train-clean-100/'
TEST_PATH = '../../LibriSpeech/test-clean/'

test_sounds = [y for x in os.walk(TEST_PATH) for y in glob(os.path.join(x[0], '*.flac'))]
train_sounds = [y for x in os.walk(TRAIN_PATH) for y in glob(os.path.join(x[0], '*.flac'))]

print(str(len(test_sounds)) + ' TEST SOUNDS IN TOTAL.')
print(str(len(train_sounds)) + ' TRAIN SOUNDS IN TOTAL.')

print(test_sounds[121])
print(test_sounds[1113])
print(train_sounds[1121])
testc = 0
trainc = 0
for i in test_sounds:
	sound = AudioSegment.from_file(i, format="flac")
	k = i.split('flac')[0] + 'wav'
	print(k)
	sound.export(k, format="wav")
	os.remove(i)
	testc = testc + 1
	print('Converted ' + str(testc) + ' out of ' + str(len(test_sounds)) + ' test samples.')


for i in train_sounds:
        sound = AudioSegment.from_file(i, format="flac")
        k = i.split('flac')[0] + 'wav'
        print(k)
        sound.export(k, format="wav")
        os.remove(i)
        trainc = trainc + 1
        print('Converted ' + str(trainc) + ' out of ' + str(len(train_sounds)) + ' train samples.')



# RUN THIS FILE FOR CONVERTING COMMONVOICE MP3 CLIPS TO WAV
import os
from pydub import AudioSegment

PATH_TO_AUDIO = '../de/clips/'
j = 0
print('THERE ARE ' + str(len(os.listdir(PATH_TO_AUDIO))) + 'SAMPLES TO CONVERT.')
for i in os.listdir(PATH_TO_AUDIO):
	sound = AudioSegment.from_mp3(PATH_TO_AUDIO + str(i))
	sound.export(PATH_TO_AUDIO + i.split('mp3')[0] + 'wav', format="wav")
	j = j + 1
	print('Converted ' + str(j) + ' mp3s to wav.')
	os.remove(PATH_TO_AUDIO + str(i))

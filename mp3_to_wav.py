# RUN THIS FILE FOR CONVERTING COMMONVOICE MP3 CLIPS TO WAV
import os
from pydub import AudioSegment

PATH_TO_AUDIO = '../de/clips/'
j = 0
s=0
print('THERE ARE ' + str(len(os.listdir(PATH_TO_AUDIO))) + ' SAMPLES TO CONVERT.')
files = os.listdir(PATH_TO_AUDIO)
for i in files:
	s=s+1
	print('scanned '+str(s))
	if (i.split('mp3')[0]) not in files:
		sound = AudioSegment.from_mp3(PATH_TO_AUDIO + str(i))
		sound.export(PATH_TO_AUDIO + i.split('mp3')[0] + 'wav', format="wav")
		j = j + 1
		print('Converted ' + str(j) + ' mp3s to wav.')
		os.remove(PATH_TO_AUDIO + str(i))

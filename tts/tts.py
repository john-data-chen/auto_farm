# -*- coding: utf-8 -*-
import sys
import requests
import os
from ConfigParser import SafeConfigParser
from slack.msg_sender import *

# set encoding to utf-8, then we can input traditional and simplified Chinese
if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')

# get parameters in config file
config_parser = SafeConfigParser()
config_parser.read('./config.txt')

# load configs
cyberon_url = config_parser.get('TTS', 'CYBERON_URL')
language = config_parser.get('TTS', 'LANGUAGE')
speaker = config_parser.get('TTS', 'SPEAKER')
speed = config_parser.get('TTS', 'SPEED')
gain = config_parser.get('TTS', 'GAIN')
f0 = config_parser.get('TTS', 'F0')
pd_1 = config_parser.get('TTS', 'PUNCTUDURATION_1')
pd_2 = config_parser.get('TTS', 'PUNCTUDURATION_2')
# combine pd_1 and pd_2
punctuDuration = \
	"{\",\": " + str(pd_1) + ", \".\":" + str(pd_2) + ", \"，\": " + str(pd_1) + ", \"。\": " + str(pd_2) + "}"


def tts(target, tts_mp3_path, editor_tuple):
	mp3_path = tts_mp3_path + editor_tuple[0]
	content = editor_tuple[1]
	# print mp3_path
	# print content

	payload = {'text': content, 'language': language, 'speaker': speaker, 'speed': speed, 'gain': gain, 'f0': f0,
	           'punctuDuration': punctuDuration}

	# send request
	r = requests.post(cyberon_url, params=payload, stream=True)
	# if code is not 200, do the error handle
	if r.status_code != 200:
		error = "download mp3 from TTS had error: \n" + str(r.content)
		print error
		get_tts_error(error)
		exit()
	else:
		# save mp3
		with open(mp3_path, 'wb') as f:
			for block in r.iter_content(1024):
				f.write(block)

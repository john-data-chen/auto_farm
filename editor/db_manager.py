# -*- coding: utf-8 -*-
import sys
import datetime
from checklog import log_save_check
import output
from info_img import process
import json
from pprint import pprint


# set encoding to utf-8, then we can input traditional and simplified Chinese
if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')

# get current file path
# print os.getcwd()


def save_to_db(articles_path, rss_path, target, file_time, title, text, last_pubDate):
	pass

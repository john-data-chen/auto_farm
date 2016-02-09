# -*- coding: utf-8 -*-
import sys
from pprint import pprint
from ConfigParser import SafeConfigParser
from pymongo import MongoClient


# set encoding to utf-8, then we can input traditional and simplified Chinese
if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')


# get parameters in config file
config_parser = SafeConfigParser()
config_parser.read('config.txt')
mongodb_uri = config_parser.get('MONGODB', 'URI')

# connect to mongodb
client = MongoClient(mongodb_uri)
db = client['auto_farm_db']


def save_to_db(target, file_time, title, text):
	post = {"created_time": file_time, "title": title, "text": text}
	posts = db[target]
	try:
		post_id = posts.insert_one(post).inserted_id
	except Exception as e:
		print e

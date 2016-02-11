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


def save_earthquake(file_time, title, text, img_url):
	posts = db.earthquake
	if posts.find({"img_url": img_url}).count() == 0:
		doc = {"created_time": file_time, "title": title, "text": text, "img_url": img_url}
		try:
			posts.insert_one(doc).inserted_id
		except Exception as e:
			print "save to database fail: " + e
			print "exit..."
			exit()
	else:
		print "A same post existed in database."
		exit()


def save_gas_price(cpc_date, fpcc_date, cpc92, cpc95, cpc98, cpc_diesel, fpcc92, fpcc95, fpcc98, fpcc_diesel,
					file_time, title, text):
	posts = db.gas_price
	if posts.find({"cpc_date": cpc_date, "fpcc_date": fpcc_date}).count() == 0:
		doc = {"cpc_date": cpc_date, "fpcc_date": fpcc_date, "cpc92": cpc92, "cpc95": cpc95, "cpc98": cpc98,
			"cpc_diesel": cpc_diesel, "fpcc92": fpcc92, "fpcc95": fpcc95, "fpcc98": fpcc98, "fpcc_diesel": fpcc_diesel,
			"created_time": file_time, "title": title, "text": text}
		try:
			posts.insert_one(doc).inserted_id
		except Exception as e:
			print "save to database fail: " + e
			print "exit..."
			exit()
	else:
		print "A same post existed in database."
		exit()


def save_tw_stock(file_time, title, text, twi_volume, otc_volume, electronic_volume, financial_volume):
	posts = db.tw_stock
	if posts.find({"twi_volume": twi_volume, "otc_volume": otc_volume, "electronic_volume": electronic_volume,
	"financial_volume": financial_volume}).count() == 0:
		doc = {"created_time": file_time, "title": title, "text": text, "twi_volume": twi_volume,
		"otc_volume": otc_volume, "electronic_volume": electronic_volume, "financial_volume": financial_volume}
		try:
			posts.insert_one(doc).inserted_id
		except Exception as e:
			print "save to database fail: " + e
			print "exit..."
			exit()
	else:
		print "A same post existed in database."
		exit()

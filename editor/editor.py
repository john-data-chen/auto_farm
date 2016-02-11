# -*- coding: utf-8 -*-
import sys
import datetime
from checklog import log_save_check
import output
from info_img import process
import json
from pprint import pprint
import db_manager


# set encoding to utf-8, then we can input traditional and simplified Chinese
if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')

# get time of now
file_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
last_pubDate = datetime.datetime.now().strftime('%A, %d %b %Y %H:%M:%S')

# get current file path
# print os.getcwd()


def earthquake_editor(crawler_tuple, logs_path, target, no_update_path, articles_path, templates_path, rss_path):
	date = crawler_tuple[0]
	# remove un-need space
	day = crawler_tuple[1].strip()
	time = crawler_tuple[2]
	depth = crawler_tuple[3]
	scale = crawler_tuple[4]
	location = crawler_tuple[5]
	location_in_title = location[location.find("(") + 1:location.find(")")]
	# print location_in_title
	area_max = crawler_tuple[6]
	img_url = crawler_tuple[7]

	# debug message
	"""
	print date
	print day
	print time
	print depth
	print scale
	print location
	print area_max
	print img_url
	"""

	# check old date to confirm update
	log_save_check.last_date(logs_path, target, no_update_path, file_time, date)

	# output img_url
	# print "img_url in editor.py: " + img_url
	with open(rss_path + target + "/img_url.txt", "w") as text_file:
		text_file.write("%s" % img_url)
	# load template
	with open(templates_path + target + "_title.json") as js_file:
		titles_in_js = json.load(js_file, encoding='utf-8')
	# send data to template
	title = titles_in_js["title"] % (location_in_title, scale)
	print title.encode('utf-8').replace("<br>", "")

	with open(templates_path + target + "_text.json") as js_file:
		texts_in_js = json.load(js_file, encoding='utf-8')
	# send data to template
	text = texts_in_js["text"] % (date, day, time, scale, location, depth, area_max)
	print text.encode('utf-8').replace("<br>", "")

	# query mongodb to check whether this post existed or not, if not, save to database
	db_manager.save_earthquake(file_time, title, text, img_url)
	# output txt files and send to slack
	output.txt_files(articles_path, rss_path, target, file_time, title, text, last_pubDate)


def gas_price_editor(crawler_tuple, logs_path, target, no_update_path, articles_path, templates_path, rss_path):
	cpc98 = crawler_tuple[1]
	cpc95 = crawler_tuple[2]
	cpc92 = crawler_tuple[3]
	cpc_diesel = crawler_tuple[4]
	fpcc98 = crawler_tuple[6]
	fpcc95 = crawler_tuple[7]
	fpcc92 = crawler_tuple[8]
	fpcc_diesel = crawler_tuple[9]
	cpc_date = crawler_tuple[0]
	fpcc_date = crawler_tuple[5]

	# debug message
	"""
	print "cpc_date:" + cpc_date
	print "cpc98: " + cpc98
	print "cpc95: " + cpc95
	print "cpc92: " + cpc92
	print "cpc_diesel: " + cpc_diesel
	print "fpcc_date:" + fpcc_date
	print "fpcc98: " + fpcc98
	print "fpcc95: " + fpcc95
	print "fpcc92: " + fpcc92
	print "fpcc_diesel: " + fpcc_diesel
	"""

	# check old date to confirm update
	log_save_check.gas_price_dates(logs_path, target, no_update_path, file_time, cpc_date, fpcc_date)

	# save and check gas price logs
	log_save_check.previous_gas_price(logs_path, target, file_time,
										cpc92, cpc95, cpc98, cpc_diesel, fpcc92, fpcc95, fpcc98, fpcc_diesel)

	# get current file path
	# print os.getcwd()
	# load template
	with open(templates_path + target + "_title.json") as js_file:
		titles_in_js = json.load(js_file, encoding='utf-8')
	# send data to template
	title = titles_in_js["title"]
	print title.encode('utf-8').replace("<br>", "")

	with open(templates_path + target + "_text.json") as js_file:
		texts_in_js = json.load(js_file, encoding='utf-8')
	# send prices to template
	text = texts_in_js["text"] % (file_time, cpc92, cpc95, cpc98, cpc_diesel, fpcc92, fpcc95, fpcc98, fpcc_diesel)
	print text.encode('utf-8').replace("<br>", "")

	# query mongodb to check whether this post existed or not, if not, save to database
	db_manager.save_gas_price(cpc_date, fpcc_date, cpc92, cpc95, cpc98, cpc_diesel, fpcc92, fpcc95, fpcc98, fpcc_diesel,
							file_time, title, text)
	# output txt files and send to slack
	output.txt_files(articles_path, rss_path, target, file_time, title, text, last_pubDate)


def gas_predict_editor(crawler_tuple, logs_path, target, no_update_path, articles_path, templates_path, rss_path):
	update_date = crawler_tuple[0]
	change_sign = crawler_tuple[1]
	if change_sign != u'不調整':
		change_val = crawler_tuple[2] + u'元'
	else:
		change_val = ""
	# debug message
	"""
	print "update_date: " + update_date
	print "change_sign:" + change_sign
	print "change_val: " + change_val
	"""

	# check old date to confirm update
	log_save_check.last_date(logs_path, target, no_update_path, file_time, update_date)

	# get current file path
	# print os.getcwd()
	# load template
	with open(templates_path + target + "_title.json") as js_file:
		titles_in_js = json.load(js_file, encoding='utf-8')
	# pprint(titles_in_js)
	# fix local variable 'title' referenced before assignment
	title = ""
	if change_sign == u'漲':
		title = titles_in_js["price_up_title"]
		title = title % change_val
	elif change_sign == u'降':
		title = titles_in_js["price_down_title"]
		title = title % change_val
	elif change_sign == u'不調整':
		title = titles_in_js["no_adjust_title"]
	else:
		print "incorrect change_sign: " + change_sign.encode('utf-8')
	print title.encode('utf-8').replace("<br>", "")

	with open(templates_path + target + "_text.json") as js_file:
		texts_in_js = json.load(js_file, encoding='utf-8')
	# pprint(texts_in_js)
	if change_sign != u'不調整':
		text = texts_in_js["price_change_text"] % (update_date, change_sign, change_val)
	elif change_sign == u'不調整':
		text = texts_in_js["no_adjust_text"] % (update_date, change_sign)
	# send prices to template
	print text.encode('utf-8').replace("<br>", "")

	# if change_sign is u'漲' or u'降', remove u'元' in the end
	if change_sign != u'不調整':
		change_val = change_val[0:-1]
	# produce info img
	process.gas_predict_img(target, file_time, change_sign, change_val)
	# output txt files and send to slack
	output.txt_files(articles_path, rss_path, target, file_time, title, text, last_pubDate)


def tw_stock_editor(crawler_tuple, logs_path, target, no_update_path, articles_path, templates_path, rss_path):
	twi = crawler_tuple[0]
	twi_ch_sign = crawler_tuple[1]
	twi_ch_pt = crawler_tuple[2]
	twi_ch_percent = str(round(float(twi_ch_pt) / (float(twi) - float(twi_ch_pt)) * 100, 2)) + "%"
	twi_volume = crawler_tuple[3]
	otc = crawler_tuple[4]
	otc_ch_sign = crawler_tuple[5]
	otc_ch_pt = crawler_tuple[6]
	otc_ch_percent = str(round(float(otc_ch_pt) / (float(otc) - float(otc_ch_pt)) * 100, 2)) + "%"
	otc_volume = crawler_tuple[7]
	electronic = crawler_tuple[8]
	electronic_ch_sign = crawler_tuple[9]
	electronic_ch_pt = crawler_tuple[10]
	electronic_ch_percent = str(round(float(electronic_ch_pt) / (float(electronic) - float(electronic_ch_pt)) * 100, 2)) + "%"
	electronic_volume = crawler_tuple[11]
	financial = crawler_tuple[12]
	financial_ch_sign = crawler_tuple[13]
	financial_ch_pt = crawler_tuple[14]
	financial_ch_percent = str(round(float(financial_ch_pt) / (float(financial) - float(financial_ch_pt)) * 100, 2)) + "%"
	financial_volume = crawler_tuple[15]

	# debug message
	"""
	print "twi: " + twi
	print "twi_ch_sign: " + twi_ch_sign
	print "twi_ch_pt: " + twi_ch_pt
	print "twi_ch_percent: " + twi_ch_percent
	print "twi_volume: " + twi_volume
	print "otc: " + otc
	print "otc_ch_sign: " + otc_ch_sign
	print "otc_ch_pt: " + otc_ch_pt
	print "otc_ch_percent: " + otc_ch_percent
	print "otc_volume: " + otc_volume
	print "electronic: " + electronic
	print "electronic_ch_sign: " + electronic_ch_sign
	print "electronic_ch_pt: " + electronic_ch_pt
	print "electronic_ch_percent: " + electronic_ch_percent
	print "electronic_volume: " + electronic_volume
	print "financial: " + financial
	print "financial_ch_sign: " + financial_ch_sign
	print "financial_ch_pt: " + financial_ch_pt
	print "financial_ch_percent: " + financial_ch_percent
	print "financial_volume: " + financial_volume
	"""

	# load template
	with open(templates_path + target + "_title.json") as js_file:
		titles_in_js = json.load(js_file, encoding='utf-8')
	title = titles_in_js["title"]
	print title.encode('utf-8').replace("<br>", "")

	with open(templates_path + target + "_text.json") as js_file:
		texts_in_js = json.load(js_file, encoding='utf-8')
	# send data to template
	text = texts_in_js["text"] % (file_time, twi_ch_sign, twi_ch_pt, twi, twi_ch_sign, twi_ch_percent, twi_volume,
									otc_ch_sign, otc_ch_pt, otc, otc_ch_sign, otc_ch_percent, otc_volume,
									electronic_ch_sign, electronic_ch_pt, electronic, electronic_ch_sign,
									electronic_ch_percent, electronic_volume,
									financial_ch_sign, financial_ch_pt, financial, financial_ch_sign,
									financial_ch_percent, financial_volume)
	print text.encode('utf-8').replace("<br>", "")

	# query mongodb to check whether this post existed or not, if not, save to database
	db_manager.save_tw_stock(file_time, title, text, twi_volume, otc_volume, electronic_volume, financial_volume)
	# produce info img
	process.tw_stock_img(target, file_time, twi, twi_ch_sign, twi_ch_pt, twi_ch_percent, twi_volume,
						otc, otc_ch_sign, otc_ch_pt, otc_volume,
						electronic, electronic_ch_sign, electronic_ch_pt, electronic_volume,
						financial, financial_ch_sign, financial_ch_pt, financial_volume)
	# output txt files and send to slack
	output.txt_files(articles_path, rss_path, target, file_time, title, text, last_pubDate)

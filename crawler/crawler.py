# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from slack.msg_sender import *
from pprint import pprint
from ConfigParser import SafeConfigParser
from checklog import log_save_check
import time
import datetime
import os


# get parameters in config file
config_parser = SafeConfigParser()
config_parser.read('config.txt')

# get user agent to crawler header
user_agent = config_parser.get('CRAWLER', 'USER-AGENT')
header = {'User-Agent': user_agent}

# get time of now
now_hour = datetime.datetime.now().strftime('%H')


def earthquake_crawler(total_url, detail_url):
	try:
		res = requests.get(total_url, verify=False, headers=header)
	except Exception as e:
		print "Get earthquake total page fail: " + str(e)
		crawl_page_error(total_url)
		exit()
	# print res.status_code
	if res.status_code != 200:
		crawl_page_error(total_url)
		exit()
	soup = BeautifulSoup(res.content, "html.parser")

	# get all urls in table
	data = []
	for link in soup.find_all('a', href=True):
		data.append(link['href'])
	# pprint(data)
	try:
		res = requests.get(detail_url + data[-2], verify=False, headers=header)
	# if there is a earthquake news exists
	except Exception as e:
		print "Get earthquake detail page fail: " + str(e)
		crawl_page_error(total_url)
		exit()
	# print res.status_code
	if res.status_code != 200:
		crawl_page_error(total_url)
		exit()
	soup = BeautifulSoup(res.content, "html.parser")

	# get all data
	data = []
	for td in soup.find_all('td', attrs={'align': "left"}):
		data.append(td.text.replace("\n", ""))
	# pprint(data)
	try:
		# save data which I need
		date = data[1]
		day = date[7:9]
		time = date[10:16]
		depth = data[7].replace(u"\u3000", "")
		scale = data[9].replace(u"\u3000", "")
		location = data[11].replace(" ", "")
		maxs = []
		for i in range(0, len(data)):
			if u"\u7d1a" in data[i]:
				maxs.append(data[i])
		area_max = "，".join(maxs).replace(" ", "")
		"""
		print date
		print day
		print time
		print depth
		print scale
		print location
		print area_max
		"""
	except Exception as e:
		error = "assign earthquake values has error:\n" + str(e)
		print error
		assign_values_error(error)

	# get image url to download
	try:
		img_url = [img['src'] for img in soup.findAll('img', {'id': "ctl03_ImgEarthquakeNo"})][0]
	# print "img_url in crawler.py: " + img_url
	except Exception as e:
		error = "assign earthquake img_url has error:\n" + str(e)
		print error
		assign_values_error(error)

	# download image from source
	"""
	import urllib
	try:
		urllib.urlretrieve(img_url, articles_path + target + "/last.gif")
	except Exception as e:
		error = "download earthquake image has error:\n" + str(e)
		print error
		assign_values_error(error)
	"""

	# return tuple
	return date, day, time, depth, scale, location, area_max, img_url


def gas_price_crawler(cpc_url, fpcc_url):
	# cpc crawler start
	try:
		res = requests.get(cpc_url, verify=False, headers=header)
	except Exception as e:
		print "Get cpc price page fail: " + str(e)
		crawl_page_error(cpc_url)
		exit()
	# print res.status_code
	if res.status_code != 200:
		crawl_page_error(cpc_url)
		exit()
	soup = BeautifulSoup(res.content, "html.parser")

	data = []
	try:
		# change another source
		# get update date
		for span in soup.find_all('dt'):
			data.append(span.text)
		cpc_update = data[1]
		# print "cpc_update: " + cpc_update.encode('utf-8')

		# get all gas prices
		data = []
		for strong in soup.find_all('strong'):
			data.append(strong.text)
		# pprint(data)
		cpc92 = data[2]
		cpc95 = data[3]
		cpc98 = data[4]
		cpc_diesel = data[6]

		# debug message
		"""
		print "cpc98: " + cpc98
		print "cpc95: " + cpc95
		print "cpc92: " + cpc92
		print "cpc_diesel: " + cpc_diesel
		"""

	except Exception as e:
		error = "assign cpc_price values has error:\n" + str(e)
		print error
		assign_values_error(error)
	# cpc price end

	# fpcc crawler start
	try:
		res = requests.get(fpcc_url, verify=False, headers=header)
	except Exception as e:
		print "Get fpcc price page fail: " + str(e)
		crawl_page_error(cpc_url)
		exit()
	# print res.status_code
	if res.status_code != 200:
		crawl_page_error(fpcc_url)
		exit()
	soup = BeautifulSoup(res.content, "html.parser")

	data = []
	try:
		# get update date
		for p in soup.find_all('p', attrs={'class': "effective_blue"}):
			data.append(p.text)
		# pprint(data)
		fpcc_update = data[0][5:-1].replace("\n", "")
		# print "fpcc_update: " + fpcc_update

		# get table's all data
		data = []
		for strong in soup.find_all('strong'):
			data.append(strong.text)
		# pprint(data)
		# price is here, the first is $, it should be removed
		fpcc92 = data[1][1:]
		fpcc95 = data[2][1:]
		fpcc98 = data[3][1:]
		fpcc_diesel = data[4][1:]
		# debug message
		"""
		print "fpcc98: " + fpcc98
		print "fpcc95: " + fpcc95
		print "fpcc92: " + fpcc92
		print "fpcc_diesel: " + fpcc_diesel
		"""
	except Exception as e:
		error = "assign fpcc_price values has error:\n" + str(e)
		print error
		assign_values_error(error)

	# return tuple
	return cpc_update, cpc98, cpc95, cpc92, cpc_diesel, fpcc_update, fpcc98, fpcc95, fpcc92, fpcc_diesel


def gas_predict_crawler(url):
	try:
		res = requests.get(url, verify=False, headers=header)
	except Exception as e:
		print "Get GoodLife page fail: " + str(e)
		crawl_page_error(url)
		exit()
	# print res.status_code
	if res.status_code != 200:
		crawl_page_error(url)
		exit()
	soup = BeautifulSoup(res.content, "html.parser")

	update_date = ""
	try:
		# get update date
		for p in soup.find_all('p', attrs={'class': "update"}):
			# print p.text
			update_date = p.text.rpartition('(')[0]
		# print update_date
	except Exception as e:
		error = "assign goodlife update date values has error:\n" + str(e)
		print error
		assign_values_error(error)

	data = []
	counter = 0
	try:
		for h2 in soup.find_all('h2'):
			# print str(counter) + ". " + h2.text
			counter += 1
			data.append(h2.text)
		change_str = data[2]
		# print change_str
	except Exception as e:
		error = "assign goodlife change string values has error:\n" + str(e)
		# try to fix issue about web page format changed
		change_str = data[1]
		print error
		assign_values_error(error)

	# test string
	# change_str = u'不調整'

	# print change_str

	# find out whether change_str is u'不調整' or u'漲跌XX'
	cht_counter = 0
	change_val = ""
	for cht in change_str.decode('utf-8'):
		# string u'不調整' doesn't have a number
		if not u'\u4e00' <= cht <= u'\u9fff':
			# print cht
			change_val += cht
			cht_counter += 1
	if cht_counter == 0:
		change_sign = change_str
	else:
		change_sign = change_str[1]
		change_val = change_val.strip()
	# debug message
	# print "GoodLife gas predict: " + change_sign + change_val + " on " + update_date

	# return tuple
	return update_date, change_sign, change_val


def tw_stock_crawler(logs_path, no_update_path, target, url):
	check_before_hour = config_parser.get('CRAWLER', 'TW_STOCK_CHECK_BEFORE_HOUR')
	if int(now_hour) < int(check_before_hour):
		cycle = 2
	else:
		cycle = 1

	open_check = config_parser.get('CRAWLER', 'TW_STOCK_OPEN_CHECK')
	if open_check == 'off':
		cycle = 1

	for cycle in range(cycle, 0, -1):
		try:
			res = requests.get(url, verify=False, headers=header)
		except Exception as e:
			print "Get tw_stock page fail: " + str(e)
			crawl_page_error(url)
			exit()
		# print res.status_code
		if res.status_code != 200:
			crawl_page_error(url)
			exit()
		soup = BeautifulSoup(res.content, "html.parser")

		data = []
		for span in soup.find_all('span'):
			# print span.text
			data.append(span.text)
		try:
			twi_ch_sign = data[2]
			twi_volume = data[3]
			otc_ch_sign = data[4]
			otc_volume = data[5]
			electronic_ch_sign = data[6]
			electronic_volume = data[7]
			financial_ch_sign = data[8]
			financial_volume = data[9]

			"""
			# debug message
			print "twi_ch_sign : " + twi_ch_sign
			print "twi_volume: " + twi_volume
			print "otc_ch_sign : " + otc_ch_sign
			print "otc_volume: " + otc_volume
			print "electronic_ch_sign: " + electronic_ch_sign
			print "electronic_volume: " + electronic_volume
			print "financial_ch_sign: " + financial_ch_sign
			print "financial_volume: " + financial_volume
			"""

			if open_check == 'on':
				log_save_check.tw_stock_today_open(now_hour, check_before_hour, logs_path, no_update_path, target,
													cycle, twi_volume, otc_volume, electronic_volume, financial_volume)

			if cycle == 2:
				print "crawler will check the 2nd round after 1 min..."
				time.sleep(60)

		except Exception as e:
			error = "assign change sign and volume values has error:\n" + str(e)
			print error
			assign_values_error(error)

	data = []
	for td in soup.find_all('td', attrs={'class': "dx"}):
		# print td.text
		data.append(td.text)
	try:
		twi = data[0]
		otc = data[1]
		electronic = data[2]
		financial = data[3]

		"""
		# debug message
		print "twi: " + twi
		print "otc: " + otc
		print "electronic: " + electronic
		print "financial: " + financial
		"""

	except Exception as e:
		error = "assign index values has error:\n" + str(e)
		print error
		assign_values_error(error)

	data = []
	counter = 0
	for td in soup.find_all('td'):
		log = str(counter) + ": " + td.text + "\n"

		# fix CI issue
		"""
		with open(logs_path + target + no_update_path + "td.text_logs.txt", "a") as text_file:
			text_file.write("%s" % log)
		"""

		data.append(td.text)
		counter += 1

	# delete log
	if os.path.isfile(logs_path + target + no_update_path + "td.text_logs.txt"):
		os.remove(logs_path + target + no_update_path + "td.text_logs.txt")

	try:
		twi_ch_pt = data[28]
		otc_ch_pt = data[32]
		electronic_ch_pt = data[36]
		financial_ch_pt = data[40]

		"""
		# debug message
		print "twi_ch_pt: " + twi_ch_pt
		print "otc_ch_pt: " + otc_ch_pt
		print "electronic_ch_pt: " + electronic_ch_pt
		print "financial_ch_pt: " + financial_ch_pt
		"""

	except Exception as e:
		error = "assign index change point values has error:\n" + str(e)
		print error
		assign_values_error(error)

	return twi, twi_ch_sign, twi_ch_pt, twi_volume, otc, otc_ch_sign, otc_ch_pt, otc_volume, electronic, \
			electronic_ch_sign, electronic_ch_pt, electronic_volume, financial, financial_ch_sign, \
			financial_ch_pt, financial_volume

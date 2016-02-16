# -*- coding: utf-8 -*-
import sys
import os
import pytest
from pprint import pprint
from ConfigParser import SafeConfigParser
from crawler.crawler import tw_stock_crawler


# set encoding to utf-8, then we can input traditional and simplified Chinese
if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')

if not os.path.isfile("config.txt"):
	print "config.txt does not exist, exit!"
	exit()

# get parameters in config file
config_parser = SafeConfigParser()
config_parser.read('config.txt')

logs_path = config_parser.get('FOLDER_PATH', 'LOGS_PATH')
no_update_path = config_parser.get('FOLDER_PATH', 'NO_UPDATE_PATH')
target = 'tw_stock'
url = config_parser.get('URL', 'TW_STOCK')

"""
# return tuple order
return twi, twi_ch_sign, twi_ch_pt, twi_volume, otc, otc_ch_sign, otc_ch_pt, otc_volume, electronic, \
		electronic_ch_sign, electronic_ch_pt, electronic_volume, financial, financial_ch_sign, \
		financial_ch_pt, financial_volume
"""


class Test_Tw_Stock_Crawler(object):

	@pytest.fixture
	def crawler(self):
		crawler = tw_stock_crawler(logs_path, no_update_path, target, url)
		return crawler

	def test_twi(self, crawler):
		twi = crawler[0]
		print ": " + twi
		assert float(twi)

	def test_twi_ch_sign(self, crawler):
		twi_ch_sign = crawler[1]
		print ": " + twi_ch_sign
		assert twi_ch_sign == u'up' or twi_ch_sign == u'down'

	def test_twi_ch_pt(self, crawler):
		twi_ch_pt = crawler[2]
		print ": " + twi_ch_pt
		assert float(twi_ch_pt)

	def test_twi_volume(self, crawler):
		twi_volume = crawler[3]
		print ": " + twi_volume
		assert float(twi_volume[:-1])

	def test_otc(self, crawler):
		otc = crawler[4]
		print ": " + otc
		assert float(otc)

	def test_otc_ch_sign(self, crawler):
		otc_ch_sign = crawler[5]
		print ": " + otc_ch_sign
		assert otc_ch_sign == u'漲' or otc_ch_sign == u'跌'

	def test_otc_ch_pt(self, crawler):
		otc_ch_pt = crawler[6]
		print ": " + otc_ch_pt
		assert float(otc_ch_pt)

	def test_otc_volume(self, crawler):
		otc_volume = crawler[7]
		print ": " + otc_volume
		assert float(otc_volume[:-1])

	def test_electronic(self, crawler):
		electronic = crawler[8]
		print ": " + electronic
		assert float(electronic)

	def test_electronic_ch_sign(self, crawler):
		electronic_ch_sign = crawler[9]
		print ": " + electronic_ch_sign
		assert electronic_ch_sign == u'up' or electronic_ch_sign == u'down'

	def test_electronic_ch_pt(self, crawler):
		electronic_ch_pt = crawler[10]
		print ": " + electronic_ch_pt
		assert float(electronic_ch_pt)

	def test_electronic_volume(self, crawler):
		electronic_volume = crawler[11]
		print ": " + electronic_volume
		assert float(electronic_volume[:-1])

	def test_financial(self, crawler):
		financial = crawler[12]
		print ": " + financial
		assert float(financial)

	def test_financial_ch_sign(self, crawler):
		financial_ch_sign = crawler[13]
		print ": " + financial_ch_sign
		assert financial_ch_sign == u'up' or financial_ch_sign == u'down'

	def test_financial_ch_pt(self, crawler):
		financial_ch_pt = crawler[14]
		print ": " + financial_ch_pt
		assert float(financial_ch_pt)

	def test_financial_volume(self, crawler):
		financial_volume = crawler[15]
		print ": " + financial_volume
		assert float(financial_volume[:-1])

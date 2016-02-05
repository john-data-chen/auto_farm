# -*- coding: utf-8 -*-
import sys
import os
import pytest
from pprint import pprint
from ConfigParser import SafeConfigParser
from crawler.crawler import gas_price_crawler


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

# real URL
cpc_url = config_parser.get('URL', 'CPC_PRICE')
fpcc_url = config_parser.get('URL', 'FPCC_PRICE')

"""
# return tuple order
cpc_update, cpc98, cpc95, cpc92, cpc_diesel, fpcc_update, fpcc98, fpcc95, fpcc92, fpcc_diesel
"""


class Test_Gas_Price_Crawler(object):

	@pytest.fixture
	def crawler(self):
		crawler = gas_price_crawler(cpc_url, fpcc_url)
		return crawler

	def test_cpc98(self, crawler):
		cpc98 = crawler[1]
		print ": " + cpc98
		assert float(cpc98)

	def test_cpc95(self, crawler):
		cpc95 = crawler[2]
		print ": " + cpc95
		assert float(cpc95)

	def test_cpc92(self, crawler):
		cpc92 = crawler[3]
		print ": " + cpc92
		assert float(cpc92)

	def test_cpc_diesel(self, crawler):
		cpc_diesel = crawler[4]
		print ": " + cpc_diesel
		assert float(cpc_diesel)

	def test_cpc_price_order(self,crawler):
		cpc98 = float(crawler[1])
		cpc95 = float(crawler[2])
		cpc92 = float(crawler[3])
		cpc_diesel = float(crawler[4])
		assert cpc98 > cpc95 > cpc92 > cpc_diesel, "cpc prices order is not correct"

	def test_fpcc98(self, crawler):
		fpcc98 = crawler[6]
		print ": " + fpcc98
		assert float(fpcc98)

	def test_fpcc95(self, crawler):
		fpcc95 = crawler[7]
		print ": " + fpcc95
		assert float(fpcc95)

	def test_fpcc92(self, crawler):
		fpcc92 = crawler[8]
		print ": " + fpcc92
		assert float(fpcc92)

	def test_fpcc_diesel(self, crawler):
		fpcc_diesel = crawler[9]
		print ": " + fpcc_diesel
		assert float(fpcc_diesel)

	def test_fpcc_prices_order(self,crawler):
		fpcc98 = float(crawler[6])
		fpcc95 = float(crawler[7])
		fpcc92 = float(crawler[8])
		fpcc_diesel = float(crawler[9])
		assert fpcc98 > fpcc95 > fpcc92 > fpcc_diesel, "fppc prices order is not correct"

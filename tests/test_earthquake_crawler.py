# -*- coding: utf-8 -*-
import sys
import os
import pytest
from pprint import pprint
from ConfigParser import SafeConfigParser
from crawler.crawler import earthquake_crawler


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

total_url = config_parser.get('TEST_URL', 'EARTHQUAKE_TOTAL')
detail_url = config_parser.get('URL', 'EARTHQUAKE_DETAIL')

"""
# return tuple
return date, day, time, depth, scale, location, area_max, img_url
"""


class Test_Earthquake_Crawler(object):

	@pytest.fixture
	def crawler(self):
		crawler = earthquake_crawler(total_url, detail_url)
		return crawler

	def test_date(self, crawler):
		date = crawler[0]
		print ": " + date
		assert date == u'104年 2月27日 0時50分 3.4秒'

	def test_day(self, crawler):
		day = crawler[1]
		print ": " + day
		assert day == u'27'

	def test_time(self, crawler):
		time = crawler[2]
		print ": " + time
		assert time == u' 0時50分'

	def test_depth(self, crawler):
		depth = crawler[3]
		print ": " + depth
		assert depth == u'97.6公里'

	def test_scale(self, crawler):
		scale = crawler[4]
		print ": " + scale
		assert scale == u'5.3'

	def test_location(self, crawler):
		location = crawler[5]
		print ": " + location
		assert location == u'宜蘭縣政府東方55.0公里(位於臺灣東部海域)'

	def test_area_max(self, crawler):
		area_max = crawler[6]
		print ": " + area_max
		assert area_max == u'宜蘭縣地區最大震度3級，花蓮縣地區最大震度3級，新北市地區最大震度2級，桃園縣地區最大震度2級，' \
		u'南投縣地區最大震度2級，臺中市地區最大震度2級，苗栗縣地區最大震度2級，臺北市地區最大震度1級，新竹縣地區最大震度1級，' \
		u'新竹市地區最大震度1級，臺東縣地區最大震度1級，彰化縣地區最大震度1級，雲林縣地區最大震度1級，嘉義市地區最大震度1級'

	def test_img_url(self, crawler):
		img_url = crawler[7]
		print ": " + img_url
		assert img_url == u'http://scweb.cwb.gov.tw/webdata/OLDEQ/201502/2015022700500353012.gif'

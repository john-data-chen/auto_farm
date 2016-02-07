# -*- coding: utf-8 -*-
import argparse
from ConfigParser import SafeConfigParser
from checklog.auto_check import *
from crawler.crawler import *
from editor.editor import *
from tts.tts import *
from info_img import img_copyer


# set encoding to utf-8, then we can input traditional and simplified Chinese
if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')

if not os.path.isfile("config.txt"):
	print "config.txt does not exist, exit!"
	exit()

# get args from command line
args_parser = argparse.ArgumentParser()
args_parser.add_argument("target", type=str, help="which target you want to crawl",
                         choices=["earthquake", "gas_predict", "gas_price", "tw_stock"])
args = args_parser.parse_args()
target = args.target
# error handle if no input args
if target is None:
	print "wrong args, for example, you should input: python jarvis.py earthquake"
	exit()

# get parameters in config file
config_parser = SafeConfigParser()
config_parser.read('config.txt')

# load configs
logs_path = config_parser.get('FOLDER_PATH', 'LOGS_PATH')
no_update_path = config_parser.get('FOLDER_PATH', 'NO_UPDATE_PATH')
articles_path = config_parser.get('FOLDER_PATH', 'ARTICLES_PATH')
templates_path = config_parser.get('FOLDER_PATH', 'TEMPLATES_PATH')
rss_path = config_parser.get('FOLDER_PATH', 'RSS_PATH')
tts_mp3_path = config_parser.get('FOLDER_PATH', 'TTS_MP3_PATH')
info_img_path = config_parser.get('FOLDER_PATH', 'INFO_IMG_PATH')
max_logs = config_parser.getint('LOG', 'MAX_LOGS')
max_old_articles = config_parser.getint('LOG', 'MAX_OLD_ARTICLES')
max_mp3 = config_parser.getint('LOG', 'MAX_MP3')
max_info_img = config_parser.getint('LOG', 'MAX_INFO_IMG')
targets_with_img = config_parser.get('TARGET_TYPE', 'TARGETS_WITH_IMG').split(", ")

# auto check and clean
check_folders(logs_path, no_update_path, articles_path, rss_path, tts_mp3_path, info_img_path, target)
clean_logs(logs_path, target, no_update_path, max_logs)
clean_articles(articles_path, target, max_old_articles)
clean_mp3(tts_mp3_path, target, max_mp3)
check_template(templates_path, target)

# load configs based target
# target without info img
if target == 'earthquake':
	total_url = config_parser.get('URL', 'EARTHQUAKE_TOTAL')
	detail_url = config_parser.get('URL', 'EARTHQUAKE_DETAIL')
	earthquake_editor(
			earthquake_crawler(total_url, detail_url),
			logs_path, target, no_update_path, articles_path, templates_path, rss_path)

if target in targets_with_img:
	# clean old img at first
	clean_info_img(info_img_path, target, max_info_img)
	if target == 'gas_price':
		"""
		# test url, only for test
		cpc_url = config_parser.get('TEST_URL', 'CPC_PRICE')
		fpcc_url = config_parser.get('TEST_URL', 'FPCC_PRICE')
		"""
		# real url
		cpc_url = config_parser.get('URL', 'CPC_PRICE')
		fpcc_url = config_parser.get('URL', 'FPCC_PRICE')

		gas_price_editor(
				gas_price_crawler(cpc_url, fpcc_url),
				logs_path, target, no_update_path, articles_path, templates_path, rss_path)

	elif target == 'gas_predict':
		url = config_parser.get('URL', 'GAS_PREDICT')
		gas_predict_editor(
				gas_predict_crawler(url),
				logs_path, target, no_update_path, articles_path, templates_path, rss_path)

	elif target == 'tw_stock':
		url = config_parser.get('URL', 'TW_STOCK')
		tw_stock_editor(
				tw_stock_crawler(logs_path, no_update_path, target, url),
				logs_path, target, no_update_path, articles_path, templates_path, rss_path)

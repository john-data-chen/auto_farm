import requests
from ConfigParser import SafeConfigParser


# get parameters in config file
config_parser = SafeConfigParser()
config_parser.read('./config.txt')

# channels
# error warning only
rd_team = config_parser.get('SLACK', 'RD_TEAM')
# test channel in EBC-TV
crawler = config_parser.get('SLACK', 'CRAWLER')
# test channel in EBC
ebcinsight_cart = config_parser.get('SLACK', 'EBCINSIGHT-CART')
# formal channel in EBC
ebc_robot = config_parser.get('SLACK', 'EBC_ROBOT')
ebc_important_info = config_parser.get('SLACK', 'EBC_IMPORTANT_INFO')
# formal channel for PM
ebc_pm = config_parser.get('SLACK', 'EBC_PM')
# test channel for PM
ebc_pm_test = config_parser.get('SLACK', 'EBC_PM_TEST')


def temp_missing(temp_name):
	slack_webhook = rd_team
	payload = {"text": "template " + temp_name + ".json does not exist, exit!"}
	requests.post(slack_webhook, json=payload)
	exit()


def crawl_page_error(url):
	slack_webhook = rd_team
	payload = {"text": "crawl page: " + url + " failed, exit!"}
	requests.post(slack_webhook, json=payload)
	exit()


def assign_values_error(error):
	slack_webhook = rd_team
	payload = {"text": "assign values has exception: " + error}
	requests.post(slack_webhook, json=payload)
	exit()


def get_tts_error(error):
	slack_webhook = rd_team
	payload = {"text": error}
	requests.post(slack_webhook, json=payload)
	exit()


def send_crawler(news):
	slack_webhook = crawler
	payload = {"text": news}
	requests.post(slack_webhook, json=payload)


def send_ebcinsight_cart(news):
	slack_webhook = ebcinsight_cart
	payload = {"text": news}
	requests.post(slack_webhook, json=payload)


def send_ebc_robot(news):
	slack_webhook = ebc_robot
	payload = {"text": news}
	requests.post(slack_webhook, json=payload)


def send_ebc_important_info(news):
	slack_webhook = ebc_important_info
	payload = {"text": news}
	requests.post(slack_webhook, json=payload)


def send_ebc_pm(news):
	slack_webhook = ebc_pm
	payload = {"text": news}
	requests.post(slack_webhook, json=payload)


def send_ebc_pm_test(news):
	slack_webhook = ebc_pm_test
	payload = {"text": news}
	requests.post(slack_webhook, json=payload)

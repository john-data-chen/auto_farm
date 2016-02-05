import requests
from ConfigParser import SafeConfigParser


# get parameters in config file
config_parser = SafeConfigParser()
config_parser.read('./config.txt')

# channels
# error warning and testing
crawler_test = config_parser.get('SLACK', 'CRAWLER_TEST')
# formal release channel
auto_farm = config_parser.get('SLACK', 'AUTO_FARM')


def temp_missing(temp_name):
	slack_webhook = crawler_test
	payload = {"text": "template " + temp_name + ".json does not exist, exit!"}
	requests.post(slack_webhook, json=payload)
	exit()


def crawl_page_error(url):
	slack_webhook = crawler_test
	payload = {"text": "crawl page: " + url + " failed, exit!"}
	requests.post(slack_webhook, json=payload)
	exit()


def assign_values_error(error):
	slack_webhook = crawler_test
	payload = {"text": "assign values has exception: " + error}
	requests.post(slack_webhook, json=payload)
	exit()


def get_tts_error(error):
	slack_webhook = crawler_test
	payload = {"text": error}
	requests.post(slack_webhook, json=payload)
	exit()


def send_crawler_test(news):
	slack_webhook = crawler_test
	payload = {"text": news}
	requests.post(slack_webhook, json=payload)


def send_auto_farm(news):
	slack_webhook = auto_farm
	payload = {"text": news}
	requests.post(slack_webhook, json=payload)

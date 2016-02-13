from slack import channel_selector
import os
from ConfigParser import SafeConfigParser
import random


# get parameters in config file
config_parser = SafeConfigParser()
config_parser.read('config.txt')
targets_with_img = config_parser.get('TARGET_TYPE', 'TARGETS_WITH_IMG').split(", ")


def txt_files(articles_path, target, file_time, title, text, last_pubDate):
	# output news
	# record time
	with open(articles_path + target + "/" + file_time + "_" + target + ".txt", "w") as text_file:
		text_file.write("%s" % title + "\n" + text)

	print ""
	print "output " + target + " news is done"

	# load configs based target
	# targets without info img
	if target == "earthquake":
		earthquake_logo = config_parser.get('RSS', 'EARTHQUAKE_LOGO')
		with open(articles_path + target + "/img_url.txt", "r") as data:
			img_url = data.read()
		text_to_slack = earthquake_logo + "\n" + title + "\n" + text.replace("<br>", "") + "\n" + img_url

	if target in targets_with_img:
		# detect which folder
		random_int = random.sample(range(100000), 1)
		text_to_slack = target + "/last_" + target + ".jpg" + "?" + str(random_int[0]) + "\n" + \
						title + "\n" + text.replace("<br>", "")

	# choose which slack channel to send
	channel_selector.select(target, text_to_slack)

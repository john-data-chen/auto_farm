import os
from msg_sender import *
from ConfigParser import SafeConfigParser


# get parameters in config file
config_parser = SafeConfigParser()
config_parser.read('./config.txt')
targets_online = config_parser.get('PM_VERIFIED_PASS', 'TARGETS_ONLINE').split(", ")
pass_to_formal_channel = config_parser.get('PM_VERIFIED_PASS', 'PASS_TO_FORMAL_CHANNEL').split(", ")


def select(target, text_to_slack):
	# detect which folder
	if os.getcwd() == "/home/charlie/public_html/production/Jarvis_alpha":
		# after PM verified result is Pass, then send to formal channels
		if target in targets_online:
			if target in pass_to_formal_channel:
				send_ebc_robot(text_to_slack)
				send_ebc_important_info(text_to_slack)
				send_ebc_pm(text_to_slack)
			else:
				send_ebcinsight_cart(text_to_slack)
		else:
			# send to test channels
			send_ebcinsight_cart(text_to_slack)
			send_ebc_pm_test(text_to_slack)
	else:
		# send to test channel: crawler
		send_crawler(text_to_slack)

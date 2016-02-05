from msg_sender import *
from ConfigParser import SafeConfigParser


# get parameters in config file
config_parser = SafeConfigParser()
config_parser.read('./config.txt')
targets_online = config_parser.get('PM_VERIFIED_PASS', 'TARGETS_ONLINE').split(", ")
pass_to_formal_channel = config_parser.get('PM_VERIFIED_PASS', 'PASS_TO_FORMAL_CHANNEL').split(", ")


def select(target, text_to_slack):
	# after PM verified result is Pass, then send to formal channels
	if target in targets_online:
		if target in pass_to_formal_channel:
			send_auto_farm(text_to_slack)
		else:
			send_crawler_test(text_to_slack)
	else:
		# send to test channel
		send_crawler_test(text_to_slack)

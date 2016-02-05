# -*- coding: utf-8 -*-
import sys
import os
from info_img.process import *
import json


# set encoding to utf-8, then we can input traditional and simplified Chinese
if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')


def last_date(logs_path, target, no_update_path, file_time, log):
	# check with old txt
	if os.path.isfile(logs_path + target + "/last_date.txt"):
		with open(logs_path + target + "/last_date.txt", "r") as data:
			last_date = data.read()
			# check two result is the same, if they are, no need write again
			if last_date == log:
				print "there is no update, exit..."
				with open(logs_path + target + no_update_path + file_time + ".txt", "w") as text_file:
					text_file.write("%s" % log)
				exit()

	# save date to txt, it will be checked next time
	with open(logs_path + target + "/last_date.txt", "w") as text_file:
		text_file.write("%s" % log)


def gas_price_dates(logs_path, target, no_update_path, file_time, cpc_date, fpcc_date):
	# check with fpcc log
	if os.path.isfile(logs_path + target + "/last_fpcc_date.txt"):
		with open(logs_path + target + "/last_fpcc_date.txt", "r") as data:
			fpcc_last_date = data.read()
		# check with cpc log
		if os.path.isfile(logs_path + target + "/last_cpc_date.txt"):
			with open(logs_path + target + "/last_cpc_date.txt", "r") as data:
				cpc_last_date = data.read()
			# check two results are different, if they are, then send slack
			if fpcc_last_date != fpcc_date and cpc_last_date != cpc_date:
				print "cpc and fpcc dates are updated, Jarvis will send to slack"
			else:
				if fpcc_last_date == fpcc_date:
					print "fpcc date is not updated"
					with open(logs_path + target + no_update_path + file_time + "_fppc.txt", "w") as text_file:
						text_file.write("%s" % cpc_date)
				elif cpc_last_date == cpc_date:
					print "cpc date is not updated"
					with open(logs_path + target + no_update_path + file_time + "_cpc.txt", "w") as text_file:
						text_file.write("%s" % cpc_date)
				exit()

	# save date to txt, it will be checked next time
	with open(logs_path + target + "/last_fpcc_date.txt", "w") as text_file:
		text_file.write("%s" % fpcc_date)
	with open(logs_path + target + "/last_cpc_date.txt", "w") as text_file:
		text_file.write("%s" % cpc_date)


def previous_gas_price(logs_path, target, file_time, cpc92, cpc95, cpc98, cpc_diesel, fpcc92, fpcc95, fpcc98, fpcc_diesel):
	# check with previous cpc92 exists
	if os.path.isfile(logs_path + target + "/previous_cpc92.txt"):
		with open(logs_path + target + "/previous_cpc92.txt", "r") as data:
			previous_cpc92 = data.read()
			# print previous_cpc92
			change_val = float(cpc92) - float(previous_cpc92)
			if change_val == 0:
				change_sign = "even"
			elif change_val > 0:
				change_sign = "up"
			else:
				change_sign = "down"
			change_val = str(abs(change_val))
			gas_price_img(target, file_time, change_sign, change_val, cpc92, cpc95, cpc98, cpc_diesel, fpcc92,
							fpcc95, fpcc98, fpcc_diesel)
	else:
		print logs_path + target + "/previous_cpc92.txt is missing"

	# save cpc92, check it in next round to get change
	with open(logs_path + target + "/previous_cpc92.txt", "w") as text_file:
		text_file.write("%s" % cpc92)


def tw_stock_today_open(now_hour, check_before_hour, logs_path, no_update_path , target, cycle, twi_volume,
							otc_volume, electronic_volume, financial_volume):
	# debug message
	# print cycle, twi_volume, otc_volume, electronic_volume, financial_volume

	# check now is before or after market close
	if int(now_hour) < int(check_before_hour):
		if cycle == 2:
			dic = {"twi_volume": twi_volume, "otc_volume": otc_volume, "electronic_volume": electronic_volume,
					"financial_volume": financial_volume}
			with open(logs_path + target + no_update_path + "1st_volumes.json", "w") as js_file:
				json.dump(dic, js_file)
		elif cycle == 1:
			print "now_hour = " + now_hour + ", market should be open now"
			if os.path.isfile(logs_path + target + no_update_path + "1st_volumes.json"):
				with open(logs_path + target + no_update_path + "1st_volumes.json") as js_file:
					volumes_in_js = json.load(js_file, encoding='utf-8')
				if twi_volume == volumes_in_js["twi_volume"] and otc_volume == volumes_in_js["otc_volume"] and \
					electronic_volume == volumes_in_js["electronic_volume"] and \
					financial_volume == volumes_in_js["financial_volume"]:
					market_status = "market is not open today."
					with open(logs_path + target + no_update_path + "market status.txt", "w") as text_file :
						text_file.write("%s" % market_status)
					print market_status
					exit()
				else:
					market_status = "market is open today."
					with open(logs_path + target + no_update_path + "market status.txt", "w") as text_file :
						text_file.write("%s" % market_status)
					print market_status
					exit()
			else:
				print logs_path + target + no_update_path + "1st_volumes.json is missing, exit..."
				exit()
		# error handle when cycle value is not correct
		else:
			print "cycle is not correct: " + cycle
			exit()
	# if now_hour >= check_before_hour, market should be close now
	else:
		print "now_hour = " + now_hour + ", market should be close now"
		if os.path.isfile(logs_path + target + no_update_path + "market status.txt"):
			with open(logs_path + target + no_update_path + "market status.txt", "r") as data:
				market_status = data.read()
			if market_status == "market is not open today.":
				print market_status
				exit()

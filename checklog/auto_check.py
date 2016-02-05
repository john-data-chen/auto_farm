import os
import shutil
from slack.msg_sender import *
from ConfigParser import SafeConfigParser


def check_folders(logs_path, no_update_path, articles_path, rss_path, tts_mp3_path, info_img_path, insight_news_rss_path,
					folder_name):
	# check log's folders
	if not os.path.exists(logs_path):
		os.mkdir(logs_path)
	if not os.path.exists(logs_path + folder_name):
		os.mkdir(logs_path + folder_name)
	if not os.path.exists(logs_path + folder_name + no_update_path):
		os.mkdir(logs_path + folder_name + no_update_path)
	# check article's folders
	if not os.path.exists(articles_path):
		os.mkdir(articles_path)
	if not os.path.exists(articles_path + folder_name):
		os.mkdir(articles_path + folder_name)
	# check rss' folders
	if not os.path.exists(rss_path):
		os.mkdir(rss_path)
	if not os.path.exists(rss_path + folder_name):
		os.mkdir(rss_path + folder_name)
	# check TTS mp3's folder
	if not os.path.exists(tts_mp3_path):
		os.mkdir(tts_mp3_path)
	if not os.path.exists(tts_mp3_path + folder_name):
		os.mkdir(tts_mp3_path + folder_name)
	# check info_img's folder
	targets_with_img = config_parser.get('TARGET_TYPE', 'TARGETS_WITH_IMG').split(", ")
	if folder_name in targets_with_img:
		if not os.path.exists(info_img_path):
			os.mkdir(info_img_path)
		if not os.path.exists(info_img_path + folder_name):
			os.mkdir(info_img_path + folder_name)
		if not os.path.exists(insight_news_rss_path):
			os.mkdir(insight_news_rss_path)
		if not os.path.exists(insight_news_rss_path + folder_name):
			os.mkdir(insight_news_rss_path + folder_name)


def clean_logs(logs_path, folder_name, no_update_path, max_logs):
	old_files = len([name for name in os.listdir(logs_path + folder_name + no_update_path) if os.path.isfile
	(os.path.join(logs_path + folder_name + no_update_path, name))])

	if old_files >= max_logs:
		# delete folder
		shutil.rmtree(logs_path + folder_name + no_update_path)
		# re-create folder
		os.mkdir(logs_path + folder_name + no_update_path)


def clean_articles(articles_path, folder_name, max_old_articles):
	old_files = len([name for name in os.listdir(articles_path + folder_name) if os.path.isfile
	(os.path.join(articles_path + folder_name, name))])

	if old_files >= max_old_articles:
		# delete folder
		shutil.rmtree(articles_path + folder_name)
		# re-create folder
		os.mkdir(articles_path + folder_name)


def clean_mp3(tts_mp3_path, folder_name, max_mp3):
	old_files = len([name for name in os.listdir(tts_mp3_path + folder_name) if os.path.isfile
	(os.path.join(tts_mp3_path + folder_name, name))])

	if old_files >= max_mp3:
		# delete folder
		shutil.rmtree(tts_mp3_path + folder_name)
		# re-create folder
		os.mkdir(tts_mp3_path + folder_name)


def clean_info_img(info_img_path, folder_name, max_info_img):
	old_files = len([name for name in os.listdir(info_img_path + folder_name) if os.path.isfile
	(os.path.join(info_img_path + folder_name, name))])

	if old_files >= max_info_img:
		# delete folder
		shutil.rmtree(info_img_path + folder_name)
		# re-create folder
		os.mkdir(info_img_path + folder_name)


def check_template(templates_path, temp_name):
	if not os.path.isfile(templates_path + temp_name + "_title.json"):
		print "template " + temp_name + "_title.json does not exist, exit!"
		temp_missing(temp_name)
		exit()
	if not os.path.isfile(templates_path + temp_name + "_text.json"):
		print "template " + temp_name + "_text.json does not exist, exit!"
		temp_missing(temp_name)
		exit()
	pass

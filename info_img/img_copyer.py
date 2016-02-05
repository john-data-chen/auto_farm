import os
import shutil


# display current path
# print os.getcwd()


def copy(info_img_path, rss_path, insight_news_rss_path, target):
	if not os.path.isfile(info_img_path + target + "/last_" + target + ".jpg"):
		print info_img_path + target + "/last_" + target + ".jpg" + " is missing..."
	else:
		shutil.copyfile(info_img_path + target + "/last_" + target + ".jpg",
					rss_path + target + "/last_" + target + ".jpg")
		shutil.copyfile(rss_path + target + "/last_" + target + ".jpg",
					insight_news_rss_path + target + "/last_" + target + ".jpg")
		print "copy " + rss_path + target + "/last_" + target + ".jpg" + " is done."

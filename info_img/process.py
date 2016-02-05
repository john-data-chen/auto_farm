# -*- coding: utf-8
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from ConfigParser import SafeConfigParser


# display current path
# print os.getcwd()

# get parameters in config file
config_parser = SafeConfigParser()
config_parser.read('config.txt')
img_assets_path = config_parser.get('FOLDER_PATH', 'IMG_ASSETS_PATH')
info_img_path = config_parser.get('FOLDER_PATH', 'INFO_IMG_PATH')

# font file path
adobe_font_path = "/AdobeFanHeitiStd-Bold.otf"
arial_font_path = "/ARIALUNI.TTF"


def gas_price_img(target, file_time, change_sign, change_val, cpc92, cpc95, cpc98, cpc_diesel, fpcc92, fpcc95, fpcc98,
                  fpcc_diesel):
    row1 = 108
    row2 = 164
    row3 = 223
    row4 = 283
    col_L = 155
    col_R = 428
    debug_message_title = "[" + target + " img creator]"

    # Load background Img,font
    try:
        im = Image.open(img_assets_path + target + "/" + target + "_back.jpg")
        font = ImageFont.truetype(img_assets_path + target + arial_font_path, 30)
        font_sign = ImageFont.truetype(img_assets_path + target + arial_font_path, 40)
        sign_up = Image.open(img_assets_path + target + "/" + target + "_up.png")
        sign_down = Image.open(img_assets_path + target + "/" + target + "_down.png")
    except IOError as e:
        print debug_message_title, "load assets Error:".format(e.errno, e.strerror)
        # print debug_message_title, "Background IMG loaded !"

    # Set draw
    try:
        draw = ImageDraw.Draw(im)
    except Exception as e:
        print e
    # Load and draw gas price changes
    # print debug_message_title + " Gas price :", change_sign
    if change_sign != "even":
        if change_sign == "up":
            sign = sign_up
            draw.ink = 236 + 42 * 256 + 26 * 256 * 256
        else:
            sign = sign_down
            draw.ink = 44 + 139 * 256 + 11 * 256 * 256
        sign.resize((25, 28), Image.BILINEAR)
        im.paste(sign, (279, 78), sign)
        draw.text((308, 62), change_val, font=font_sign)
    else:
        pass

    # Draw gas prices
    draw.ink = 255 + 255 * 256 + 255 * 256 * 256
    draw.text((col_L, row1), cpc92, font=font)
    draw.text((col_R, row1), fpcc92, font=font)
    draw.text((col_L, row2), cpc95, font=font)
    draw.text((col_R, row2), fpcc95, font=font)
    draw.text((col_L, row3), cpc98, font=font)
    draw.text((col_R, row3), fpcc98, font=font)
    draw.text((col_L, row4), cpc_diesel, font=font)
    draw.text((col_R, row4), fpcc_diesel, font=font)
    # print MESSAGE_TITLE, "draw gas prices is done"

    # Img save
    try:
        im.save(info_img_path + target + "/" + file_time + "_" + target + ".jpg", "JPEG", quality=100)
        im.save(info_img_path + target + "/last_" + target + ".jpg", "JPEG", quality=100)
    except IOError as e:
        print debug_message_title, "Save IMG Error:".format(e.errno, e.strerror)
    else:
        print debug_message_title, "IMG save to " + info_img_path + target


def gas_predict_img(target, file_time, change_sign, change_val):
	debug_message_title = "[" + target + " img creator]"

	# Load background Img,font
	try:
		im = Image.open(img_assets_path + target + "/" + target + "_back.jpg")
		font = ImageFont.truetype(img_assets_path + target + arial_font_path, 125)
		sign_up = Image.open(img_assets_path + target + "/" + target + "_up.png")
		sign_down = Image.open(img_assets_path + target + "/" + target + "_down.png")
		no_adjust_str = Image.open(img_assets_path + target + "/" + target + "_no_adjust_str.png")
		red_face = Image.open(img_assets_path + target + "/" + target + "_red_face.png")
		green_face = Image.open(img_assets_path + target + "/" + target + "_green_face.png")
		yellow_face = Image.open(img_assets_path + target + "/" + target + "_yellow_face.png")
	except IOError as e:
		print debug_message_title, "load assets Error:".format(e.errno, e.strerror)
	# print debug_message_title, "Background IMG loaded !"

	# Set draw
	try:
		draw = ImageDraw.Draw(im)
	except Exception as e:
		print e

	# debug message
	# change_sign = u"漲"
	# change_sign = u"降"
	# change_sign = u"不調整"
	# change_val = u''

	# assign a temp value to avoid an issue of override value
	price_change = sign_down
	face = green_face
	if change_sign == u"不調整":
		price_change = no_adjust_str
		face = yellow_face
	elif change_sign == u"漲":
		price_change = sign_up
		# R + G * 256 + B * 256 * 256
		draw.ink = 245 + 28 * 256 + 36 * 256 * 256
		face = red_face
	elif change_sign == u"降":
		price_change = sign_down
		draw.ink = 81 + 238 * 256 + 47 * 256 * 256
		face = green_face
	else:
		print "change_sign: " + change_sign + " is incorrect!"
		pass
	price_change.resize((25, 28), Image.BILINEAR)
	face.resize((25, 28), Image.BILINEAR)
	# (x, y)
	im.paste(price_change, (272, 175), price_change)
	im.paste(face, (110, 150), face)
	draw.text((370, 130), change_val, font=font)

	# Img save
	try:
		im.save(info_img_path + target + "/" + file_time + "_" + target + ".jpg", "JPEG", quality=100)
		im.save(info_img_path + target + "/last_" + target + ".jpg", "JPEG", quality=100)
	except IOError as e:
		print debug_message_title, "Save IMG Error:".format(e.errno, e.strerror)
	else:
		print debug_message_title, "IMG save to " + info_img_path + target


def tw_stock_img(target, file_time, twi, twi_ch_sign, twi_ch_pt, twi_ch_percent, twi_volume,
						otc, otc_ch_sign, otc_ch_pt, otc_volume,
						electronic, electronic_ch_sign, electronic_ch_pt, electronic_volume,
						financial, financial_ch_sign, financial_ch_pt, financial_volume):

	debug_message_title = "[" + target + " img creator]"

	# Load background Img,font
	try:
		im = Image.open(img_assets_path + target + "/" + target + "_back.jpg")
		arial_font_72 = ImageFont.truetype(img_assets_path + target + arial_font_path, 72)
		arial_font_32 = ImageFont.truetype(img_assets_path + target + arial_font_path, 32)
		arial_font_30 = ImageFont.truetype(img_assets_path + target + arial_font_path, 30)
		arial_font_24 = ImageFont.truetype(img_assets_path + target + arial_font_path, 24)
		adobe_font = ImageFont.truetype(img_assets_path + target + adobe_font_path, 24)
		sign_up = Image.open(img_assets_path + target + "/" + target + "_up.png")
		sign_down = Image.open(img_assets_path + target + "/" + target + "_down.png")
		no_change = Image.open(img_assets_path + target + "/" + target + "_no_change.png")
	except IOError as e:
		print debug_message_title, "load assets Error:".format(e.errno, e.strerror)
	# print debug_message_title, "Background IMG loaded !"

	# Set draw
	try:
		draw = ImageDraw.Draw(im)
	except Exception as e:
		print e

	# twi starts here
	# debug message
	# twi_ch_sign = u'漲'
	# twi_ch_sign = u'跌'
	# twi_ch_sign = u'test'

	# Load twi index values and draw
	twi_ch_str = twi_ch_pt + "(" + twi_ch_percent + ")"

	sign = no_change
	sign.resize((25, 28), Image.BILINEAR)
	# print debug_message_title + " twi_ch_sign :", twi_ch_sign
	if twi_ch_sign == u'漲':
		sign = sign_up
		draw.ink = 254 + 39 * 256 + 90 * 256 * 256
		im.paste(sign, (408, 110), sign)
	elif twi_ch_sign == u'跌':
		sign = sign_down
		draw.ink = 81 + 238 * 256 + 47 * 256 * 256
		im.paste(sign, (408, 110), sign)
	else:
		print debug_message_title + " twi_ch_sign :", twi_ch_sign
		twi_ch_str = ""
		draw.ink = 255 + 247 * 256 + 1 * 256 * 256
		im.paste(sign, (495, 115), sign)
	draw.text((40, 55), twi, font=arial_font_72)
	draw.text((440, 102), twi_ch_str, font=arial_font_24)

	# common settings of txt area
	# txtarea  width = 170px , mid = 85px
	# txtarea start : 48px,234px,420px
	# sign width = 26px
	txtarea_mid = 85
	txtarea_start = 0
	txtarea_y1 = 195
	txtarea_y2 = 225
	sign_width = 26
	sign_x = 0
	sign_y = 238
	txt2_padding = 6
	txt1_w = 0
	txt2_w = 0

	# otc starts here
	# debug message
	# otc_ch_sign = u'漲'
	# otc_ch_sign = u'跌'
	# otc_ch_sign = u'test'

	sign = no_change
	sign.resize((25, 28), Image.BILINEAR)
	# print debug_message_title + " otc_ch_sign :", otc_ch_sign

	# get text width
	txt1_w = get_txt_width(draw, otc, font=arial_font_30)
	txt2_w = get_txt_width(draw, otc_ch_pt, font=arial_font_30)

	# 48 ~ 218 px
	txtarea_start = 48
	sign_x = txtarea_start + txtarea_mid - ((sign_width + txt2_padding + txt2_w) / 2)

	if otc_ch_sign == u'漲':
		sign = sign_up
		draw.ink = 254 + 39 * 256 + 90 * 256 * 256
		im.paste(sign, (sign_x, sign_y), sign)
	elif otc_ch_sign == u'跌':
		sign = sign_down
		draw.ink = 81 + 238 * 256 + 47 * 256 * 256
		im.paste(sign, (sign_x, sign_y), sign)
	else:
		print debug_message_title + " otc_ch_sign :", otc_ch_sign
		otc_ch_pt = ""
		draw.ink = 255 + 247 * 256 + 1 * 256 * 256
		im.paste(sign, (sign_x, sign_y), sign)

	draw.text((txtarea_start + txtarea_mid - (txt1_w / 2), txtarea_y1), otc, font=arial_font_30)
	draw.text((sign_x + sign_width + txt2_padding, txtarea_y2), otc_ch_pt, font=arial_font_30)

	# electronic starts here
	# debug message
	# electronic_sign = u'漲'
	# electronic_ch_sign = u'跌'
	# electronic_ch_sign = u'test'

	sign = no_change
	sign.resize((25, 28), Image.BILINEAR)
	# print debug_message_title + " electronic_ch_sign :", electronic_ch_sign

	# get text width
	txt1_w = get_txt_width(draw, electronic, font=arial_font_30)
	txt2_w = get_txt_width(draw, electronic_ch_pt, font=arial_font_30)

	# 234 ~ 404 px
	txtarea_start = 234
	sign_x = txtarea_start + txtarea_mid - ((sign_width + txt2_padding + txt2_w) / 2)

	if electronic_ch_sign == u'漲':
		sign = sign_up
		draw.ink = 254 + 39 * 256 + 90 * 256 * 256
		im.paste(sign, (sign_x, sign_y), sign)
	elif electronic_ch_sign == u'跌':
		sign = sign_down
		draw.ink = 81 + 238 * 256 + 47 * 256 * 256
		im.paste(sign, (sign_x, sign_y), sign)
	else:
		print debug_message_title + " electronic_ch_sign :", electronic_ch_sign
		electronic_ch_pt = ""
		draw.ink = 255 + 247 * 256 + 1 * 256 * 256
		im.paste(sign, (sign_x, sign_y), sign)
	draw.text((txtarea_start + txtarea_mid - (txt1_w / 2), txtarea_y1), electronic, font=arial_font_30)
	draw.text((sign_x + sign_width + txt2_padding, txtarea_y2), electronic_ch_pt, font=arial_font_30)

	# financial starts here
	# debug message
	# financial_sign = u'漲'
	# financial_ch_sign = u'跌'
	# financial_ch_sign = u'test'

	sign = no_change
	sign.resize((25, 28), Image.BILINEAR)
	# print debug_message_title + " financial_ch_sign :", financial_ch_sign

	# get text width
	txt1_w = get_txt_width(draw, financial, font=arial_font_30)
	txt2_w = get_txt_width(draw, financial_ch_pt, font=arial_font_30)

    # 420 ~ 690 px
	txtarea_start = 420
	sign_x = txtarea_start + txtarea_mid - ((sign_width + txt2_padding + txt2_w) / 2)

	if financial_ch_sign == u'漲':
		sign = sign_up
		draw.ink = 254 + 39 * 256 + 90 * 256 * 256
		im.paste(sign, (sign_x, sign_y), sign)
	elif financial_ch_sign == u'跌':
		sign = sign_down
		draw.ink = 81 + 238 * 256 + 47 * 256 * 256
		im.paste(sign, (sign_x, sign_y), sign)
	else:
		print debug_message_title + " financial_ch_sign :", financial_ch_sign
		financial_ch_pt = ""
		draw.ink = 255 + 247 * 256 + 1 * 256 * 256
		im.paste(sign, (sign_x, sign_y), sign)
	draw.text((txtarea_start + txtarea_mid - (txt1_w / 2), txtarea_y1), financial, font=arial_font_30)
	draw.text((sign_x + sign_width + txt2_padding, txtarea_y2), financial_ch_pt, font=arial_font_30)

	# draw white texts
	draw.ink = 255 + 255 * 256 + 255 * 256 * 256
	# draw volume numbers, remove u"億" in the end
	draw.text((470, 63), twi_volume[:-1], font=arial_font_32)
	# for below indexes
	draw.text((60, 260), otc_volume[:-1], font=arial_font_30)
	draw.text((250, 260), electronic_volume[:-1], font=arial_font_30)
	draw.text((455, 260), financial_volume[:-1], font=arial_font_30)

	# draw u"成交" and u"億"
	# for twi
	draw.text((405, 75), u"成交", font=adobe_font)
	draw.text((585, 75), u"億", font=adobe_font)
	# for below indexes
	draw.text((170, 268), u"億", font=adobe_font)
	draw.text((360, 268), u"億", font=adobe_font)
	draw.text((545, 268), u"億", font=adobe_font)

	# Img save
	try:
		im.save(info_img_path + target + "/" + file_time + "_" + target + ".jpg", "JPEG", quality=100)
		im.save(info_img_path + target + "/last_" + target + ".jpg", "JPEG", quality=100)
	except IOError as e:
		print debug_message_title, "Save IMG Error:".format(e.errno, e.strerror)
	else:
		print debug_message_title, "IMG save to " + info_img_path + target


def get_txt_width(draw, txt, font):
	w, h = draw.textsize(txt, font)
	return w

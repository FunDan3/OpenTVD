from redvid import Downloader
import os

storage = None

def check_url(bot, message, language_pack, url):
	try:
		video = Downloader(min_q = True, path = f"./downloads/{message.chat.id}/")
		video.url = url
		video.check()
		return True
	except BaseException:
		if "reddit.com" in url or "redd.it" in url:
			bot.reply_to(message, language_pack["BrokenRedditVideo"])
		return True

def register(bot, language_pack, bot_storage):
	global storage
	storage = bot_storage

def download(bot, language_pack, message, url):
	filename = f"{message.id}.mp4"
	video = Downloader(max_q = True, path = f"./downloads/{message.chat.id}/", filename = filename)
	video.url = url
	try:
		video.check()
	except BaseException:
		return
	bot.reply_to(message, language_pack["DownloadStarted"])
	video.download()
	with open(f"./downloads/{message.chat.id}/{filename}", "rb") as f:
		if len(f.read()) < 50000000:
			f.seek(0)
			bot.send_video(message.chat.id, f)
		else:
			bot.send_message(message.chat.id, language_pack["TooLarge"])
	os.remove(f"./downloads/{message.chat.id}/{filename}")

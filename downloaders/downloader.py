# General module to download some videos
from . import YouTube
from . import Reddit
import validators
storage = None
def download(bot, language_pack, message):
	if message.chat.id not in storage:
		storage[message.chat.id] = {}
	replacors = {"://www.": "://",
		"http://": "https://"}
	url = message.text
	for replace, replaced in replacors.items():
		url.replace(replace, replaced)
	if not validators.url(url):
		bot.reply_to(message, language_pack["UrlInvalid"])
		return
	if YouTube.check_url(bot, message, language_pack, url):
		YouTube.download(bot, language_pack, message, url)
	elif Reddit.check_url(bot, message, language_pack, url):
		Reddit.download(bot, language_pack, message, url)
	else:
		bot.reply_to(message, language_pack["UnknownService"])

def register(bot, language_pack, bot_storage):
	global storage
	storage = bot_storage

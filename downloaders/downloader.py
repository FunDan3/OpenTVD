# General module to download some videos
from . import YouTube
import validators
def download(bot, language_pack, message):
	replacors = {"://www.": "://",
		"http://": "https://"}
	url = message.text
	for replace, replaced in replacors.items():
		url.replace(replace, replaced)
	if not validators.url(url):
		bot.reply_to(message, language_pack["UrlInvalid"])
		return
	if YouTube.check_url(url):
		pass
	else:
		bot.reply_to(message, language_pack["UnknownService"])

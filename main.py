import telebot
import commands
from components import language_packer
from components import error_handler
import downloaders
storage = {}
def start(language, token):
	bot = telebot.TeleBot(token)
	language_pack = language_packer.language_pack(f"./languagepacks/{language}.json")
	commands.register(bot, language_pack, storage)
	error_handler.register(bot, language_pack, storage)
	for downloader in dir(downloaders):
		if not downloader.startswith("_"):
			getattr(downloaders, downloader).register(bot, language_pack, storage)
	print(f"Started {language}")
	bot.infinity_polling()

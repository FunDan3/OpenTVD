import telebot
import commands
from components import language_packer
def start(language, token):
	bot = telebot.TeleBot(token)
	language_pack = language_packer.language_pack(f"./languagepacks/{language}.json")
	commands.register(bot, language_pack)
	bot.infinity_polling()

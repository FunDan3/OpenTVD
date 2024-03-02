import telebot
import commands
def start(language, token):
	bot = telebot.TeleBot(token)
	commands.register(bot)
	bot.infinity_polling()

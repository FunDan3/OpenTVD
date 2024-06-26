from downloaders import downloader
from components import error_handler
def register(bot, language_pack, storage):
	@bot.message_handler(func = lambda message: message.text.startswith("http"))
	@error_handler.memreset()
	def on_link(message):
		downloader.download(bot, language_pack, message)

	@bot.message_handler(commands = ["license"])
	def license(message):
		bot.send_message(message.chat.id, language_pack["LicenseText"])

	@bot.message_handler(commands = ["start", "help"])
	def start(message):
		bot.send_message(message.chat.id, language_pack["StartText"])

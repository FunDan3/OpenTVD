from downloaders import downloader
def register(bot, language_pack):
	@bot.message_handler(func = lambda message: message.text.startswith("http"))
	def on_link(message):
		print(message)
		downloader.download(bot, language_pack, message)

	@bot.message_handler(commands = ["license"])
	def license(message):
		bot.send_message(message.chat.id, language_pack["LicenseText"])

	@bot.message_handler(commands = ["start", "help"])
	def start(message):
		bot.send_message(message.chat.id, language_pack["StartText"])

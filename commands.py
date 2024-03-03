def register(bot, language_pack):
	@bot.message_handler(commands = ["license"])
	def license(message):
		bot.send_message(message.chat.id, language_pack["LicenseText"])

	@bot.message_handler(commands = ["start", "help"])
	def start(message):
		bot.send_message(message.chat.id, language_pack["StartText"])

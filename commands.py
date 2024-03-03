def register(bot, language_pack):
	@bot.message_handler()
	def anything(message):
		bot.send_message(message.chat.id, f"{message.chat.id}")

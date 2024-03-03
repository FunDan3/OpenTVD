from telebot import types
import pytube
import os

storage = None

def check_url(url):
	try:
		pytube.YouTube(url)
		return True
	except Exception:
		return False

def register(bot, language_pack, bot_storage):
	global storage
	storage = bot_storage
	@bot.message_handler(func = lambda message: message.text == language_pack["YTAudioButton"])
	def audio_button(message):
		markup = types.ReplyKeyboardRemove(selective = False)
		bot.send_message(message.chat.id, language_pack["FetchingStreams"], reply_markup = markup)
		def on_progress(stream, chunk, bytes_remaining):
			percent = (stream.filesize - bytes_remaining)/stream.filesize*100
			bot.edit_message_text(f"{percent}%", sent.chat.id, sent.id)

		def on_complete(stream, file_path):
			bot.edit_message_text(language_pack["DownloadFinished"], sent.chat.id, sent.id)
			with open(file_path, "rb") as f:
				bot.send_audio(message.chat.id, f)
			os.remove(file_path)
			storage[sent.chat.id]["YouTube"]["locked"] = False
		video = pytube.YouTube(storage[message.chat.id]["YouTube"]["url"],
			on_progress_callback = on_progress,
			on_complete_callback = on_complete)
		storage["locked"] = True
		streams = video.streams
		streams = streams.filter(only_audio = True)
		stream = streams.order_by("abr").first()
		sent = bot.send_message(message.chat.id, "0%")
		stream.download(filename = str(sent.chat.id)+".mp3", skip_existing = False) #Ik that it isnt .mp3

	@bot.message_handler(func = lambda message: message.text == language_pack["YTVideoButton"])
	def video_button(message):
		pass
def download(bot, language_pack, message, url):
	if "YouTube" in storage[message.chat.id] and storage[message.chat.id]["YouTube"]["locked"]:
		bot.reply_to(message, language_pack["AlreadyDownloading"])
		return
	storage[message.chat.id]["YouTube"] = {"url": url, "locked": False}
	markup = types.ReplyKeyboardMarkup()
	audio_button = types.KeyboardButton(language_pack["YTAudioButton"])
	video_button = types.KeyboardButton(language_pack["YTVideoButton"])
	markup.add(audio_button, video_button)
	sent = bot.reply_to(message, language_pack["AudioOrVideo"], reply_markup = markup)

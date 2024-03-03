from telebot import types
import pytube
import os

storage = None

def check_url(url):
	try:
		pytube.YouTube(url) # Seems like accepts reddit but doesnt work with it.
		return True and "youtu" in url # I seem to remember domains like m.youtube.com and youtu.be
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
		storage[message.chat.id]["YouTube"]["locked"] = True
		streams = video.streams
		streams = streams.filter(only_audio = True)
		stream = streams.order_by("abr").first()
		sent = bot.send_message(message.chat.id, "0%")
		stream.download(filename = str(sent.chat.id)+".mp3", skip_existing = False) #Ik that it isnt .mp3

	@bot.message_handler(func = lambda message: message.text == language_pack["YTVideoButton"])
	def video_button(message):
		markup = types.ReplyKeyboardRemove(selective = False)
		bot.send_message(message.chat.id, language_pack["FetchingStreams"], reply_markup = markup)
		video = pytube.YouTube(storage[message.chat.id]["YouTube"]["url"])
		streams = video.streams
		streams = streams.filter(progressive = True)
		streams = streams.order_by("resolution")
		streams_resolutions = []
		markup = types.ReplyKeyboardMarkup()
		for stream in streams:
			if stream.resolution not in streams_resolutions:
				streams_resolutions.append(stream.resolution)
				button = types.KeyboardButton(stream.resolution)
				markup.add(button)
		bot.send_message(message.chat.id, language_pack["PickResolution"], reply_markup = markup)

	def download_video(message, quality):
		markup = types.ReplyKeyboardRemove(selective = False)
		bot.send_message(message.chat.id, language_pack["FetchingStreams"], reply_markup = markup)
		def on_progress(stream, chunk, bytes_remaining):
			percent = (stream.filesize - bytes_remaining)/stream.filesize*100
			bot.edit_message_text(f"{percent}%", sent.chat.id, sent.id)

		def on_complete(stream, file_path):
			bot.edit_message_text(language_pack["DownloadFinished"], sent.chat.id, sent.id)
			with open(file_path, "rb") as f:
				bot.send_video(message.chat.id, f)
			os.remove(file_path)
			storage[sent.chat.id]["YouTube"]["locked"] = False
		video = pytube.YouTube(storage[message.chat.id]["YouTube"]["url"],
			on_progress_callback = on_progress,
			on_complete_callback = on_complete)
		storage[message.chat.id]["YouTube"]["locked"] = True
		streams = video.streams
		stream = streams.filter(progressive = True).filter(res = quality).order_by("fps").first()
		sent = bot.send_message(message.chat.id, "0%")
		stream.download(filename = str(sent.chat.id)+".mp4", skip_existing = False) #Ik that it might not be .mp4

	@bot.message_handler(func = lambda message: message.text == "144p")
	def p144(message):
		download_video(message, "144p")
	@bot.message_handler(func = lambda message: message.text == "240p")
	def p240(message):
		download_video(message, "240p")
	@bot.message_handler(func = lambda message: message.text == "360p")
	def p360(message):
		download_video(message, "360p")
	@bot.message_handler(func = lambda message: message.text == "480p")
	def p480(message):
		download_video(message, "480p")
	@bot.message_handler(func = lambda message: message.text == "720p")
	def p720(message):
		download_video(message, "720p")
	@bot.message_handler(func = lambda message: message.text == "1080p")
	def p1080(message):
		download_video(message, "1080p")
	# There is no progressive streams after 1080p
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

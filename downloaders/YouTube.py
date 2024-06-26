from components import error_handler
from telebot import types
import pytube
import os

storage = None

def check_url(bot, message, language_pack, url):
	try:
		pytube.YouTube(url) # Seems like accepts reddit but doesnt work with it.
		return "youtu" in url # I seem to remember domains like m.youtube.com and youtu.be
	except Exception:
		return False

def register(bot, language_pack, bot_storage):
	global storage
	storage = bot_storage
	@bot.message_handler(func = lambda message: message.text == language_pack["YTAudioButton"])
	@error_handler.memreset()
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
		if stream.filesize > 50000000: #50 mb
			bot.send_message(message.chat.id, language_pack["TooLarge"])
			return
		sent = bot.send_message(message.chat.id, "0%")
		stream.download(f"downloads/{message.chat.id}/", filename = stream.default_filename.replace(".mp4", ".mp3"), skip_existing = False)

	@bot.message_handler(func = lambda message: message.text == language_pack["YTVideoButton"])
	@error_handler.memreset()
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
				if stream.filesize < 50000000: #50 mb
					streams_resolutions.append(stream.resolution)
					button = types.KeyboardButton(stream.resolution)
					markup.add(button)
		if streams_resolutions:
			bot.send_message(message.chat.id, language_pack["PickResolution"], reply_markup = markup)
		else:
			bot.send_message(message.chat.id, language_pack["TooLarge"])

	@error_handler.memreset()
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
		stream.download(f"downloads/{message.chat.id}/", skip_existing = False)

	@bot.message_handler(func = lambda message: message.text == "144p")
	@error_handler.memreset()
	def p144(message):
		download_video(message, "144p")
	@bot.message_handler(func = lambda message: message.text == "240p")
	@error_handler.memreset()
	def p240(message):
		download_video(message, "240p")
	@bot.message_handler(func = lambda message: message.text == "360p")
	@error_handler.memreset()
	def p360(message):
		download_video(message, "360p")
	@bot.message_handler(func = lambda message: message.text == "480p")
	@error_handler.memreset()
	def p480(message):
		download_video(message, "480p")
	@bot.message_handler(func = lambda message: message.text == "720p")
	@error_handler.memreset()
	def p720(message):
		download_video(message, "720p")
	@bot.message_handler(func = lambda message: message.text == "1080p")
	@error_handler.memreset()
	def p1080(message):
		download_video(message, "1080p")
	# There is no progressive streams after 1080p

@error_handler.memreset()
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

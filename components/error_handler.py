from telebot import types
import traceback
import secrets
import json
bot = None
storage = None
language_pack = None

def dictize(obj):
	newmsg = {}
	for key in dir(obj):
		if not hasattr(obj, key):
			continue
		value = getattr(obj, key)
		if key.startswith("_") or value == None:
			continue
		if type(value) in [str, int, float, list, dict]:
			newmsg[key] = value
		elif hasattr(value, "__call__"):
			continue
		else:
			newmsg[key] = dictize(value)
	return newmsg

def register(bot_obj, language, bot_storage):
	global storage
	global bot
	global language_pack
	bot = bot_obj
	language_pack = language
	storage = bot_storage

def find_chat_id(args):
	for arg in args:
		if type(arg) == types.Message:
			return arg.chat.id, arg

def memreset():
	def wrapper(function):
		def wrapped(*args, **kwargs):
			global storage
			try:
				function(*args, **kwargs)
			except Exception:
				chat_id, message = find_chat_id(args)
				storage_part = storage[chat_id] if chat_id in storage else {}
				error_report = json.dumps({"Storage": storage_part, "message": dictize(message)}, indent = 4)
				bot.send_message(secrets.telegram.owner_id, "ERROR\n\n"+traceback.format_exc()+"\n"+error_report)
				if chat_id in storage:
					del storage[chat_id]
				bot.send_message(chat_id, language_pack["Error"])
		return wrapped
	return wrapper

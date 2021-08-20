import os

from pyrogram.types import Message

from tronx import USER_ID



# -----
GUEST = int(os.environ.get("SUDO_USERS", USER_ID))

if len(str(GUEST)) == 1 and GUEST == USER_ID:
	SUDO_USERS = [USER_ID]
else:
	SUDO_USERS = [GUEST] + [USER_ID]
# -----



# -----
def __list_all_plugins():
	from os.path import dirname, basename, isfile
	import glob

	mod_paths = glob.glob(dirname(__file__) + "/*.py")
	all_plugins = [
		basename(f)[:-3]
		for f in mod_paths
		if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
	]
	return all_plugins


MODULES = sorted(__list_all_plugins())
__all__ = MODULES + ["MODULES"]
# -----




# types of message
def types(m: Message):
	reply = m.reply_to_message
	if reply.text:
		cast = "text" 
	elif reply.photo:
		cast = "photo"
		name = reply.photo.file_name
	elif reply.video:
		cast = "video"
		name = reply.video.file_name
	elif reply.document:
		cast = "document"
		name = reply.document.file_name
	elif reply.contact:
		cast = "contact"
	elif reply.audio:
		cast = "audio"
		name = reply.audio.file_name
	elif reply.sticker:
		cast = "sticker"
		name = reply.sticker.file_name
	elif reply.animation:
		cast = "animation"
		name = reply.animation.file_name
	elif reply.poll:
		cast = "poll"
	else:
		cast = "unknown"
	return cast, name




# chat type
def chattype(m: Message):
	chat = m.chat.type
	if chat == "supergroup":
		chat_type = "supergroup"
	elif chat == "group":
		chat_type == "group"
	elif chat == "private":
		chat_type = "private"
	else:
		chat_type = "unknown chat type"
	return chat_type

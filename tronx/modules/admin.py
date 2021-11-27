import time
import asyncio
import html

from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions, User

from pyrogram.errors import (
	UserAdminInvalid, 
	UsernameInvalid,
	UserNotParticipant,
	UsernameNotOccupied,
)
from pyrogram.methods.chats.get_chat_members import Filters as ChatMemberFilters

from tronx import (
	app, 
	CMD_HELP, 
	PREFIX,
	Config,
	)

from tronx.helpers import (
	get_arg, 
	get_args, 
	GetUserMentionable, 
	mention_html, 
	mention_markdown, 
	CheckAdmin, 
	CheckReplyAdmin, 
	RestrictFailed,
	gen,
	error, 
	send_edit,
	private,
	code,
	long,
	kick,
)




CMD_HELP.update(
	{"admin" : (
		"admin", 
		{
		"ban" : "bans a user",
		"banall [confirm]" : "Ban all members in by one command",
		"unban" : "unbans a user",
		"mute" : "restricts a user from talking in groups",
		"unmute" : "unrestricts a user from talking in groups",
		"promote" : "promote a member to admin",
		"demote" : "demote a admin to a member",
		"pin" : "pin a message in group",
		"kick" : "kick a user out of your group.",
		"unpin" : "unpin a pinned message in group",
		"unpin all" : "unpin all pinned messages in one command"
		}
		)
	}
)




@app.on_message(gen("ban"))
async def ban_hammer(_, m):
	try:
		# return if used in private
		await private(m)
		reply = m.reply_to_message
		user = False
		if await CheckAdmin(m) is True:
			await send_edit(m, "⏳ • Hold on . . .", mono=True)
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if long(m) == 1:
					return await send_edit(m, "Give me user id | username or reply to the user you want to ban . . .", mono=True)
				elif long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await send_edit(m, "Something went wrong !", mono=True)

			if user:
				if user.user.is_self:
					return await send_edit(m, "You can't ban yourself !", mono=True)
				elif user.status == "administrator":
					return await send_edit(m, "How am i supposed to ban an admin ?", mono=True)
				elif user.status == "creator":
					return await send_edit(m, "How am i supposed to ban a creator of a group ?", mono=True)
			else:
				return await send_edit(m, "Something went wrong !", mono=True)

			await kick(m.chat.id, user.user.id)
			await send_edit(m, f"Banned {user.user.mention} in this chat !")
		else:
			return await send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("banall"))
async def ban_all(_, m):
	try: 
		await private(m)
		if await CheckAdmin(m) is True:
			count = 0
			data = []
			data.clear()
			if long(m) == 1:
				return await send_edit(m, "Use '`confirm`' text after command to ban all members . . .", delme=2)
			elif long(m) > 1 and m.command[1] == "confirm":
				async for x in app.iter_chat_members(m.chat.id):
					if x.status == "member":
						await kick(m.chat.id, x.user.id)
						count += 1
						await send_edit(m, f"Banned {x.user.mention} . . .")
				await send_edit(m, f"Banned {count} members !")
			elif long(m) > 1 and m.command[1] != "confirm":
				await send_edit(m, "Use '`confirm`' text after command to ban all members . . .", delme=2, mono=True)
		else:
			await send_edit(m, "`Sorry, you are not an admin here . . .`", delme=2, mono=True)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("unban"))
async def unban(_, m):
	try:
		await private(m)
		reply = m.reply_to_message
		user = False
		if await CheckAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if long(m) == 1:
					return await send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await send_edit(m, "Something went wrong !", mono=True, delme=4)

			if user:
				if user.user.is_self:
					return await send_edit(m, "You can't Unban yourself !", mono=True)
				elif user.status == "administrator":
					return await send_edit(m, "How am i supposed to ban an admin ?", mono=True)
				elif user.status == "creator":
					return await send_edit(m, "How am i supposed to ban a creator of a group ?", mono=True)
			else:
				return await send_edit(m, "Something went wrong !", mono=True)

			await app.unban_chat_member(m.chat.id, user.user.id)
			await send_edit(m, f"Unbanned {user.user.mention} in this chat !")
		else:
			return await send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await error(m, e)
					




@app.on_message(gen("mute"))
async def mute_user(_, m):
	try:
		await private(m)
		reply = m.reply_to_message
		user = False
		if await CheckAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if long(m) == 1:
					return await send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await send_edit(m, "Something went wrong !", mono=True, delme=4)

			if user:
				if user.user.is_self:
					return await send_edit(m, "You can't mute yourself !", mono=True)
				elif user.status == "administrator":
					return await send_edit(m, "How am i supposed to mute an admin ?", mono=True)
				elif user.status == "creator":
					return await send_edit(m, "How am i supposed to mute a creator of a group ?", mono=True)
			else:
				return await send_edit(m, "Something went wrong !", mono=True)

			await app.restrict_chat_member(
				m.chat.id,
				user.user.id,
				permissions=ChatPermissions(
					can_send_messages=False,
					can_send_media_messages=False,
					can_send_stickers=False,
					can_send_animations=False,
					can_send_games=True,
					can_use_inline_bots=False,
					can_add_web_page_previews=False,
					can_send_polls=False,
					can_change_info=False,
					can_invite_users=True,
					can_pin_messages=False,
				)
				)		
			await send_edit(m, f"Muted {user.user.mention} in this chat !")
		else:
			return await send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("unmute"))
async def unmute(_, m):
	try:
		await private(m)
		reply = m.reply_to_message
		user = False
		if await CheckAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if long(m) == 1:
					return await send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await send_edit(m, "Something went wrong !", mono=True, delme=4)

			if user:
				if user.user.is_self:
					return await send_edit(m, "You can't Unmute yourself !", mono=True)
				elif user.status == "administrator":
					return await send_edit(m, "How do i unmute an admin ?", mono=True)
				elif user.status == "creator":
					return await send_edit(m, "How do i unmute a creator ?", mono=True)
			else:
				return await send_edit(m, "Something went wrong !", mono=True)

			await app.restrict_chat_member(
				m.chat.id,
				user.user.id,
				permissions=ChatPermissions(
					can_send_messages=True,
					can_send_media_messages=True,
					can_send_stickers=True,
					can_send_animations=True,
					can_send_games=True,
					can_use_inline_bots=True,
					can_add_web_page_previews=True,
					can_send_polls=True,
					can_change_info=False,
					can_invite_users=True,
					can_pin_messages=False,
				)
				)
			await send_edit(m, f"Unmuted {user.user.mention} in this chat !")
		else:
			return await send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("kick"))
async def kick_user(_, m):
	try:
		await private(m)
		reply = m.reply_to_message
		user = False
		if await CheckAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if long(m) == 1:
					return await send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await send_edit(m, "Something went wrong !", mono=True, delme=4)

			if user:
				if user.user.is_self:
					return await send_edit(m, "You can't kick yourself !", mono=True)
				elif user.status == "administrator":
					return await send_edit(m, "How am i supposed to kick an admin ?", mono=True)
				elif user.status == "creator":
					return await send_edit(m, "How am i supposed to kick a creator of a group ?", mono=True)
			else:
				return await send_edit(m, "Something went wrong !", mono=True)

			await kick(m.chat.id, user.user.id)
			await send_edit(m, f"Kicked {user.user.mention} in this chat !")
		else:
			return await send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("pin"))
async def pin_message(_, m):
	try:
		if await CheckAdmin(m) is True:
			reply = m.reply_to_message
			if reply:
				await send_edit(m, "⏳ • Hold on . . .", mono=True)
				done = await reply.pin()
				await send_edit(m, "Pinned message!", mono=True) if done else await send_edit(m, "Failed to pin message", delme=2, mono=True)
			elif not reply:
				await send_edit(m, "Reply to a message so that I can pin that message . . .", delme=2, mono=True)    
		else:
			await send_edit(m, "Sorry, you don't have permissions to perform this action !", mono=True, delme=5)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("unpin"))
async def pin_message(_, m):
	try:
		reply = m.reply_to_message
		if reply:
			await send_edit(m, "⏳ • Hold on . . .", mono=True)
			done = reply.unpin()
			await send_edit(m, "Unpinned message !", mono=True) if done else await send_edit(m, "Failed to unpin message . . .", delme=2, mono=True)
		elif not reply and long(m) > 1:
			cmd = m.command[1]
			if cmd == "all":
				done = await app.unpin_all_chat_messages(m.chat.id)
				await send_edit(m, "Unpinned all pinned messages . . .", mono=True) if done else await send_edit(m, "Failed to unpin all messages . . .", delme=2, mono=True)
			elif cmd != "all":
				await send_edit(m, "Reply to a pinned message to unpin or use 'all' as suffix to unpin all pinned messages . . .", delme=2, mono=True)
			else:
				await send_edit(m, "Failed to unpin messages . . .", delme=2, mono=True)
		elif not reply and long(m) == 1:
			await send_edit(m, "Reply to the pinned message to unpin it !", mono=True, delme=5)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("promote"))
async def promote(_, m):
	try:
		await private(m)
		reply = m.reply_to_message
		user = False
		if await CheckAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if long(m) == 1:
					return await send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await send_edit(m, "Something went wrong !", mono=True, delme=4)

			if user:
				if user.user.is_self:
					return await send_edit(m, "You can't promote yourself !", mono=True)
				elif user.status == "administrator":
					return await send_edit(m, "How am i supposed to promote already promoted user ?", mono=True)
				elif user.status == "creator":
					return await send_edit(m, "How am i supposed to promote a creator of a group ? wth ?", mono=True)
			else:
				return await send_edit(m, "Something went wrong !", mono=True)

			await app.promote_chat_member(
				m.chat.id, 
				user.user.id,
				can_pin_messages=True, 
				can_invite_users=True,
				can_restrict_members=True,
				can_delete_messages=True,
				can_post_messages=True,
				)
			await send_edit(m, f"Promoted {user.user.mention} in this chat !")
		else:
			return await send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("demote"))
async def demote(client, m):
	try:
		await private(m)
		reply = m.reply_to_message
		user = False
		if await CheckAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if long(m) == 1:
					return await send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await send_edit(m, "Something went wrong !", mono=True, delme=4)

			if user:
				if user.user.is_self:
					return await send_edit(m, "You can't demote yourself !", mono=True)
				elif user.status == "creator":
					return await send_edit(m, "How am i supposed to demote a creator of a group ?", mono=True)
			else:
				return await send_edit(m, "Something went wrong !", mono=True)

			await app.promote_chat_member(
					m.chat.id,
					user.user.id,
					is_anonymous=False,
					can_change_info=False,
					can_delete_messages=False,
					can_edit_messages=False,
					can_invite_users=False,
					can_promote_members=False,
					can_restrict_members=False,
					can_pin_messages=False,
					can_post_messages=False,
					)
			await send_edit(m, f"Demoted {user.user.mention} in this chat !")
		else:
			return await send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await error(m, e)

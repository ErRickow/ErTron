""" stats plugin """

from pyrogram.types import Message
from pyrogram.enums import ChatType

from main import app, gen



@app.on_cmd(
    commands="stats",
    usage="Get stats of how many channels/bots/ etc you have."
)
async def dialogstats_handler(_, m: Message):
    """ dialogstats handler for stats plugin """
    try:
        await app.send_edit("Getting stats . . .", text_type=["mono"])

        bot = 0
        user = 0
        group = 0
        channel = 0
        stats_format = """
        • **STATS FOR:** {}

        🤖 • **BOTS:** {}
        👨 • **USERS:** {}
        🛡️ • **GROUPS:** {}
        ⚙️ • **CHANNELS:** {}
        """

        async for x in app.get_dialogs():
            if x.chat.type == ChatType.CHANNEL:
                channel += 1
            if x.chat.type == ChatType.BOT:
                bot += 1
            if x.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
                group += 1
            if x.chat.type == ChatType.PRIVATE:
                user += 1

        await app.send_edit(stats_format.format(app.UserMention(), bot, user, group, channel))
    except Exception as e:
        await app.error(e)

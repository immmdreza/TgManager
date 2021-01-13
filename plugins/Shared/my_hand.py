from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message

@Client.on_message(filters.command('ping'))
def ping_all(_, message: Message):
    message.reply_text('Pinged and ready')

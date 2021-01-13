from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
from helpers import getSessions
from configs import running_clients, session_path, shared_plugins
from pyrogram.errors import SessionPasswordNeeded, BadRequest
from pyrogram import raw

addacc_data = {}

@Client.on_message(filters.me & filters.command('runall'))
async def start_all(_, message: Message):
    global running_clients
    sessions = list(getSessions())
    for x in sessions:
        if x not in running_clients:
            cli = Client(session_path + '/' + x, plugins= shared_plugins)
            is_authorized = await cli.connect()
            if is_authorized:
                await cli.send(raw.functions.updates.GetState())
                await cli.initialize()
    
                running_clients[x] = cli
                await message.reply_text(f'Session `{x}` started!')
            else:
                await message.reply_text(f'Unauthorized session found: `{x}`')
    message.reply_text('All SET.')


@Client.on_message(filters.me & filters.command('run'))
async def start(_, message: Message):
    global running_clients

    accs = message.text.split(' ')[1:]
    for x in accs:
        if x not in running_clients:
            cli = Client(session_path + '/' + x, plugins= shared_plugins)
            is_authorized = await cli.connect()
            if is_authorized:
                await cli.send(raw.functions.updates.GetState())
                await cli.initialize()
    
                running_clients[x] = cli
                await message.reply_text(f'Session `{x}` started!')
            else:
                await message.reply_text(f'Unauthorized session found: `{x}`')
        message.reply_text('All SET.')


@Client.on_message(filters.me & filters.command('stopall'))
def stop_all(_, message: Message):
    global running_clients
    for x in running_clients:
        running_clients[x].stop()
        message.reply_text(f'Session `{x}` stoped.')
    running_clients = {}
    message.reply_text('All SET.')


@Client.on_message(filters.me & filters.command('stop'))
def stop_(_, message: Message):
    global running_clients

    accs = message.text.split(' ')[1:]
    for x in accs:
        running_clients[x].stop()
        message.reply_text(f'Session `{x}` stoped.')
        del running_clients[x]
    message.reply_text('All SET.')
        

@Client.on_message(filters.me & filters.command('accs'))
def show(_, message: Message):
    global running_clients
    text = "**Runnig Accounts:**\n- "
    message.edit_text(text + '\n- '.join(running_clients.keys()))


@Client.on_message(filters.me & filters.command('info'))
def info(_, message: Message):
    global running_clients
    text = "**Accounts info:**"
    for x in running_clients:
        me = running_clients[x].get_me()
        text += f'\n- `{x}`: {me.first_name} ({me.id}) [@{me.username}]'
    message.edit_text(text)


@Client.on_message(filters.me & filters.command('addacc'))
def add_acc(_, message: Message):
    global addacc_data

    try:
        se_name = message.text.split(' ')[1]
    except IndexError:
        message.edit_text('Add session name to the command')
        return

    addacc_data = {}
    addacc_data['lvl'] = 0
    addacc_data['se_name'] = se_name
    message.edit_text('Ok reply me **phone number**.')
    

@Client.on_message(filters.me & filters.reply)
async def check_things(client: Client, message: Message):
    global addacc_data

    if addacc_data == {}:
        return

    me = await client.get_me()
    if message.reply_to_message.from_user.id == me.id:
        if message.text.startswith('+'):
            if addacc_data['lvl'] == 0:
                msg = await message.reply_text("`...`")
                addacc_data['phone'] = message.text
                cli = Client(
                    session_path + '/' + addacc_data['se_name'], plugins= shared_plugins
                )
                addacc_data['cli'] = cli
                await cli.connect()
                r = await cli.send_code(message.text)
                addacc_data['lvl'] = 1
                addacc_data['c_hash'] = r
                await msg.edit_text(f"Reply me the **code you receive from telegram**! (`{message.text}``)")
        elif message.text.isdigit():
            if addacc_data['lvl'] == 1:
                addacc_data['code'] = message.text
                msg = await message.reply_text("`...`")
                try:
                    user = await addacc_data['cli'].sign_in(
                        addacc_data['phone'],
                        addacc_data['c_hash'].phone_code_hash,
                        message.text
                    )
                    await msg.edit_text(f"Logged in as **{user.first_name}**\nSession: `{addacc_data['se_name']}`")
                    addacc_data['cli'].disconnect()
                except SessionPasswordNeeded:
                    hint = await addacc_data['cli'].get_password_hint()
                    await msg.edit_text(f'**Password required!**\nReply me your password\n`Hint: {hint}`')
                    addacc_data['lvl'] = 2
        else:
            if addacc_data['lvl'] == 2:
                msg = await message.reply_text("`...`")
                try:
                    user = await addacc_data['cli'].check_password(message.text)
                    await msg.edit_text(f"Logged in as **{user.first_name}**\nSession: `{addacc_data['se_name']}`")
                    await addacc_data['cli'].disconnect()
                except BadRequest:
                    await msg.edit_text(f'**Invalid password**\ntry againg.')
            else:
                await message.reply_text(f'What you want ?') 


                



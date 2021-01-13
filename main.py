from pyrogram import Client, idle
from configs import main_plugins, main_session


main_cli = Client(f'Sessions/{main_session}', plugins= main_plugins)

main_cli.start()
print('Started main.')

idle()
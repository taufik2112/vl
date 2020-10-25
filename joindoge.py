# Louis Philippe B. Facun
# DogeClick Bot Channel from dogeclick.com
# Auto joiner (/join)

import asyncio
import logging
import re
import time
import os
import sys

logging.basicConfig(level=logging.ERROR)

from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from datetime import datetime
from colorama import Fore, init as color_ama
color_ama(autoreset=True)

os.system('cls' if os.name=='nt' else 'clear')

# Get your own values from my.telegram.org
api_id = 800812
api_hash = 'db55ad67a98df35667ca788b97f771f5'

''' DogeClick Bot Channel from dogeclick.com
Options:
1. Dogecoin_click_bot
2. Litecoin_click_bot
3. BCH_click_bot
4. Zcash_click_bot
5. Bitcoinclick_bot
# '''
dogeclick_channel = 'Dogecoin_click_bot'

def print_msg_time(message):
	print('[' + Fore.CYAN + f'{datetime.now().strftime("%H:%M:%S")}' + Fore.RESET + f'] {message}')

async def main():
	print(Fore.MAGENTA + '    _    _   _    ___  _____ _____ ___ ____ ___    _    _     _ ')
	print(Fore.MAGENTA + '   / \  | \ | |  / _ \|  ___|  ___|_ _/ ___|_ _|  / \  | |   | |')
	print(Fore.MAGENTA + '  / _ \ |  \| | | | | | |_  | |_   | | |    | |  / _ \ | |   | | ')
	print(Fore.MAGENTA + ' / ___ \| |\  | | |_| |  _| |  _|  | | |___ | | / ___ \| |___| |___ ')
	print(Fore.MAGENTA + '/_/   \_\_| \_|  \___/|_|   |_|   |___\____|___/_/   \_\_____|_____|\n' + Fore.RESET)
	print(Fore.GREEN + '    -   By Deidara  -   \n' + Fore.RESET)
                                
	# Check if phone number is not specified
	if len(sys.argv) < 2:
		print('Usage: python join.py phone_number')
		print('-> Input number in international format (example: +639162995600)\n')
		e = input('Press any key to exit...')
		exit(1)
		
	phone_number = sys.argv[1]
	
	if not os.path.exists("session"):
		os.mkdir("session")
   
	# Connect to client
	client = TelegramClient('session/' + phone_number, api_id, api_hash)
	await client.start(phone_number)
	me = await client.get_me()
	
	print(f'Nama akun anda: {me.first_name}({me.username})\n')
	print_msg_time('Mengirim perintah /join memindai')
	
	# Start command /join
	await client.send_message(dogeclick_channel, '/join')
	
	# Join the channel
	@client.on(events.NewMessage(chats=dogeclick_channel, incoming=True))
	async def join_start(event):
		message = event.raw_text
		if 'You must join' in message:	
			channel_name = re.search(r'You must join @(.*?) to earn', message).group(1)
			print_msg_time(f'Bergabung ke @{channel_name}...')
			
			# Join the channel
			await client(JoinChannelRequest(channel_name))
			print_msg_time(f'Verifying data...')
			
			# Clicks the joined
			await client(GetBotCallbackAnswerRequest(
				peer=dogeclick_channel,
				msg_id=event.message.id,
				data=event.message.reply_markup.rows[0].buttons[1].data
			))
	
	# Print waiting hours
	@client.on(events.NewMessage(chats=dogeclick_channel, incoming=True))
	async def wait_hours(event):
		message = event.raw_text
		if 'You must stay' in message:	
			waiting_hours = re.search(r'at least (.*?) to earn', message).group(1)
			print_msg_time(Fore.GREEN + f'Berhasil! Mohon tunggu {waiting_hours} untuk mendapat reward\n' + Fore.RESET)
			
	# No more ads
	@client.on(events.NewMessage(chats=dogeclick_channel, incoming=True))
	async def no_ads(event):
		message = event.raw_text
		if 'no new ads available' in message:	
			print_msg_time(Fore.RED + 'Sorry, there are no new ads available\n' + Fore.RESET)
			e = input('Silahkan mencoba kembali nanti, terimakasih...')
			exit(1)
			
	await client.run_until_disconnected()
	
asyncio.get_event_loop().run_until_complete(main())

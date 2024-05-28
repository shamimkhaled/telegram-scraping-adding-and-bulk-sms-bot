import csv
import os
import sys
import random
import time
import pickle
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError, PeerFloodError
from telethon.tl.types import InputPeerUser
from telethon.sync import events
import pyfiglet

# Constants for console colors
light_green = '\033[92m'
white = '\033[0m'
red = '\033[91m'
cyan = '\033[96m'
rs = '\033[0m'


info = light_green + '(' + white + 'i' + light_green + ')' + rs
error = light_green + '(' + red + '!' + light_green + ')' + rs
success = white + '(' + light_green + '+' + white + ')' + rs
INPUT = light_green + '(' + cyan + '~' + light_green + ')' + rs
colors = [light_green, white, red, cyan]

# Constants for sleep time between messages (in seconds)
SLEEP_TIME = 20

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def banner_text():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('Telegram Bot')
    print(random.choice([light_green, white, red]) + banner + rs)

clear()
banner_text()
print(f'  Author: {white}Shamim Khaled{rs}\n')

f = open('account_info.txt', 'rb')
accounts = []
while True:
    try:
        accounts.append(pickle.load(f))
    except EOFError:
        f.close()
        break
print(f'{INPUT}{light_green}({cyan}~{light_green}) Choose an account\n')
for i, acc in enumerate(accounts):
    print(f'{light_green}({white}{i}{light_green}) {acc[2]}')
ind = int(input(f'\n {INPUT}{light_green}({cyan}~{light_green}) Enter your choice: '))
api_id = accounts[ind][0]
api_hash = accounts[ind][1]
phone = accounts[ind][2]

c = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
c.connect()

if not c.is_user_authorized():
    try:
        c.send_code_request(phone)
        code = input(f'{light_green}({cyan}~{light_green}) Enter the login code for {white}{phone}{red}: ')
        c.sign_in(phone, code)
    except PhoneNumberBannedError:
        print(f'{error}{white}{phone}{red} is banned!{rs}')
        print(f'{error}{light_green} Run {white}manage.py{light_green} to filter them{rs}')
        sys.exit()

# Assuming members.csv file structure: username,user_id,access_hash,group,group_id,status
input_file = "F:\\telegram-group-scraping-bot\\members\\members.csv"

users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {
            'username': row[0],
            'user id': int(row[1]),
            'access hash': int(row[2]),
            'group': row[3],
            'group_id': row[4],
            'status': row[5]
        }
        users.append(user)

print(f'{light_green}[1] Send SMS by user ID\n[2] Send SMS by username ')
mode = int(input(f'{light_green}Input: {rs}'))

message = input(f'{light_green}[+] Enter Your Message: {rs}')

for user in users:
    try:
        if mode == 2:
            if user['username'] == "":
                continue
            receiver = c.get_input_entity(user['username'])
        elif mode == 1:
            receiver = InputPeerUser(user['user id'], user['access hash'])
        else:
            print(f'{red}[!] Invalid Mode. Exiting.')
            c.disconnect()
            sys.exit()

        print(f'{light_green}[+] Sending Message to: {user["username"]}')
        c.send_message(receiver, message.format(user['username']))
        print(f'{light_green}[+] Waiting {SLEEP_TIME} seconds')
        time.sleep(SLEEP_TIME)
    except PeerFloodError:
        print(f'{red}[!] Getting Flood Error from Telegram.')
        print(f'{red}[!] Script is stopping now. Please try again after some time.')
        c.disconnect()
        sys.exit()
    except Exception as e:
        print(f'{red}[!] Error: {e}')
        print(f'{red}[!] Trying to continue...')
        continue

c.disconnect()
print("Done. Message sent to all users.")

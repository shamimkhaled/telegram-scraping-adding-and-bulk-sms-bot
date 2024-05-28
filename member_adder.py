import sys
import csv
import time
import keyboard
import random
import pyfiglet
from colorama import init, Fore
import os
import pickle
import traceback
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest

'''
try:
    import beepy
except ImportError:
    if os.name == 'nt':
        os.system('pip install beepy')
    else:
        pass
'''
init()

red = Fore.RED
light_green = Fore.GREEN
rs = Fore.RESET
white = Fore.WHITE
cyan = Fore.CYAN
yellow = Fore.YELLOW

colors = [red, light_green, white, yellow, cyan]
info = light_green + '(' + white + 'i' + light_green + ')' + rs
error = light_green + '(' + red + '!' + light_green + ')' + rs
success = white + '(' + light_green + '*' + white + ')' + rs
INPUT = light_green + '(' + cyan + '~' + light_green + ')' + rs
plus = light_green + '(' + white + '+' + light_green + ')' + rs

def banner_text():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('Telegram Bot')
    print(random.choice(colors) + banner + rs)
    print(f' Author: {white}Shamim Khaled{rs}')


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
        
global scraped_group
with open('target_group.txt', 'r') as f:
    scraped_group = f.readline()
f.close()

clear()
banner_text()

users = []
input_file = 'members\\members.csv'
with open(input_file, 'r', encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter=',', lineterminator='\n')
    next(reader, None)
    for row in reader:
        user = {}
        user['username'] = row[0]
        user['user_id'] = row[1]
        user['access_hash'] = row[2]
        user['group'] = row[3]
        user['group_id'] = row[4]
        users.append(user)

accounts = []
f = open('account_info.txt', 'rb')
while True:
    try:
        accounts.append(pickle.load(f))
    except EOFError:
        break

print('\n' + info + light_green + ' Creating sessions for all accounts...' + rs)

for a in accounts:
    iD = int(a[0])
    Hash = str(a[1])
    phn = str(a[2])
    clnt = TelegramClient(f'sessions\\{phn}', iD, Hash)
    clnt.connect()

    banned = []
    if not clnt.is_user_authorized():
        try:
            clnt.send_code_request(phn)
            code = input(f'{INPUT}{light_green} Enter the code for {white}{phn}{cyan}[s to skip]:{red}')
            if 's' in code:
                accounts.remove(a)
            else:
                clnt.sign_in(phn, code)
        except PhoneNumberBannedError:
            print(f'{error}{white}{phn} {red}is banned!{rs}')
            banned.append(a)
    for z in banned:
        accounts.remove(z)
        print('\n'+info+light_green+'Banned account removed'+rs)

    time.sleep(0.5)
    clnt.disconnect()


print(info+' Sessions created!')
time.sleep(2)

print(f'{plus}{light_green} Enter the exact username of the public group{white}[Without @]')
g = input(f'{INPUT}{light_green} Username[Eg: spikegrowth, Technology_Hut]: {red}')
group = 't.me/' + str(g)

# print('\n')
print(f'{info}{light_green} Joining from all accounts...{rs}')
for account in accounts:
    api_id = int(account[0])
    api_hash = str(account[1])
    phone = str(account[2])
    client = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
    client.connect()
    try:
        username = client.get_entity(group)
        client(JoinChannelRequest(username))
        print(f'{success}{light_green} Joined from {phone}')
    except:
        print(f'{error}{red} Error in joining from {phone}')
        accounts.remove(account)
    client.disconnect()
time.sleep(2)
clear()

number = len(accounts)
print(f'{info}{light_green} Total accounts: {white}{number}')
print(f'{info}{light_green} If you have more than 10 accounts then it is recommended to use 10 at a time')
a = int(input(f'{plus}{light_green} Enter number of accounts to use: {red}'))
to_use = []

print(f'\n{info}{light_green} Distributing CSV files...{rs}')
time.sleep(2)
for i in accounts[:a]:
    done = []
    to_use.append(i)
    file = 'members\\members' + str(accounts.index(i)) + '.csv'
    with open(file, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])

        # GET 60 USERS TO ADD
        for user in users[:60]:
            writer.writerow([user['username'], user['user_id'], user['access_hash'], user['group'], user['group_id']])
            done.append(user)
    f.close()
    del_count = 0
    while del_count != len(done):
        del users[0]
        del_count += 1
    if len(users) == 0:
        break
if not len(users) == 0:
    with open('members\\members.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
        for user in users:
            writer.writerow([user['username'], user['user_id'], user['access_hash'], user['group'], user['group_id']])
    f.close()
    m = str(len(users))
    print(f'{info}{light_green} Remaining {m} users stored in {white}members.csv')
for acc in to_use:
    accounts.remove(acc)

with open('account_info.txt', 'wb') as f:
    for acc in accounts:
        pickle.dump(acc, f)
    for k in to_use:
        pickle.dump(k, f)
    f.close()
'''
with open('resume.txt', 'w') as f:
    f.write(scraped_group)
    f.close()
'''
print(f'{info}{light_green} CSV file distribution complete{rs}')
time.sleep(2)
clear()
if not os.name == 'nt':
    print(f'{error}{red} Automation supports only Windows systems')
    sys.exit()

program = 'user_adder.py'
o = str(len(to_use))
print(f'\n{info}{red} This will be fully automated.')
print(f'{info}{red} Don\'t touch the keyboard until cmd window pop-up stops')
input(f'\n{plus}{light_green} Press enter to continue...{rs}')
print(f'\n{info}{light_green} Launching from {o} accounts...{rs}\n')

for i in range(5, 0, -1):
    print(random.choice(colors) + str(i) + rs)
    time.sleep(1)
for account in to_use:
    api_id = str(account[0])
    api_hash = str(account[1])
    phone = str(account[2])
    file = 'members\\members' + str(to_use.index(account)) + '.csv'
    os.system('start cmd')
    time.sleep(1.5)
    keyboard.write('python' + ' ' + program + ' ' + api_id + ' ' + api_hash + ' ' + phone + ' ' + file + ' ' + group + ' ' + str(scraped_group))
    keyboard.press_and_release('Enter')
    print(f'{plus}{light_green} Launched from {phone}')

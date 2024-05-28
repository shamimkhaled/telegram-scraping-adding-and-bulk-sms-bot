import csv
import sys
import pickle
import random
import pyfiglet
import os
import datetime
import datetime
from colorama import init, Fore, Style
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from telethon.tl.types import UserStatusRecently
from telethon.tl.types import UserStatusRecently, ChannelParticipantsAdmins, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, UserStatusOnline
from time import sleep
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import SendMessageRequest


init()

light_green = Fore.LIGHTGREEN_EX
rs = Fore.RESET
red = Fore.RED
white = Fore.WHITE
cyan = Fore.CYAN
green = Fore.GREEN
blue = Fore.BLUE

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)

info = light_green + '(' + white + 'i' + light_green + ')' + rs
error = light_green + '(' + red + '!' + light_green + ')' + rs
success = white + '(' + light_green + '+' + white + ')' + rs
INPUT = light_green + '(' + cyan + '~' + light_green + ')' + rs
colors = [light_green, white, red, cyan]

def banner_text():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('Telegram Bot')
    print(random.choice(colors) + banner + rs)

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

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
print(f'{INPUT}{cyan} Choose an account to scrape members\n')
i = 0
for acc in accounts:
    print(f'{light_green}({white}{i}{light_green}) {acc[2]}')
    i += 1
ind = int(input(f'\n{INPUT}{cyan} Enter your choice: '))
api_id = accounts[ind][0]
api_hash = accounts[ind][1]
phone = accounts[ind][2]
group_name = input(f"Enter the name of the group [don't enter channel name] without the @: {red}")

c = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
c.connect()
if not c.is_user_authorized():
    try:
        c.send_code_request(phone)
        code = input(f'{INPUT}{light_green} Enter the login code for {white}{phone}{red}: ')
        c.sign_in(phone, code)
    except PhoneNumberBannedError:
        print(f'{error}{white}{phone}{red} is banned!{rs}')
        print(f'{error}{light_green} Run {white}manage.py{light_green} to filter them{rs}')
        sys.exit()

group = c.get_entity(group_name)
target_group = "t.me/" + group_name

choice = int(input(f"\n{light_green}How would you like to obtain the users?\n\n{red}[{cyan}0{red}]{light_green} All users\n{red}[{cyan}1{red}]{light_green} Active Users(online today and yesterday)\n{red}[{cyan}2{red}]{light_green} Users active in the last week\n{red}[{cyan}3{red}]{light_green} Users active in the last month\n{red}[{cyan}4{red}]{light_green} Non-active users(not active in the last month) \n\nYour choice: "))
members = []
members = c.iter_participants(group, aggressive=True)

channel_full_info = c(GetFullChannelRequest(group))
count = channel_full_info.full_chat.participants_count

def write(group,member):
    if member.username:
        username = member.username
    else:
        username = ''
    if isinstance(member.status,UserStatusOffline):
        writer.writerow([username, member.id, member.access_hash, group.title, group.id,member.status.was_online])
    else:
        writer.writerow([username, member.id, member.access_hash, group.title, group.id,type(member.status).__name__])

admin_choice = input(f"{light_green}Would you like to have admins on a separate CSV file? {rs}[y/n] {light_green}")
if admin_choice == "y" or admin_choice == "Y":
    with open("members\\admins.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'group', 'group id','status'])
        for member in c.iter_participants(group, filter=ChannelParticipantsAdmins):    
            if not member.bot:
                write(group,member)
f.close()
print(f"{light_green}")
with open("members\\members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'group', 'group id','status'])
    if choice == 0:
        try:
            for index,member in enumerate(members):
                print(f"{index+1}/{count}", end="\r")
                if index%100 == 0:
                    sleep(3)
                if not member.bot:
                    write(group,member)                   
        except:
            print("\nThere was a FloodWaitError, but check members.csv. More than 95%% of members should be already added.")
    elif choice == 1:
        try:
            for index,member in enumerate(members):
                print(f"{index+1}/{count}", end="\r")
                if index%100 == 0:
                    sleep(3)
                if not member.bot:
                    if isinstance(member.status, (UserStatusRecently,UserStatusOnline)):
                        write(group,member)
                    elif isinstance(member.status,UserStatusOffline):
                        d = member.status.was_online                    
                        today_user = d.day == today.day and d.month == today.month and d.year == today.year
                        yesterday_user = d.day == yesterday.day and d.month == yesterday.month and d.year == yesterday.year
                        if today_user or yesterday_user:
                            write(group,member)
        except:
            print("\nThere was a FloodWaitError, but check members.csv. More than 95%% of members should be already added.")
    elif choice == 2:
        try:
            for index,member in enumerate(members):
                print(f"{index+1}/{count}", end="\r")
                if index%100 == 0:
                    sleep(3)
                if not member.bot:
                    if isinstance(member.status, (UserStatusRecently,UserStatusOnline,UserStatusLastWeek)):
                        write(group,member)
                    elif isinstance(member.status,UserStatusOffline):
                        d = member.status.was_online
                        for i in range(0,7):
                            current_day = today - datetime.timedelta(days=i)
                            correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                            if correct_user:
                                write(group,member)
        except:
            print("\nThere was a FloodWaitError, but check members.csv. More than 95%% of members should be already added.")
    elif choice == 3:
        try:
            for index,member in enumerate(members):
                print(f"{index+1}/{count}", end="\r")
                if index%100 == 0:
                    sleep(3)
                if not member.bot:
                    if isinstance(member.status, (UserStatusRecently,UserStatusOnline,UserStatusLastWeek,UserStatusLastMonth)):
                        write(group,member)
                    elif isinstance(member.status,UserStatusOffline):
                        d = member.status.was_online
                        for i in range(0,30):
                            current_day = today - datetime.timedelta(days=i)
                            correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                            if correct_user:
                                write(group,member)
        except:
            print("\nThere was a FloodWaitError, but check members.csv. More than 95%% of members should be already added.")
    elif choice == 4:
        try:
            all_users = []
            active_users = []
            for index,member in enumerate(members):
                print(f"{index+1}/{count}", end="\r")
                all_users.append(member)
                if index%100 == 0:
                    sleep(3)
                if not member.bot:
                    if isinstance(member.status, (UserStatusRecently,UserStatusOnline,UserStatusLastWeek,UserStatusLastMonth)):
                        active_users.append(member)
                    elif isinstance(member.status,UserStatusOffline):
                        d = member.status.was_online
                        for i in range(0,30):
                            current_day = today - datetime.timedelta(days=i)
                            correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                            if correct_user:                            
                                active_users.append(member)
            for member in all_users:
                if member not in active_users:
                    write(group,member)
        except:
            print(f"\n{red}There was a FloodWaitError, but check members.csv. More than 95%% of members should be already added.")

    




f.close()

print(f"\n{light_green}Users saved in the csv file.{rs}\n")
clear()
banner_text()
with open('target_group.txt', 'w') as f:
    f.write(target_group)
f.close()
sys.exit()


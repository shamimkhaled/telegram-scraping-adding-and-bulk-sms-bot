import requests
import os, random
import pickle, pyfiglet
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from colorama import init, Fore
from time import sleep

init()

ligh_green = Fore.LIGHTGREEN_EX
white = Fore.WHITE
cyan = Fore.CYAN
yellow = Fore.YELLOW
red = Fore.RED
n = Fore.RESET
all_colors = [ligh_green, red, white, cyan, yellow]

def banner_text():
    font = pyfiglet.Figlet(font='slant')
    banner = font.renderText('Telegram Bot')
    print(f'{random.choice(all_colors)}{banner}{n}')
    print(red+' Author: Shamim Khaled'+n+'\n')


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

while True:
    clear()

    banner_text()

    print(ligh_green+'[1] Add new accounts'+n)
    print(ligh_green+'[2] Filter all banned accounts'+n)
    print(ligh_green+'[3] List out all the accounts'+n)
    print(ligh_green+'[4] Delete specific accounts'+n)
    print(ligh_green+'[5] Quit')

    choose = int(input(f'\nEnter your choice: {red}'))
    if choose == 1:
        with open('account_info.txt', 'ab') as g:
            recently_added = []
            while True:
                a = int(input(f'\n{ligh_green}Enter API ID: {red}'))
                b = str(input(f'{ligh_green}Enter API Hash: {red}'))
                c = str(input(f'{ligh_green}Enter Phone Number: {red}'))
                p = ''.join(c.split())
                pickle.dump([a, b, p], g)
                recently_added.append([a, b, p])
                ab = input(f'\nDo you want to add more accounts?[y/n]: ')
                if 'y' in ab:
                    pass
                else:
                    print('\n'+ligh_green+'[i] Saved all accounts in account_info.txt'+n)
                    g.close()
                    sleep(3)
                    clear()
                    print(ligh_green + '[*] Logging in from new accounts...\n')
                    for added in recently_added:
                        c = TelegramClient(f'sessions/{added[2]}', added[0], added[1])
                        try:
                            c.start()
                            print(f'n\n{ligh_green}[+] Logged in - {added[2]}')
                            c.disconnect()
                        except PhoneNumberBannedError:
                            print(f'{red}[!] {added[2]} is banned! Filter it using option 2')
                            continue
                        print('\n')
                    input(f'\n{ligh_green}Press enter to goto main menu...')
                    break
        g.close()
    elif choose == 2:
        accounts = []
        banned_accounts = []
        h = open('account_info.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(h))
            except EOFError:
                break
        h.close()
        if len(accounts) == 0:
            print(red+'[!] There are no accounts! Please add some and retry')
            sleep(3)
        else:
            for account in accounts:
                api_id = int(account[0])
                api_hash = str(account[1])
                phone = str(account[2])
                client = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
                client.connect()
                if not client.is_user_authorized():
                    try:
                        client.send_code_request(phone)
                        client.sign_in(phone, input('[+] Enter the code: '))
                    except PhoneNumberBannedError:
                        print(red+str(phone) + ' is banned!'+n)
                        banned_accounts.append(account)
            if len(banned_accounts) == 0:
                print(ligh_green+'Congrats! No banned accounts')
                input('\nPress enter to goto main menu')
            else:
                for m in banned_accounts:
                    accounts.remove(m)
                with open('account_info.txt', 'wb') as k:
                    for a in accounts:
                        Id = a[0]
                        Hash = a[1]
                        Phone = a[2]
                        pickle.dump([Id, Hash, Phone], k)
                k.close()
                print(ligh_green+'[i] All banned accounts removed'+n)
                input('\nPress enter to goto main menu')
    elif choose == 3:
        screen = []
        j = open('account_info.txt', 'rb')
        while True:
            try:
                screen.append(pickle.load(j))
            except EOFError:
                break
        j.close()
        print(f'\n{ligh_green}')
        print(f'API ID  |            API Hash              |    Phone ')
        print(f'==========================================================')
        i = 0
        for z in screen:
            print(f'{z[0]} | {z[1]} | {z[2]}')
            i += 1
        print(f'==========================================================')
        input('\nPress enter to goto main menu')

    elif choose == 4:
        accounts = []
        f = open('account_info.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        i = 0
        print(f'{ligh_green}[i] Choose an account to delete\n')
        for acc in accounts:
            print(f'{ligh_green}[{i}] {acc[2]}{n}')
            i += 1
        index = int(input(f'\n{ligh_green}[+] Enter a choice: {n}'))
        phone = str(accounts[index][2])
        session_file = phone + '.session'
        if os.name == 'nt':
            os.system(f'del sessions\\{session_file}')
        else:
            os.system(f'rm sessions/{session_file}')
        del accounts[index]
        f = open('account_info.txt', 'wb')
        for account in accounts:
            pickle.dump(account, f)
        print(f'\n{ligh_green}[+] Account Deleted{n}')
        input(f'{ligh_green}Press enter to goto main menu{n}')
        f.close()
    elif choose == 5:
        clear()
        banner_text()
        quit()
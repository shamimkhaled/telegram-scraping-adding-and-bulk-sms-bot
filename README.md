# Telegram Bot - Scrape Telegram Members and Add to your Group and Send to Bulk SMS  All Scraped Members

## Environment Setup:

1. **Download and Install Python:**
   - Visit [python.org/downloads](https://www.python.org/downloads/) to download and install Python for your operating system.
   - Set up the Python environment path in Windows, Linux, or macOS.

   **Download and Install VS Code:**
      - Visit [code.visualstudio.com/download](https://code.visualstudio.com/download) to download and install VS Code for your operating system.

2. **Create Python Virtual Environment:**
   - Open your terminal in the project directory or Open the project directory in VS code.
   - Run the command: `python -m venv env` to create a virtual environment.
     
   **Activate the environment :** 
    - Windows: `.\env\Scripts\activate` 
    - Linux or macOS: `source env/bin/activate`

3. **Install Project Dependencies:**
   - Run: `pip install -r requirements.txt` to install project dependencies.

4. **Create Telegram API Token:**
   - Go to [my.telegram.org/auth](https://my.telegram.org/auth).
   - Enter your phone number and set up the API information to generate an API token.

## Documentation:

**Step 1: Setup Accounts**

- Open the terminal in the project directory.
- Run `python authenticate.py`.
  - Choose option 1 to enter new accounts.
  - Enter Api id, Api hash, and phone number.
  - If adding more accounts, enter 'y'; if not, enter 'n'.
  - Choose option 2 to filter all banned accounts.
  - Choose option 3 to show all accounts.
  - Choose option 4 to delete accounts.

**Step 2: Scraping Members**

- Run `python member_scraper.py` in the terminal.
  - Choose an account to scrape.
  - Choose to scrape from a public or private group.
    - PUBLIC GROUPS: Suppose public group username is @PythonHub. Enter only 'PythonHub'. Omit '@' and hit enter
     - PRIVATE GROUPS: Copy invite link and paste in the terminal and hit enter.
  - Choose whether to filter active users.

**Step 3: Adding Members**

- Launch `python member_adder.py` in the terminal.
- It'll create sessions and prompt for a login code if not logged in.
- Enter the username of the public group without '@'.
- Enter the number of accounts to use.
- Read the warning and press enter to proceed.
- It'll add members using the specified accounts.

**Troubleshooting:**

1. **Members Not Getting Added:**
   - It may be due to account limitations. Try using other accounts.

2. **Error While Logging In:**
   - If you have two-factor authentication enabled, turn it off. You can turn it back on after logging in.

For any problems, open an issue on GitHub or contact the developer via the Telegram group mentioned in the README.md.

**Step 4: Send Bulk Messages**

- Launch `python bulk_sms.py` in the terminal.
- Select the number and enter.
- Choose the option to send a message based on the member's username or user ID.
- It will send the message to all members in the group.

Ensure to follow the documentation properly for smooth execution of the project.
## Color Reference

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Example Color | ![#0a192f](https://via.placeholder.com/10/0a192f?text=+) #0a192f |
| Example Color | ![#f8f8f8](https://via.placeholder.com/10/f8f8f8?text=+) #f8f8f8 |
| Example Color | ![#00b48a](https://via.placeholder.com/10/00b48a?text=+) #00b48a |
| Example Color | ![#00d1a0](https://via.placeholder.com/10/00b48a?text=+) #00d1a0 |


## Authors

- [@shamimkhaled](https://www.github.com/shamimkhaled)


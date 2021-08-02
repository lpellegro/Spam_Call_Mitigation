# Banned_IP_Notification

Cisco Expressway release X14 is able to mitigate spam calls and toll fraud by jailing the spam IP source addresses, thus offloading Expressway by unwanted calls and reducing the impact of toll fraud. 

This is a bundle made by 2 independent scripts. The first one - ipjail.py - sends a notification card to a Webex space whenever a new IP is banned on a monitored Expressway. 
The second script - listening_bot.py - allows the admin to interact with the bot by changing the status of an IP between 4 different statuses (ban/unban/exempt/remove exemption) and request the call activity list of a banned IP.
The remaining scripts are used by one or the other and only need to be in the same folder with the two main ones.

HOW TO RUN

Customize the credentials.py file. This file contains the local settings: FQDN, IP addresse, username and password of every Expressway, Webex room ID, bot beaerer, and IPWhois token.
Copy the files in a directory of the server that will run the scripts
Launch ipjail.py file. This file runs once, and searches for banned IP addresses in Expressway. When found, sends a notification in the Webex space. In order to make it recurrent, use Crontab (Linux) or Task Scheduler (Windows). This is an example with Crontab and a Python virtual environment in CentOS 8 for a script running every hour: 

    0 * * * * cd /root/working_directory && source ~/.virtualenvs/${PWD##*/}/bin/activate && python3.9 ipjail.py >> cron.log 2>&1
    
Launch listening_bot.py. This script requires Websocket Webex Bot: https://github.com/fbradyirl/webex_bot. It allows the admin to interact with the notification system.
Dependencies:

- Python 3.9

- pip install webex_bot
- pip install request requests
- pip install paramiko
- pip install openpyxl

# Spam Call and Toll Fraud Mitigation

Cisco Expressway release X14 is able to mitigate spam calls and toll fraud attempts by jailing the spam IP address, thus offloading Expressway by unwanted calls and reducing the impact of toll fraud. 

This is a bundle made by 2 independent scripts. The first one - ipjail.py - sends a notification card to a Webex space whenever a new IP is banned on a monitored Expressway. 
The second script - listening_bot.py - allows the admin to interact with the bot by changing the status of an IP between 4 different statuses (ban/unban/exempt/remove exemption) and to request the call activity list of a banned IP.
The rest of the scripts need to be in the same folder with the two main ones.

Dependencies:
- Python 3.9
- pip install webex_bot
- pip install requests
- pip install paramiko
- pip install openpyxl

# Step-by-step Installation Instructions
* Create a Webex bot and store the bot Access Token
* Create a Webex space and store the room ID
* Register to https://www.whoisxmlapi.com and get an API Key for whois lookup
* Install and run the script. The following instructions apply to CentOS 8, but other platforms might be considered

## Create a Webex bot

Register to developer.webex.com. Click on your name in the right upper corner, select "My Webex Apps" and the option "Create a Bot". Copy and store the Access Token:

<img width="1897" alt="Copy the Access" src="https://user-images.githubusercontent.com/88320330/128480031-c5f74719-6149-45c4-85b2-1cefaca2d6d8.png">

## Create a Webex space
1. Use the bot access token to create a room: go to https://developer.webex.com/docs/platform-introduction, select "API Reference" on the left-hand side, scroll down to "Rooms", then click on "Create a room". On the right-hand side uncheck "Use personal access token" and paste the bot access token. Put a name in the "title" box (i.e. "My Space") and then hit "Run". Copy the and store the room ID.

<img width="1247" alt="Copy the room ID" src="https://user-images.githubusercontent.com/88320330/128480164-dd4f7c54-dbb4-47ec-a548-5b8c604e848f.png">

2. Add yourself in the room as a member: go to Memberships -> Create a Membership

<img width="1677" alt="Paste the Access" src="https://user-images.githubusercontent.com/88320330/128480307-4f937c82-2162-434d-b235-0de822cf4e8f.png">

## Get an API Key for Whois lookup

Go to https://www.whoisxmlapi.com and register. Click on your username in the right-hand side upper corner and select "My Products". Your API Key will be shown. Store your API Key.

##  Run the scripts in CentOS 8
1. Install Python3.9 
2. Create a new directory (in this example is called "notifications"): 
   ```
   mkdir notifications
   ```
3. Install a virtual environment on this directory:
   ```
   cd notifications
   python3.9 -m venv ~/.virtualenvs/${PWD##*/}
   source ~/.virtualenvs/${PWD##*/}/bin/activate
   ```
4. Install the following packages:
   ```
   pip install webex_bot
   pip install requests
   pip install paramiko
   pip install openpyxl
   ```
   
5. Download the script from GitHub and customise the credentials.py file as explained in the file itself (some examples are also reported. Pay attention to commas).
6. Test the script by running: ```python3.9 ipjail.py ```. If credentials.py has been customised correctly the script should run. The script connects to Expressway using HTTPS. If Expressway uses a private cert, the CA must be trusted by the server running the script.
7. If the test is successful, configure Crontab to run the script periodically by typing: ```crontab -e```. The following configuration makes the script run every hour:
   ```
   0 * * * * cd  /root/notifications && source ~/.virtualenvs/${PWD##*/}/bin/activate && python3.9 ipjail.py  >> cron.log 2>&1
   ```
8. Test the listening bot by typing ```python3.9 listening_bot.py```. Then set it up as a service to start at boot and automatically restart in case of issues:
   
```
vi /etc/systemd/system/webex_bot.service
```

```
[Unit]
Description="Webex bot with websocket"

[Service]
User=root
WorkingDirectory=/root/notifications
VIRTUAL_ENV=/root/.virtualenvs/notifications/
Environment=PATH=$VIRTUAL_ENV/bin:$PATH
ExecStart=/root/.virtualenvs/notifications/bin/python3.9 listening_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```
9. Run the service: 
   ```
   systemctl enable webex_bot.service
   systemctl start webex_bot.service
   ```
11. Check the status: 
    ```
    systemctl status webex_bot.service
    ```
13. To stop the service: 
    ```
    systemctl stop webex_bot.service
    ```



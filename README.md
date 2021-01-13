# TgManager
This is An accounts manager userbot for telegram 

## Setup

1- **Clone the project** ( `git clone https://github.com/immmdreza/TgManager.git` )

2- **Head to the project directory** ( `cd TgManager` )

3- **Install requirements** ( `py -m pip install -r requirements.txt` ) 

4- Open config.ini And replace _API_ID_ and _API_HASH_ with your's

5- **Create a folder for session files named Sessions** ( `mkdir Sessions` )

6- **Run the main client** ( `py main.py` )

## Remember 

To add handler for child accounts You should make python files in `plugins` folder

Handlers in `main_handlers` folder are all for main client, as you there is one named _accs.py_ to manage child accounts.

## Commands

This commands should run by main account:
  - `/addacc [Session Name]`: use this to add account.
  - `/runall` : starts all child accounts
  - `/stopall` : stops all runnig accounts 
  - `/run [Session Name]` : run on or more specific accounts
  - `/stop [Session Name]` : stop on or more specific accounts
  - `/accs` : get a list of running session names
  - `/info` : get info about running accounts 

## Last thing 

Read [Pyrogram](https://docs.pyrogram.org/) documentations specially [Smart Plugins](https://docs.pyrogram.org/topics/smart-plugins) 

Explore the code it's easy to understand .

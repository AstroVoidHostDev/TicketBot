<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=900&color=00F7FF&center=true&vCenter=true&width=650&lines=TicketBot+Discord+%2B+BestFree+Bot;Fast+%7C+Secure+%7C+Professional;Made+By+❤️+ITZ_YTANSH" />
</p>

# 🎟️ Ultimate Discord Ticket Bot
A premium Discord ticket bot with dropdown system, private tickets, transcripts, and dynamic branding.


<p align="center">
  <img src="https://media.discordapp.net/attachments/1487308929795883089/1490001952564580595/standard.gif" width="500">
</p>

<p align="center">
  ⚡ Premium Ticket System • Fast • Secure • Customizable ⚡
</p>

---
🚀 Features
🎯 Dropdown ticket system (Support, Bug, Purchase, Other)
🔒 Private ticket channels (user + staff only)
📜 Transcript logs
🎨 Stylish panel UI with banner
⚡ Fast & optimized
🔁 24/7 hosting with PM2
🏷️ Custom bot name using `.env`
---
📦 Requirements
Python 3.11
Node.js (for PM2)
Discord Bot Token
---
⚙️ FULL INSTALL GUIDE
1. Update system
```bash
apt update && apt upgrade -y
```
---
2. Install Python 3.11
```bash
apt install -y build-essential wget libssl-dev zlib1g-dev libncurses5-dev libreadline-dev libsqlite3-dev libgdbm-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev

cd /tmp
wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz
tar -xvf Python-3.11.9.tgz
cd Python-3.11.9

./configure --enable-optimizations
make -j$(nproc)
make altinstall
```
---
3. Upload / Clone bot files
```bash
git clone https://github.com/AstroVoidHostDev/TicketBot
cd TicketBot
```
---
4. Create virtual environment
```bash
python3.11 -m venv myenv
source myenv/bin/activate
```
---
5. Install dependencies
```bash
pip install -U pip
pip install discord.py python-dotenv
pip install -r requirements.txt
```
---
6. Create .env file
```bash
nano .env
```
Paste:
```env
BOT_TOKEN=your_discord_bot_token
TICKET_BOT_NAME=ticketbot
```
---
7. Run bot # Only For Checking..
```bash
python bot.py
```
---
🤖 DISCORD SETUP
Enable Intents:
Message Content Intent ✅
Server Members Intent ✅
---
Run setup command:
```
/setup
```
Select:
Category (tickets)
Log Channel
---
Send panel:
```
.panel
```
---
🔥 PM2 (24/7 HOSTING) # Use This For Start Bot
Install PM2
```bash
npm install -g pm2
```
Start bot
```bash
pm2 start bot.py --name ticket-bot --interpreter ./myenv/bin/python
```
Save
```bash
pm2 save
```
Auto start
```bash
pm2 startup
```
(copy command and run)
---
📊 PM2 COMMANDS
```bash
pm2 list
pm2 logs ticket-bot
pm2 restart ticket-bot
pm2 stop ticket-bot
pm2 delete ticket-bot
```
---
📁 FILE STRUCTURE
```
project/
 ├── bot.py
 ├── config.json
 ├── .env
 └── myenv/
```
---
⚠️ FIX ERRORS
Setup nahi hua
→ Run `/setup`
Missing Permissions
→ Give bot:
Send Messages
Manage Channels
Embed Links
Token Error
→ Check `.env`
---
💎 CUSTOMIZATION
Change name:
```
TICKET_BOT_NAME=yourname
```
Change banner:
Edit in bot.py:
```python
embed.set_image(url="your_url")
```
---
🔥 DONE
Your bot is now fully working 💀🔥

Made With ❤️ ITZ_YTANSH

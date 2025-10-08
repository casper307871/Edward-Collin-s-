Edward Admin Bot v7

Edward Admin Bot is a Telegram admin bot designed for full group moderation, including GBAN, FBAN, CASBAN, shadowbans, and absolute protection for priority users. This bot automatically enforces rules across all preloaded groups and federation groups.

Built with Python and python-telegram-bot >=20.0.

📂 Repository Structure

EdwardAdminBot/
│
├── LICENSE
├── README.md
├── requirements.txt
├── config.py
├── bot.py
├── data.json
├── event_logs.txt
├── utils/
│   ├── __init__.py
│   ├── db_utils.py
│   ├── logger.py
│   ├── protection.py
│   ├── enforcement.py
│   ├── founders.py
│   └── rescue.py
└── handlers/
    ├── __init__.py
    ├── general.py
    ├── founder_commands.py
    ├── bans.py
    └── messages.py




⚙️ Setup
	1.	Clone the repository:

git clone <repo_url>
cd EdwardAdminBot


	2.	Install dependencies:

pip install -r requirements.txt


	3.	Configure bot token:
Edit config.py and replace YOUR_BOT_TOKEN_HERE with your Telegram bot token.
	4.	Run the bot:

python bot.py





🤖 Commands

General

Command	Description
/start	Check if bot is running
/help	Show this help message
/whois <user_id>	Lookup user info
/history <user_id>	Show recent administrative actions

Founder Tools

Command	Description
/panel	Show ban counts, founders, and group stats
/addfounder <user_id>	Add a dynamic founder
/removefounder <user_id>	Remove a dynamic founder
/founders	List all founders
`/secure on	off`
/logs	Show recent logs
/protect <user_id>	Protect user from any bans/mutes
/unprotect <user_id>	Remove protection
/protectedlist	List all protected users

Ban Management

Command	Description
/gban <user_id> [reason]	Global ban across all enforced groups
/ungban <user_id>	Remove global ban
/fban <user_id> [reason]	Federation ban across all federation groups
/unfban <user_id>	Remove federation ban
/shadowban <user_id>	Silently delete user messages in enforced groups
/unshadowban <user_id>	Remove shadowban
/casban <user_id>	Remove admin + ban user in all enforced groups




🔐 Features
	•	Absolute Protection: Users under protection cannot be banned, muted, or restricted by any admin, bot, or system.
	•	Auto Rescue: Protected users are automatically unbanned/unmuted if affected.
	•	Enforced Groups: Preloaded with default channels/groups to monitor and enforce rules.
	•	Founder Privileges: Founders have full access across all groups enforced by Edward.
	•	Logging & History: Maintains action logs and user histories for auditing.
	•	MIT Licensed: Fully open source and modifiable under MIT License.







📝 License

This project is licensed under the MIT License – see LICENSE file for details.
?

# CheckerBot

CheckerBot is an automated Python bot that checks if a university has uploaded new exam results and instantly sends the result files to a specified Telegram chat for students.

## Features
- **Automated Exam Result Detection:** Periodically monitors the university’s exam results page for new uploads.
- **Telegram Notifications:** Forwards new exam result files directly to a Telegram group or chat.
- **Error Handling & Logging:** Logs errors and notifies the administrator via Telegram for quick troubleshooting.
- **Workday Scheduling:** Restricts checks to working hours and weekdays (Asia/Yerevan timezone).

## Technologies Used
- Python
- Playwright (web automation)
- BeautifulSoup (HTML parsing)
- pyTelegramBotAPI / telebot (Telegram bot)
- pytz (timezone management)
- asyncio (asynchronous operations)

## Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/vanyan12/CheckerBot.git
   cd CheckerBot
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure the bot:**
   - Replace `<BOT_TOKEN>` in `test_main.py` with your Telegram bot token.
   - Set your Telegram user ID for admin notifications.
4. **Run the bot:**
   ```bash
   python test_main.py
   ```

## Configuration
- **Result Files Directory:** By default, files are saved/sent from the `Files` directory in the project root.
- **Admin Notifications:** Update the admin Telegram ID in `test_main.py` to receive error alerts.

## Contributing
Contributions and suggestions are welcome! Please open an issue or submit a pull request.

## License
MIT License

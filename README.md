# tgbot

A Telegram bot made with Pyrogram

## Requirements

- Python 3.6 or higher
- A [Telegram API key](//docs.pyrogram.org/intro/setup#api-keys)
- A [Telegram bot token](//t.me/botfather)

## Run

1. `virtualenv venv` to create a virtual environment
2. `venv/bin/pip install -U -r requirements.txt` to install the requirements
3. Copy the configuration files and replace the values with your own
   ```
   cp tgbot/config{_example,}.ini
   cp tgbot/config{_example,}.py
   ```
4. Run with `venv/bin/python -m tgbot`
5. Stop with <kbd>CTRL+C</kbd>

## License

GPL-3.0-or-later

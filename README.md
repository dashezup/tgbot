# tgbot

A collection of Pyrogram Smart Plugins for Telegram bots, made with
[Pyrogram Smart Plugins](https://docs.pyrogram.org/topics/smart-plugins)

- Some of the plugins are used in [@ezupdevbot](https://t.me/ezupdevbot)
  (exclusive use in Dash's groups)
- `media.music` plugin is ported to the Heroku deployment friendly project
  [tgmusicbot](https://github.com/callsmusic/tgmusicbot)

## Plugins

| Plugin                   | Description                                                |
|--------------------------|------------------------------------------------------------|
| `admin.call-adimn`       | @admin in groups                                           |
| `captcha.emoji_buttons`  | 4 random emojis for group CAPTCHA                          |
| `captcha.one_button`     | one button for group CAPTCHA                               |
| `media.music`            | download music from YouTube/SoundCloud/Mixcloud            |
| `media.ytdl_with_button` | download videos from various sites                         |
| `vcsets.notes`           | notes for Telegram group @VCSets                           |
| `commands`               | some commands such like `!start` and `!help`               |
| `pin`                    | /pin a message and open a poll for loud pin                |
| `ping`                   | reply to ping with pong for checking if the bot was online |

## Requirements

- Python 3.6 or higher (some plugins may require higher versions)
- A [Telegram API key](https://docs.pyrogram.org/intro/setup#api-keys)
- A [Telegram bot token](https://t.me/botfather)

## Run

1. `virtualenv venv` to create a virtual environment
2. install `python3-devel zlib-devel libjpeg-turbo-devel libwebp-devel`, clear
   cache of pip (`~/.cache/pip` on linux distro)
   for building wheel for Pillow.
   `venv/bin/pip install -U -r requirements.txt` to install the requirements
3. Create a new `config.ini` file, copy-paste the following and replace the
   values with your own. Exclude or include plugins to fit your needs.
   Create `config.py` and add constants that are specified in module docstrings
   of enabled plugins.
   ```
   [pyrogram]
   api_id = 1234567
   api_hash = 0123456789abcdef0123456789abcdef
   bot_token = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

   [plugins]
   root = plugins
   exclude = welcome
   ```
4. Run with `venv/bin/python tgbot.py`
5. Stop with <kbd>CTRL+C</kbd>

## License

AGPL-3.0-or-later

```
tgbot, a collection of Pyrogram Smart Plugins for Telegram bots
Copyright (C) 2021  Dash Eclipse

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

# plugins/ping.py
PING_DELAY_DELETE = 4

# plugins/welcome.py
# int | str | list
WELCOME_CHATS = -1234567891012
WELCOME_DELAY_KICK_MIN = 2

# plugin/music
MUSIC_CHATS = [
    -1234567891012,
    -2345678910123
]
MUSIC_USERS = [1234567890]
MUSIC_DELAY_DELETE_INFORM = 10
MUSIC_INFORM_AVAILABILITY = (
    "This bot only serves the specified group and"
    "its members in private chat"
)
MUSIC_MAX_LENGTH = 10800

# plugins/commands.py
COMMANDS_CHATS = MUSIC_CHATS
COMMANDS_TEXT_START = (
    "This is a music downloader bot for "
    "members of the channel and group"
)
COMMANDS_TEXT_CONTACTS = (
    "Regarding any issues with the bot "
    "feel free to contact"
)
COMMANDS_TEXT_HELP = (
    MUSIC_INFORM_AVAILABILITY
    + "\n\n<b>Usage</b>:\n"
    "- Send a message that only contains a YouTube/SoundCloud/Mixcloud link "
    "to download the music\n"
    "- Playlists are not supported\n"
    "- Your message will be deleted in private chat after the music gets "
    "successfully uploaded\n"
    "- You can get YouTube links with inline bot @vid\n\n"
    + COMMANDS_TEXT_CONTACTS
)

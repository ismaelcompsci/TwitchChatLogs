import errno
import json
import logging
import logging.handlers
import os
import re
from datetime import datetime
from uuid import UUID
from dotenv import load_dotenv

import emoji
from pydantic import BaseModel, Field
from twitchio.ext import commands

load_dotenv()


class Tags(BaseModel):
    badge_info: str
    badges: str
    client_nonce: str = None
    color: str
    display_name: str
    emotes: str
    first_msg: int
    flags: str
    id: UUID
    mod: int
    returning_chatter: int
    room_id: int
    subscriber: int
    tmi_sent_ts: str
    turbo: int
    user_id: int
    user_type: str


class TwitchChat(BaseModel):
    text: str
    username: str
    display_name: str
    channel: str
    timestamp: datetime
    id: UUID
    type: int
    raw: str
    tags: Tags


FILE_LOG_DIR = "D:/_Logs"
TIKTOK_REGEX = r"\bhttps?:\/\/(?:m|www|vm)\.tiktok\.com\/\S*?\b(?:(?:(?:usr|v|embed|user|video)\/|\?shareId=|\&item_id=)(\d+)|(?=\w{7})(\w*?[A-Z\d]\w*)(?=\s|\/$))\b"
REMOVE_FILES = ["_only_channel", "_links", "_error_logs"]

OAUTHTOKEN = os.getenv("OAUTHTOKEN")
CHANNELS_TO_LOG = [
    "slwalekop",
    "xqc",
    "dizzy",
    "jessesmfi",
    "forsen",
    "xqcisoffline",
    "pokelawls",
    "hasanabi",
    "sodapoppin",
    "summit1g",
    "trainwreckstv",
    "kaicenat",
    "robcdee",
]


filedirec = FILE_LOG_DIR


def dir_make(filedirec):
    # creating seperate directories for logs Code reference: https://stackoverflow.com/a/12517490
    if not os.path.exists(os.path.dirname(filedirec)):
        try:
            os.makedirs(os.path.dirname(filedirec))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


log_file = filedirec + "/_error_logs/" + "chat.log"
dir_make(log_file)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="%Y-%m-%d_%H:%M:%S",
    handlers=[
        logging.handlers.TimedRotatingFileHandler(
            log_file,  # Active log name
            when="M",
            interval=600,  # Log rotation in min.
            encoding="utf-8",
        )
    ],
)


class Bot(commands.Bot):
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(
            token=OAUTHTOKEN,
            prefix="?",
            initial_channels=CHANNELS_TO_LOG,
        )

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # serialize_msg = {
        #     "timestamp": message.timestamp.strftime("%Y-%m-%d_%H:%M:%S"),
        #     "channel": message.channel.name,
        #     "author": message.author.name,
        #     "message": message.content,
        #     "author_display_name": message.author.display_name,
        #     "author_badges": message.author.badges,
        #     "author_is_mod": message.author.is_mod,
        #     "author_is_subscriber": message.author.is_subscriber,
        #     "author_is_vip": message.author.is_vip,
        #     "author_prediction": message.author.prediction,
        #     "author_first_msg": message.first,
        #     "message_raw_data": message.raw_data,
        # }
        t = message.tags
        # t["badge-info"] = t.pop("@badge-info")

        tags = Tags(
            badge_info=t["@badge-info"],
            badges=t["badges"],
            client_nonce=t.get("client-nonce", None),
            color=t["color"],
            display_name=t["display-name"],
            emotes=t["emotes"],
            first_msg=t["first-msg"],
            flags=t["flags"],
            id=t["id"],
            mod=t["mod"],
            returning_chatter=t["returning-chatter"],
            room_id=t["room-id"],
            subscriber=t["subscriber"],
            tmi_sent_ts=t["tmi-sent-ts"],
            turbo=t["turbo"],
            user_id=t["user-id"],
            user_type=t["user-type"],
        )

        chat = TwitchChat(
            text=emoji.demojize(message.content),
            username=message.author.name,
            display_name=message.author.display_name,
            channel=message.channel.name,
            timestamp=message.timestamp,
            id=message.id,
            type=1,
            raw=message.raw_data,
            tags=tags,
        )

        self.log_channel_user(message, chat)
        self.log_channel(message, chat)
        self.tiktok_links(message, chat)

    def log_channel(self, message, chat):
        channel = message.channel.name
        year = message.timestamp.year
        month = message.timestamp.month
        day = message.timestamp.day

        dir_ = self.make_dir(channel, year, month, day, log_user=False)

        filename = channel + ".txt"

        with open(dir_ + filename, "a") as f:
            f.write(chat.json() + "\n")

    def log_channel_user(self, message, chat):
        channel = message.channel.name
        year = message.timestamp.year
        month = message.timestamp.month

        dir_ = self.make_dir(channel, year, month, log_user=True)

        filename = message.author.name + ".txt"
        with open(dir_ + filename, "a") as f:
            f.write(chat.json() + "\n")

    def make_dir(self, channel, year, month, day=None, log_user=False):
        if log_user == False:
            dir_filename = f"{filedirec}/_only_channel/{channel}/{year}/{month}/{day}/"
        else:
            dir_filename = f"{filedirec}/{channel}/{year}/{month}/"
        # print(dir_filename)
        self.create_dir(dir_filename)

        return dir_filename

    def create_dir(self, pathname):
        if not os.path.exists(os.path.dirname(pathname)):
            try:
                os.makedirs(os.path.dirname(pathname))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def tiktok_links(self, message, chat):
        link = re.findall(TIKTOK_REGEX, message.content)
        if link:
            dir_ = f"{filedirec}/_links/{message.channel.name}/{message.timestamp.year}/{message.timestamp.month}/"
            self.create_dir(dir_)

            filename = dir_ + message.channel.name + ".txt"
            with open(filename, "a") as f:
                f.write(chat.json() + "\n")
        return


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.

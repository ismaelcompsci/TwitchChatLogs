import datetime
import json
from re import X

from fastapi import FastAPI, HTTPException


from .models import *
import time

from .constants import FILE_LOG_DIR, REMOVE_FILES
import os


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} {end-start:.4f}s")
        return result

    return wrapper


# @timer
def read_channel_logs(
    channel: str, year: str = None, month: str = None, day: str = None
) -> ChannelLog | UserLog:
    """
    Read channel logs for the day or the specified day
    """
    today = datetime.now()
    year = year or today.year
    month = month or today.month
    day = day or today.day

    filename = (
        f"{FILE_LOG_DIR}/_only_channel/{channel}/{year}/{month}/{day}/{channel}.txt"
    )

    return reader(filename, ChannelLog)


def read_user_chatlogs(
    channel: str,
    username: str,
    year: str = None,
    month: str = None,
    reverse: bool = False,
) -> ChannelLog | UserLog:
    """
    Read user chatlogs at specified channel and or specified data year/month
    """
    today = datetime.now()
    year = year or today.year
    month = month or today.month

    filename = f"{FILE_LOG_DIR}/{channel}/{year}/{month}/{username}.txt"
    data = reader(filename, UserLog)

    if reverse:
        data.messages.reverse()
    return data


def list_of_logged_channels() -> ChannelsLogged:
    files = os.listdir(FILE_LOG_DIR)

    for file in REMOVE_FILES:
        files.remove(file)

    channels = []
    for file in files:
        channels.append(Channel(username=file))

    return ChannelsLogged(channels=channels)


def channel_logged_list(channel: str) -> ChannelLogList:
    """ """
    directory_name = FILE_LOG_DIR + f"/_only_channel/{channel}"

    channels = []

    for root, dirs, files in os.walk(directory_name):
        for name in files:
            _, year, month, day = root.split("\\")

            channels.append(ChannelLogFiles(year=year, month=month, day=day))

    return ChannelLogList(logs=channels)


def channel_logs_users_list(channel: str, reversed: bool) -> ChannelLogList:
    dir_ = FILE_LOG_DIR + f"/{channel}"

    dates = []

    for direc in os.listdir(dir_):
        for subdir in os.listdir(dir_ + "\\" + direc):
            dates.append(ChannelLogFiles(year=direc, month=subdir))

    if reversed:
        dates.reverse()
        return ChannelLogList(logs=dates)
    return ChannelLogList(logs=dates)


def get_channel_tiktoks(channel: str):
    today = datetime.now()
    year = today.year
    month = today.month

    dir_ = FILE_LOG_DIR + f"/_links/{channel}/{year}/{month}/{channel}.txt"
    data = reader(dir_, None)
    data.reverse()

    return data


# @timer
def reader(file, obj_output: ChannelLog | UserLog | None) -> ChannelLog | UserLog:
    """
    load every line as a python dict

    """
    content = []
    buff = 65536

    try:
        with open(file, "r") as f:
            while True:
                lines = f.readlines(buff)
                if not lines:
                    break
                for line in lines:
                    message = json.loads(line)
                    content.append(build_message(message))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail="No Logs Found")

    if not obj_output:
        return content
    return obj_output(messages=content)


def build_message(message: str) -> TwitchChat:

    t = message["tags"]
    tags = Tags(
        badge_info=t["badge_info"],
        badges=t["badges"],
        client_nonce=t["client_nonce"],
        color=t["color"],
        display_name=t["display_name"],
        emotes=t["emotes"],
        first_msg=t["first_msg"],
        flags=t["flags"],
        id=t["id"],
        mod=t["mod"],
        returning_chatter=t["returning_chatter"],
        room_id=t["room_id"],
        subscriber=t["subscriber"],
        tmi_sent_ts=t["tmi_sent_ts"],
        turbo=t["turbo"],
        user_id=t["user_id"],
        user_type=t["user_type"],
    )

    chat = TwitchChat(
        text=message["text"],
        username=message["username"],
        display_name=message["display_name"],
        channel=message["channel"],
        timestamp=message["timestamp"],
        id=message["id"],
        type=message["type"],
        raw=message["raw"],
        tags=tags,
    )

    return chat

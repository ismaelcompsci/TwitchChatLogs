from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, Params, add_pagination, paginate
from .models import *
from fastapi.middleware.cors import CORSMiddleware


from .utils import (
    channel_logged_list,
    list_of_logged_channels,
    read_channel_logs,
    read_user_chatlogs,
    channel_logs_users_list,
    get_channel_tiktoks,
)


app = FastAPI(docs_url="/", redoc_url=None)

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/channel/{channel}")
def channel(channel: str) -> ChannelLog:
    """
    Get Chat logs of the entire day
    """
    return read_channel_logs(channel)


@app.get("/channel/{channel}/{year}/{month}/{day}")
def channel_year_month_day(channel: str, year: str, month: str, day: str) -> ChannelLog:
    """
    Get Chat logs of the specified date
    """
    try:
        return read_channel_logs(channel, year, month, day)
    except Exception as e:
        raise HTTPException(status_code=404, detail="No Logs Found")


@app.get("/channel/{channel}/username/{username}")
def user(channel: str, username: str) -> UserLog | dict:
    """
    Get User Chat logs for the current month on specified channel
    """
    # try:
    return read_user_chatlogs(channel, username)
    # except Exception as e:
    #     print(e)
    #     raise HTTPException(status_code=404, detail="No Logs Found")


@app.get("/channel/{channel}/username/{username}/{year}/{month}")
def user_year_month(
    channel: str, username: str, year: str, month: str, reverse: bool = False
) -> UserLog:
    """
    Get user chat logs for the month on specified channel with year and month
    """
    try:

        return read_user_chatlogs(channel, username, year, month, reverse)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=204, detail="No Logs Found")


@app.get("/list/all/channel/{channel}")
def channel_logs_available(channel: str) -> ChannelLogList:
    """
    Gets available dates of all specified channel logs
    """
    try:
        return channel_logged_list(channel)
    except Exception as e:
        raise HTTPException(status_code=404, detail="No logs Found")


@app.get("/list/all/channel/{channel}/users")
def channel_logs_users(channel: str, reverse: bool | None = None) -> ChannelLogList:
    """
    Gets available dates of user logs on channel
    """
    # example:
    #     logs: [
    #     {year: "2023", month: "2"},
    #     {year: 2023", month: "3"}
    #     ]
    try:
        return channel_logs_users_list(channel, reverse)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Channel not being logged")


@app.get("/list/channels/")
def logged_channel() -> ChannelsLogged:
    """
    Gets list of logged channels
    """
    try:
        return list_of_logged_channels()
    except Exception as e:
        raise HTTPException(status_code=404, detail="No Logs Found")


@app.get("/tikoks/channel/{channel}", response_model=Page[TwitchChat])
def channel_tiktoks(channel: str):
    return paginate(get_channel_tiktoks(channel))


add_pagination(app)

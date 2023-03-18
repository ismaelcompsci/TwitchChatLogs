from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# class AuthorBadges(BaseModel):
#     subscriber: Optional[int] = None
#     moments: Optional[int] = None
#     bits: Optional[int] = None
#     vip: Optional[int] = None
#     no_audio: Optional[int] = None
#     turbo: Optional[int] = None


# class Message(BaseModel):
#     timestamp: str
#     channel: str
#     author: str
#     message: str
#     author_display_name: str
#     author_badges: Optional[AuthorBadges] = None
#     author_is_mod: bool
#     author_is_subscriber: bool
#     author_is_vip: bool
#     author_prediction: Optional[str] = None
#     author_first_msg: bool
#     message_raw_data: str


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


class ChannelLogFiles(BaseModel):
    year: str
    month: str
    day: Optional[str] = None


class ChannelLogList(BaseModel):
    logs: list[ChannelLogFiles]


class Channel(BaseModel):
    username: str


class ChannelsLogged(BaseModel):
    channels: list[Channel]


class ChannelLog(BaseModel):
    messages: list[TwitchChat]


class UserLog(BaseModel):
    messages: Optional[list[TwitchChat]] = None

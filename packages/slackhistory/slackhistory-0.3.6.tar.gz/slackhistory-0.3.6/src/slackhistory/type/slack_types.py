from abc import abstractmethod
from dataclasses import dataclass, field, fields
from logging import getLogger
import json
from typing import Self

logger = getLogger(__name__)


class BaseDataClass:
    '''
    Some helper funcion for dataclasses
    '''

    def to_dict(self) -> dict:
        result: dict = {}
        for k, v in self.__dict__.items():
            to_dict = getattr(v, "to_dict", None)
            if callable(to_dict):
                result[k] = v.to_dict()
            elif isinstance(v, list):
                temp_list: list = []
                for i in v:
                    to_dict = getattr(i, "to_dict", None)
                    if callable(to_dict):
                        temp_list.append(i.to_dict())
                    else:
                        temp_list.append(i)
                result[k] = temp_list
            else:
                result[k] = v
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, inpt: dict) -> Self:
        tmp_dict = {}
        for f in fields(cls):  # type: ignore
            if value := inpt.get(f.name, None):
                tmp_dict[f.name] = value
        return cls(**tmp_dict)


@dataclass
class Replies(BaseDataClass):
    '''
    Slack api responses with a list of messages.
    Replies starts on the second element
    ex:
        [message, reply_1, reply_2 ...]
    '''
    ok: bool
    messages: list[dict] = field(default_factory=list)

    @property
    def reply_list(self) -> list[dict]:
        return self.messages[1:]


@dataclass
class Channel(BaseDataClass):
    id: str = ""
    name: str = ""


@dataclass
class ChannelResponseMetadata(BaseDataClass):
    next_cursor: str = ""


@dataclass
class ChannelList(BaseDataClass):
    ok: bool
    response_metadata: ChannelResponseMetadata = field(
        default_factory=ChannelResponseMetadata)
    channels: list[Channel] = field(default_factory=list)

    @classmethod
    def from_dict(cls, inpt: dict) -> Self:
        tmp_dict = {}
        for f in fields(cls):
            if value := inpt.get(f.name, None):
                if f.name == "channels":
                    tmp_dict[f.name] = [
                        Channel.from_dict(i) for i in inpt["channels"]
                    ]
                elif f.name == "response_metadata":
                    tmp_dict[f.name] = ChannelResponseMetadata.from_dict(
                        inpt["response_metadata"])
                else:
                    tmp_dict[f.name] = value
        return cls(**tmp_dict)


@dataclass
class ChannelHistory(BaseDataClass):
    ok: bool
    has_more: bool = False
    oldest: str = ""
    messages: list[dict] = field(default_factory=list)


@dataclass
class MessageAndReplies(BaseDataClass):
    msg: dict = field(default_factory=dict)
    replies: list[dict] = field(default_factory=list)


@dataclass
class SlackMessageAndReply(BaseDataClass):
    ok: bool
    channel_name: str = ""
    channel_id: str = ""
    start_date: str = ""
    start_ts: str = ""
    end_date: str = ""
    end_ts: str = ""
    messages: list[MessageAndReplies] = field(default_factory=list)

    @classmethod
    def from_dict(cls, inpt: dict) -> Self:
        tmp_dict = {}
        for f in fields(cls):
            if value := inpt.get(f.name, None):
                if f.name == "messages":
                    tmp_dict[f.name] = [
                        MessageAndReplies.from_dict(i) for i in inpt["messages"]
                    ]
                else:
                    tmp_dict[f.name] = value
        return cls(**tmp_dict)


@dataclass
class CacheTypes(BaseDataClass):
    channel_list: bool = False
    channel_history: bool = False
    message_replies: bool = False


@dataclass
class CacheSetting(BaseDataClass):
    active: bool = False
    cache_path: str = "/tmp"
    cache_prefix: str = ""
    cache: CacheTypes = field(default_factory=CacheTypes)

    @classmethod
    def from_dict(cls, inpt: dict) -> Self:
        tmp_dict = {}
        for f in fields(cls):
            if value := inpt.get(f.name, None):
                if f.name == "cache":
                    tmp_dict[f.name] = CacheTypes.from_dict(inpt["cache"])
                else:
                    tmp_dict[f.name] = value
        return cls(**tmp_dict)

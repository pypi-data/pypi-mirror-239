from asyncio import Event, Task, create_task, sleep
from dataclasses import field
from logging import getLogger
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse

from ..log.log import TRACE
from ..type.slack_types import CacheSetting, ChannelHistory, ChannelList, MessageAndReplies, Replies, SlackMessageAndReply
from datetime import datetime

logger = getLogger(__name__)


class SlackHelper:
    """
    Get messages and reply after a set date
    """
    _date_format: str = '%Y-%m-%d %H:%M:%S'

    def __init__(
        self,
        token: str,
        cache_setting: CacheSetting = field(default_factory=CacheSetting)
    ) -> None:
        self._token: str = token
        self._slack_client = AsyncWebClient(token=self._token)
        # TODO Slack limits api requests, having a caching system would be nice
        self._cache = cache_setting

    async def _get_channel_id(self, channel_name: str) -> str:
        logger.log(TRACE, "_get_channel_id")
        channel_list = await self._get_channel_list()
        channel_id = ""
        for channel in channel_list.channels:
            if channel.name == channel_name:
                channel_id = channel.id
                break
        return channel_id

    def _load_cache(self, file: str) -> dict:
        ...

    def _save_cache(self, file: str):
        ...

    async def _get_channel_list(self) -> ChannelList:
        logger.log(TRACE, "_get_channel_list")
        res: AsyncSlackResponse = await self._slack_client.conversations_list(
            types="public_channel,private_channel")
        return ChannelList.from_dict(res.data)  # type: ignore

    async def _get_channel_history(self, channel_id: str, start_date: str,
                                   end_date: str) -> ChannelHistory:
        logger.log(TRACE, "_get_channel_history")
        res: AsyncSlackResponse = await self._slack_client.conversations_history(
            channel=channel_id, oldest=start_date, latest=end_date)
        return ChannelHistory.from_dict(res.data)  # type: ignore

    async def _get_message_reply_list(self, channel_id: str,
                                      ts: str) -> Replies:
        logger.log(TRACE, "_get_message_reply_list")
        res: AsyncSlackResponse = await self._slack_client.conversations_replies(
            channel=channel_id, ts=ts)
        return Replies.from_dict(res.data)  # type: ignore

    def _to_timestamp(self, inpt: str) -> str:
        logger.log(TRACE, "_to_timestamp")
        if not inpt:
            return ""
        date = datetime.strptime(inpt, self._date_format)
        ts = datetime.timestamp(date)
        return str(ts)

    def _get_current_time(self) -> str:
        """Return current time in self._date_format format

        Returns:
            str: current time in self._date_format format
        """
        return datetime.now().strftime(self._date_format)

    async def _get_replies(self,
                           channel_id: str,
                           messages: list[dict],
                           concurrency: bool = True,
                           req_interval: float = 1) -> list[MessageAndReplies]:
        """Finds the replies for our messages

        Args:
            channel_id (str): Slack channel id
            messages (list[dict]): A list of messages
            concurrency (bool, optional): Whether or not to send slack requests concurrently. Defaults to True.
            req_interval (float, optional): Only applies when 'concurrency == False'. Sleep N seconds between requests. Defaults to 1.

        Returns:
            list[MessageAndReplies]: Return messages + replies
        """
        logger.log(TRACE, "_convert")

        async def _update_reply(msg_and_reply: MessageAndReplies,
                                channel_id: str, ts: str, event: Event):
            result = await self._get_message_reply_list(channel_id, ts)
            msg_and_reply.replies = result.messages[1:]
            event.set()

        event_list: list[Event] = []
        result: list[MessageAndReplies] = []

        for msg in messages:
            if msg.get("reply_count", 0) > 0:
                if concurrency:
                    event = Event()
                    msg_and_reply = MessageAndReplies(msg=msg)
                    create_task(
                        _update_reply(msg_and_reply, channel_id, msg["ts"],
                                      event))
                    event_list.append(event)
                    result.append(msg_and_reply)
                else:
                    # request one at a time to prevent exceeding slack api request limit
                    msg_and_reply_list = await self._get_message_reply_list(
                        channel_id, msg["ts"])
                    result.append(
                        MessageAndReplies(
                            msg=msg, replies=msg_and_reply_list.messages[1:]))
                    logger.log(TRACE, "sleep for %s", req_interval)
                    await sleep(req_interval)
            else:
                result.append(MessageAndReplies(msg=msg))

        for event in event_list:
            await event.wait()

        return result

    async def get_message_and_replies(
            self,
            channel_name: str,
            start_date: str,
            end_date: str = "",
            concurrency: bool = True,
            req_interval: float = 1) -> SlackMessageAndReply:
        """Returns messages and replies between a set date

        Args:
            channel_name (str): The channel name
            start_date (str): Example: 2023-10-28 08:00:00
            end_date (str, optional): Example: 2023-10-28 08:00:00
            concurrency (bool, optional): Whether or not to send slack requests concurrently. Defaults to True.
            req_interval (int, optional): Only applies when 'concurrency == False'. Sleep N seconds between requests. Defaults to 1.

        Returns:
            SlackMessageAndReply: Containing messages and replies
        """
        logger.log(TRACE, "get_message_and_replies")
        if not (channel_id := await self._get_channel_id(channel_name)):
            logger.error("channel id not found !!!")
            return SlackMessageAndReply(ok=False)

        start_ts = self._to_timestamp(start_date)
        if not end_date:
            end_date = self._get_current_time()
        end_ts = self._to_timestamp(end_date)

        history = await self._get_channel_history(channel_id=channel_id,
                                                  start_date=start_ts,
                                                  end_date=end_ts)
        messages = await self._get_replies(channel_id, history.messages,
                                           concurrency, req_interval)

        return SlackMessageAndReply(ok=True,
                                    channel_id=channel_id,
                                    channel_name=channel_name,
                                    start_date=start_date,
                                    start_ts=start_ts,
                                    end_date=end_date,
                                    end_ts=end_ts,
                                    messages=messages)

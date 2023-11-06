# Slack History

A Slack helper library to get the history (messages and replies) of a channel


## Installation
```bash
pip install slackhistory
```

## Quick start
```python
import asyncio
from slackhistory import SlackHelper
from slackhistory.type.slack_types import SlackMessageAndReply
from os import environ


async def main():
    slack_helper = SlackHelper(token=environ.get("TOKEN", ""))

    # end_date is optional
    message_and_replies: SlackMessageAndReply = await slack_helper.get_message_and_replies(
        "alex-playground", start_date="2023-10-28 08:00:00", end_date="2023-11-4 22:00:00")

    # the result can be converted to dict or json
    print(message_and_replies.to_dict())
    print(message_and_replies.to_json())


if __name__ == "__main__":
    asyncio.run(main())
```
Example Result: [example_result.json](./examples/example_result.json)

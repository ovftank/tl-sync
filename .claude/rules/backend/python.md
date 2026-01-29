---
paths:
  - "app.py"
  - "**/*.py"
---

# Python Backend - TLSync

## Critical Rules (MUST READ)

**Message sync tool:**

```python
# DON'T - leaks original sender
await event.forward_to(target_chat)

# DO - anonymous + prefix + preserve media
if msg.media:
    await client.send_file(entity=target_chat, file=msg.media,
                          caption=f"{prefix}: {msg.message or ''}",
                          reply_to=topic_id)
else:
    await client.send_message(entity=target_chat,
                             message=f"{prefix}: {msg.message}",
                             reply_to=topic_id)
```

**Message Flow:**

- User → Admin: ONLY forward when `msg.reply_to.forum_topic == True` AND `reply_to_msg_id == user["receive_topicid"]`
- Admin → User: ONLY forward when `msg.reply_to.forum_topic == True` AND `reply_to_msg_id == admin["receive_topicid"]`

**Type Hints (Python 3.10+):**

```python
# DON'T USE (deprecated - PEP 585 & PEP 604)
from typing import List, Dict, Union, Optional
List[int], Dict[str, int], Union[int, str], Optional[int]

# USE (modern)
list[int], dict[str, int], int | str, int | None
```

## External References

- Telethon events details: @.github/TECHNICAL.MD#telethon-event-object
- Message flow diagrams: @.github/TECHNICAL.MD#message-flow-logic
- Config structure: @data.json
- Existing implementation: @app.py

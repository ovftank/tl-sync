# tlsync technical

## telethon event object

```python
event.chat_id              # id nhóm (channel_id)
event.message.id           # id tin nhắn
event.message.message      # nội dung text
event.message.sender_id    # id người gửi (user_id)
event.message.media        # none hoặc media (ảnh, video, file)
event.message.reply_to     # none hoặc MessageReplyHeader
event.message.date         # thời gian gửi
event.message.out          # true nếu tin gửi đi, false nếu tin nhận
```

**check forum topic:**

```python
event.message.reply_to.forum_topic        # true nếu là forum topic
event.message.reply_to.reply_to_msg_id    # topic id được reply
```

**log:**

```text
# tin thường (k reply) - từ admin_group
channel_id=3538180541, user_id=6656772173
reply_to=None
message='admin gửi nè'

# tin thường (k reply) - từ user_group
channel_id=3565628485, user_id=7818631225
reply_to=None
message='không forward nè'

# tin reply vào topic - từ user_group
channel_id=3565628485, user_id=7818631225
reply_to=MessageReplyHeader(
    reply_to_scheduled=False,
    forum_topic=True,        # key: là forum topic
    quote=False,
    reply_to_msg_id=3,       # topic id
    reply_to_peer_id=None,
    reply_from=None,
    reply_media=None,
    reply_to_top_id=None,
    quote_text=None,
    quote_entities=[],
    quote_offset=None,
    todo_item_id=None,
)
message='forward từ user nè'
```

**lưu ý:**

- `event.chat_id` là `channel_id` trong `peer_id`
- `event.message.sender_id` là `user_id` trong `from_id`
- khi user reply topic, `reply_to.forum_topic=true` và `reply_to_msg_id` là topic id
- khi admin gửi tin thường, `reply_to=None`

---

## event object structure

```mermaid
classDiagram
    class Event {
        +int chat_id
        +Message message
    }

    class Message {
        +int id
        +string message
        +int sender_id
        +Media|None media
        +MessageReplyHeader|None reply_to
        +datetime date
        +bool out
    }

    class MessageReplyHeader {
        +bool reply_to_scheduled
        +bool forum_topic
        +bool quote
        +int reply_to_msg_id
        +PeerType|None reply_to_peer_id
        +MessageFwdHeader|None reply_from
        +MessageMedia|None reply_media
        +int|None reply_to_top_id
        +string|None quote_text
        +list quote_entities
        +int|None quote_offset
        +int|None todo_item_id
    }

    Event --> Message : chứa
    Message --> MessageReplyHeader : có thể chứa
```

## message flow logic

```mermaid
flowchart TD
    A[tin nhắn mới] --> B{từ nhóm nào?}

    B -->|user_group| C{kiểm tra reply_to}
    B -->|admin_group| D[tìm config admin]

    C -->|reply_to là None| E[bỏ qua]
    C -->|reply_to tồn tại| F{forum_topic?}

    F -->|false| G[bỏ qua]
    F -->|true| H{topic_id khớp?}

    H -->|không khớp| I[bỏ qua]
    H -->|khớp| J[forward đến admin_group]

    D --> K[gửi đến user_group topic]
```

## config structure

```mermaid
classDiagram
    class ConfigData {
        +dict admin_group
        +dict user_group
    }

    class GroupConfig {
        +int chatid
        +list members
    }

    class Member {
        +int chatid
        +str prefix
        +int topicid
    }

    ConfigData --> GroupConfig : chứa
    GroupConfig --> Member : chứa
```

## message types

```mermaid
flowchart TB
    subgraph Incoming["tin nhắn đến"]
        direction TB
        M1[tin thường<br/>reply_to=None]
        M2[trả lời topic<br/>forum_topic=True]
        M3[trả lời thường<br/>forum_topic=False]
    end

    subgraph Outgoing["tin nhắn đi"]
        direction TB
        M4[bài đăng lịch<br/>reply_to_scheduled=True]
        M5[tin nhắn trực tiếp<br/>out=True]
    end
```

## handler logic detail

```mermaid
flowchart TD
    START[sự kiện NewMessage] --> LOAD[tải config]

    LOAD --> CHECK_CHAT{chat_id == ?}

    CHECK_CHAT -->|user_group.chatid| CHECK_SENDER_1{sender_id trong users?}
    CHECK_CHAT -->|admin_group.chatid| CHECK_SENDER_2{sender_id trong admins?}
    CHECK_CHAT -->|khác| IGNORE[bỏ qua tin nhắn]

    CHECK_SENDER_1 -->|không| IGNORE
    CHECK_SENDER_1 -->|có| CHECK_REPLY_1{reply_to tồn tại?}

    CHECK_REPLY_1 -->|không| IGNORE
    CHECK_REPLY_1 -->|có| CHECK_FORUM{forum_topic == true?}

    CHECK_FORUM -->|không| IGNORE
    CHECK_FORUM -->|có| CHECK_TOPIC{reply_to_msg_id == topicid?}

    CHECK_TOPIC -->|không| IGNORE
    CHECK_TOPIC -->|có| FORWARD_TO_ADMIN[forward đến admin_group<br/>với prefix]

    CHECK_SENDER_2 -->|không| IGNORE
    CHECK_SENDER_2 -->|có| SEND_TO_USER[gửi đến user_group<br/>reply_to=topicid<br/>với prefix]

    FORWARD_TO_ADMIN --> END[xong]
    SEND_TO_USER --> END
    IGNORE --> END
```

---

## docs

- [telethon events reference](https://docs.telethon.dev/en/stable/quick-references/events-reference.html)
- [telethon updates](https://docs.telethon.dev/en/stable/basic/updates.html)
- [telethon concepts entities](https://docs.telethon.dev/en/stable/concepts/entities.html)
- [message fields](https://docs.telethon.dev/en/stable/modules/custom.html)

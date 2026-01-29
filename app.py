import asyncio
import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from telethon import TelegramClient, events

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# @ovftank
TOKEN = ""
API_ID = 0
API_HASH = ""
CONFIG_PATH = Path(__file__).parent / "data.json"

DEFAULT_CONFIG = {"pairs": []}


class Member(BaseModel):
    chatid: int
    prefix: str
    receive_topicid: int | None = None
    send_topicid: int | None = None


class GroupConfig(BaseModel):
    chatid: int
    admins: list[Member] | None = None
    users: list[Member] | None = None


class PairConfig(BaseModel):
    id: str
    name: str
    admin_group: GroupConfig
    user_group: GroupConfig


class ConfigData(BaseModel):
    pairs: list[PairConfig]


def load_config():
    if not CONFIG_PATH.exists():
        save_config(DEFAULT_CONFIG)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    logger.info(f"[CONFIG] Load | pairs={len(cfg.get('pairs', []))}")
    return cfg


def save_config(data: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info(f"[CONFIG] Saved | path={CONFIG_PATH}")


async def forward_message(client, message, target_chat, prefix, reply_to=None):
    if message.media:
        await client.send_file(
            entity=target_chat,
            file=message.media,
            caption=f"{prefix}: {message.message or ''}",
            reply_to=reply_to,
        )
    else:
        await client.send_message(
            entity=target_chat,
            message=f"{prefix}: {message.message}",
            reply_to=reply_to,
        )


async def run_bot():
    client: TelegramClient = TelegramClient("bot_session", API_ID, API_HASH)
    async with client:
        await client.sign_in(bot_token=TOKEN)
        logger.info("[BOT] Started | session=bot_session")

        @client.on(events.NewMessage())
        async def message_handler(event: events.NewMessage.Event):
            try:
                message = event.message

                if message.message.lower() == "gid":
                    chat_type = ""
                    if event.is_private:
                        chat_type = "PRIVATE"
                    elif event.is_channel:
                        if event.chat:
                            if (
                                hasattr(event.chat, "gigagroup")
                                and event.chat.gigagroup
                            ):
                                chat_type = "GIGAGROUP"
                            elif (
                                hasattr(event.chat, "megagroup")
                                and event.chat.megagroup
                            ):
                                chat_type = "SUPERGROUP"
                            elif (
                                hasattr(event.chat, "broadcast")
                                and event.chat.broadcast
                            ):
                                chat_type = "CHANNEL"
                            else:
                                chat_type = "CHANNEL"
                        else:
                            chat_type = "CHANNEL"
                    elif event.is_group:
                        chat_type = "GROUP"

                    response = f"📌 CHAT ID: `{event.chat_id}`\n📋 TYPE: {chat_type}"

                    if (
                        message.reply_to
                        and hasattr(message.reply_to, "forum_topic")
                        and message.reply_to.forum_topic
                    ):
                        topic_id = message.reply_to.reply_to_msg_id
                        response += f"\n🏷️ TOPIC ID: `{topic_id}`"

                    await event.reply(response)
                    logger.info(f"[CMD] gid | chat_id={event.chat_id} type={chat_type}")
                    return

                chat_id = event.chat_id
                if chat_id is None:
                    return
                logger.info(f"[EVENT] NewMessage | chat_id={chat_id} sender_id={message.sender_id}")

                cfg = load_config()
                matched_pairs = []

                for p in cfg.get("pairs", []):
                    if p["user_group"]["chatid"] == chat_id:
                        matched_pairs.append((p, "user"))
                    elif p["admin_group"]["chatid"] == chat_id:
                        matched_pairs.append((p, "admin"))

                if not matched_pairs:
                    logger.info(f"[EVENT] NoMatch | chat_id={chat_id} sender_id={message.sender_id} reason=chatid_not_in_config")
                    return

                for pair, group_type in matched_pairs:
                    logger.info(f"[EVENT] Match | pair={pair['id']} type={group_type} sender_id={message.sender_id}")
                    if group_type == "user":
                        if pair["user_group"]["chatid"] == 0:
                            logger.warning(f"[EVENT] Skip | pair={pair['id']} reason=user_group.chatid=0")
                            continue

                        for user in pair["user_group"]["users"]:
                            if user["chatid"] == message.sender_id:
                                logger.info(f"[EVENT] UserMatch | prefix={user['prefix']} receive_topicid={user.get('receive_topicid')} send_topicid={user.get('send_topicid')}")
                                prefix = user["prefix"]
                                reply_to = user.get("send_topicid") or None

                                if (
                                    not user.get("receive_topicid")
                                    or user["receive_topicid"] == 0
                                ):
                                    await forward_message(
                                        client,
                                        message,
                                        pair["admin_group"]["chatid"],
                                        prefix,
                                        reply_to=reply_to,
                                    )
                                    logger.info(f"[FORWARD] User→Admin (no-filter) | pair={pair['id']} prefix={prefix} reply_to={reply_to} target={pair['admin_group']['chatid']}")
                                elif (
                                    message.reply_to
                                    and hasattr(message.reply_to, "forum_topic")
                                    and message.reply_to.forum_topic
                                    and message.reply_to.reply_to_msg_id
                                    == user["receive_topicid"]
                                ):
                                    await forward_message(
                                        client,
                                        message,
                                        pair["admin_group"]["chatid"],
                                        prefix,
                                        reply_to=reply_to,
                                    )
                                    logger.info(f"[FORWARD] User→Admin (topic-filter) | pair={pair['id']} prefix={prefix} reply_to={reply_to} target={pair['admin_group']['chatid']} topic_id={message.reply_to.reply_to_msg_id}")
                                break

                    elif group_type == "admin":
                        if pair["admin_group"]["chatid"] == 0:
                            logger.warning(f"[EVENT] Skip | pair={pair['id']} reason=admin_group.chatid=0")
                            continue

                        for admin in pair["admin_group"]["admins"]:
                            if admin["chatid"] == message.sender_id:
                                logger.info(f"[EVENT] AdminMatch | prefix={admin['prefix']} receive_topicid={admin.get('receive_topicid')} send_topicid={admin.get('send_topicid')}")
                                prefix = admin["prefix"]
                                reply_to = admin.get("send_topicid") or None

                                if (
                                    not admin.get("receive_topicid")
                                    or admin["receive_topicid"] == 0
                                ):
                                    await forward_message(
                                        client,
                                        message,
                                        pair["user_group"]["chatid"],
                                        prefix,
                                        reply_to=reply_to,
                                    )
                                    logger.info(f"[FORWARD] Admin→User (no-filter) | pair={pair['id']} prefix={prefix} reply_to={reply_to} target={pair['user_group']['chatid']}")
                                elif (
                                    message.reply_to
                                    and hasattr(message.reply_to, "forum_topic")
                                    and message.reply_to.forum_topic
                                    and message.reply_to.reply_to_msg_id
                                    == admin["receive_topicid"]
                                ):
                                    await forward_message(
                                        client,
                                        message,
                                        pair["user_group"]["chatid"],
                                        prefix,
                                        reply_to=reply_to,
                                    )
                                    logger.info(f"[FORWARD] Admin→User (topic-filter) | pair={pair['id']} prefix={prefix} reply_to={reply_to} target={pair['user_group']['chatid']} topic_id={message.reply_to.reply_to_msg_id}")
                                break

            except Exception as e:
                logger.error(f"[ERROR] message_handler | {type(e).__name__}: {e}")

        await client.disconnected


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(run_bot())

    try:
        yield
    finally:
        task.cancel()
        try:
            await asyncio.wait_for(task, timeout=5.0)
        except (asyncio.CancelledError, asyncio.TimeoutError):
            pass


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    cfg = load_config()
    return templates.TemplateResponse("index.html", {"request": request, "config": cfg})


@app.get("/api/config")
async def get_config():
    return load_config()


@app.put("/api/config")
async def update_config(data: ConfigData):
    current = load_config()
    current["pairs"] = [p.model_dump() for p in data.pairs]
    save_config(current)
    logger.info(f"[API] PUT /api/config | pairs={len(current['pairs'])}")
    return current


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=80,
        workers=1,
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )

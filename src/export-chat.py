#!/usr/bin/env python3.12
import datetime
import pathlib
import subprocess

import telethon

root_dir = pathlib.Path(__file__).parents[1]


def get_pass(name: str):
    out = subprocess.run(["pass", "show", name], capture_output=True, text=True).stdout
    return out.rstrip("\n")


session_file = root_dir / "session"

api_id = int(get_pass("tg-api-id"))
api_hash = get_pass("tg-api-hash")

client = telethon.TelegramClient(session_file, api_id, api_hash)


async def main():
    now = datetime.datetime.now()
    print(f"⏰ {now}")
    channel_entity = await client.get_entity("demhack_chat")
    print(channel_entity)


with client:
    client.loop.run_until_complete(main())

#!/usr/bin/env python3.12
import datetime
import pathlib
import subprocess

import telethon
import argparse

from src.module.utils import json_dump

root_dir = pathlib.Path(__file__).parents[1]

argparser = argparse.ArgumentParser()
argparser.add_argument("--output", "-o")
argparser.add_argument("--name", "-n")
args = argparser.parse_args()

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
    out_file_path = pathlib.Path(args.output)
    out_file = out_file_path.open("w")
    counter = 0

    async for item in client.iter_messages(args.name):
        counter += 1
        user = item.from_id.user_id if item.from_id is not None and hasattr(item.from_id, "user_id") else '-'
        line= f"{counter:03} {item.date} {user} {item.message}".replace("\n", "")[:100]
        print(line)
        out_file.write("{}\n".format(json_dump(item.to_dict())))

with client:
    client.loop.run_until_complete(main())

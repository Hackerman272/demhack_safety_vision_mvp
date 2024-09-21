import argparse
import datetime
import pathlib

import telethon
from asyncstdlib import enumerate

from module.utils import get_pass, json_dump

root_dir = pathlib.Path(__file__).parents[1]

argparser = argparse.ArgumentParser()
argparser.add_argument("--output", "-o")
argparser.add_argument("--name", "-n")
args = argparser.parse_args()


session_file = root_dir / "session"

api_id = int(get_pass("tg-api-id"))
api_hash = get_pass("tg-api-hash")

client = telethon.TelegramClient(session_file, api_id, api_hash)


async def main():
    now = datetime.datetime.now()
    print(f"⏰ {now}")
    out_file_path = pathlib.Path(args.output)
    out_file = out_file_path.open("w")

    async for index, item in enumerate(client.iter_messages(args.name)):
        # user = item.from_id.user_id if item.from_id is not None and hasattr(item.from_id, "user_id") else "-"
        # line = f"{counter:03} {item.date} {user} {item.message}".replace("\n", "")[:100]
        # print(line)
        if index % 100 == 0:
            print(index)
        out_file.write("{}\n".format(json_dump(item.to_dict())))


with client:
    client.loop.run_until_complete(main())

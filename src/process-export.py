import argparse
import datetime
import logging
import pathlib
from dataclasses import asdict, dataclass
from signal import SIG_DFL, SIGPIPE, signal
from typing import Generator, TextIO

from autogen import ConversableAgent
from pytimeparse.timeparse import timeparse

from module.config import get_config
from module.export import get_items, get_user
from module.utils import get_pass, indent, json_dump, yaml_dump

signal(SIGPIPE, SIG_DFL)

logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)


argparser = argparse.ArgumentParser()
argparser.add_argument("--input", "-i")
argparser.add_argument("--agent", "-a")
argparser.add_argument("--no-log", action="store_true")
args = argparser.parse_args()

root_dir = pathlib.Path(__file__).parents[1]
config = get_config([root_dir / "config/global.yaml", root_dir / "local.yaml"], root_dir)


def log(log_file: TextIO, text: str):
    print(text)
    if not args.no_log:
        log_file.write(f"{text}\n")


def filter_items(items):
    for item in items:
        if item.from_id.from_type == "PeerChannel":
            continue
        if not item.message:
            continue
        yield item


@dataclass
class MessageChunk:
    userID: str
    text: str
    date: str


def get_messages_chunk(data_path: pathlib.Path) -> Generator[list[MessageChunk], None, None]:
    time_max = timeparse(config.prompt.messages.time_max)
    time_min = timeparse(config.prompt.messages.time_max)

    chunk = []
    start_time = None

    for index, item in enumerate(filter_items(get_items(data_path))):
        start_time = start_time or item.date
        chunk.append(
            MessageChunk(
                userID=get_user(item),
                text=item.message,
                date=item.date.strftime("%Y-%m-%d %H:%M:%S"),
            )
        )

        delta = (item.date - start_time).total_seconds()

        if (
            (len(chunk) >= config.prompt.messages.count_max or delta > time_max)
            and len(chunk) >= config.prompt.messages.count_min
            and delta > time_min
        ):
            yield chunk
            chunk = []
            start_time = None


def get_agent(name: str):
    config_list = {
        "gpt-4": dict(model="gpt-4", api_key=get_pass("openai-api-key")),
        "gemini-pro": dict(model="gemini-pro", api_type="google", api_key=get_pass("gemini-api-key")),
    }

    return ConversableAgent(
        "chatbot",
        llm_config={"config_list": [config_list[name]]},
        # system_message=system_prompt,
        code_execution_config=False,
        function_map=None,
        human_input_mode="NEVER",
    )


def process_messages_chunk(now: datetime.datetime, log_file: TextIO, messages_chunk: list[MessageChunk]):
    prompt_template_path = pathlib.Path(config.root_dir / config.prompt.template)
    prompt = prompt_template_path.read_text().replace('"MESSAGES"', yaml_dump(messages_chunk))

    log(log_file, "---")
    log(log_file, f"date: {now}")
    log(log_file, f"template: {prompt_template_path.stem}")
    log(log_file, "messages:")
    log(log_file, f"  count: {len(messages_chunk)}")
    log(log_file, f"  from: {messages_chunk[0].date}")
    log(log_file, f"  to: {messages_chunk[-1].date}")

    agent = get_agent(args.agent)
    reply = agent.generate_reply(messages=[{"content": prompt, "role": "user"}])
    response = reply["content"]

    log(log_file, f"response: |-\n{indent(response)}")


def process():
    data_path = pathlib.Path(args.input)
    now = datetime.datetime.now()
    name = data_path.stem
    log_file_path = pathlib.Path(config.root_dir / f"tmp/logs/{name}/{args.agent}/{now:%Y-%m-%d-%H-%M-%S}.yaml")
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    log_file = log_file_path.open("w")

    for messages_chunk in get_messages_chunk(data_path):
        process_messages_chunk(now, log_file, messages_chunk)
        break

    print("saved_to: ", log_file_path)


def research_01():
    data_path = pathlib.Path(args.input)
    for index, item in enumerate(filter_items(get_items(data_path))):
        print(item.date, get_user(item), item.message)
        break


def main():
    process()


if __name__ == "__main__":
    main()

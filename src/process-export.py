import argparse
import datetime
import logging
import pathlib
from signal import SIG_DFL, SIGPIPE, signal

from autogen import ConversableAgent

from module.config import get_config
from module.export import get_items, get_user
from module.utils import get_pass, json_dump

signal(SIGPIPE, SIG_DFL)

logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)


argparser = argparse.ArgumentParser()
argparser.add_argument("--input", "-i")
args = argparser.parse_args()

root_dir = pathlib.Path(__file__).parents[1]
config = get_config([root_dir / "config/global.yaml", root_dir / "local.yaml"], root_dir)


def filter_items(items):
    for item in items:
        if not item.message:
            continue
        yield item


def get_messages(limit=10):
    data_path = pathlib.Path(args.input)

    yield "["
    for index, item in enumerate(filter_items(get_items(data_path))):
        line_item = {
            "from:": get_user(item),
            "text": item.message,
            "date": item.date.isoformat(),
        }
        yield "  {}".format(json_dump(line_item))

        if index >= limit:
            break
    yield "]"


def main():
    system_prompt = pathlib.Path(config.root_dir / "data/prompt_safety_vision_0.1.md").read_text()
    messages = "\n".join(get_messages(300))
    prompt = system_prompt.replace("MESSAGES", messages)

    now = datetime.datetime.now()
    print(f"⏰ {now}")

    log_file_path = pathlib.Path(config.root_dir / f"tmp/openai-gpt4-log_{now:%Y-%m-%d-%H-%M-%S}.txt")
    log_file = log_file_path.open("w")

    agent = ConversableAgent(
        "chatbot",
        llm_config={
            "config_list": [
                # dict(model="gpt-4", api_key=get_pass("openai-api-key")),
                dict(model="gemini-pro", api_type="google", api_key=get_pass("gemini-api-key")),
            ]
        },
        # system_message=system_prompt,
        code_execution_config=False,
        function_map=None,
        human_input_mode="NEVER",
    )

    print(messages)
    log_file.write(f"{messages}\n\n")

    reply = agent.generate_reply(messages=[{"content": prompt, "role": "user"}])
    print(reply["content"])
    log_file.write(f"{reply['content']}\n")


if __name__ == "__main__":
    main()

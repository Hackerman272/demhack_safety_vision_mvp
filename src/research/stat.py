import argparse
import json
import pathlib
import re
from collections import Counter
from collections import defaultdict
import datetime
from operator import itemgetter
from typing import Iterator

import matplotlib.pyplot as plt
import numpy as np
import spacy
from nltk.stem.snowball import SnowballStemmer

from module.export import get_items, get_user, ExportItem

argparser = argparse.ArgumentParser()
argparser.add_argument("--input", "-i")
args = argparser.parse_args()

nlp = spacy.load("ru_core_news_sm")
stemmer = SnowballStemmer("russian")


def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def format_date(date_string):
    try:
        return datetime.datetime.fromisoformat(date_string)
    except ValueError:
        return "Invalid Date"


def parse_message_content(message_content):
    if isinstance(message_content, list):
        content = ""
        for part in message_content:
            if isinstance(part, str):
                content += part
            elif isinstance(part, dict) and "text" in part:
                content += part["text"]
        return content.replace("\n", " ").replace("  ", " ")
    else:
        return message_content.replace("\n", " ").replace("  ", " ") or ""


def clean_messages(items: Iterator[ExportItem]):
    output = []
    for item in items:
        if not item.message:
            continue
        date = format_date(item.date)
        item_info = {
            "id": item.id,
            "date": date,
            "actor": get_user(item),
            "content": item.message,
        }
        output.append(item_info)
    return output


def aggregate_messages(messages):
    aggregated_messages = defaultdict(list)
    for message in messages:
        actor = message["actor"] if message["actor"] else "Unknown"
        aggregated_messages[actor].append(message)

    for actor, msgs in aggregated_messages.items():
        aggregated_messages[actor] = sorted(msgs, key=itemgetter("id"))

    return sorted(
        aggregated_messages.items(), key=lambda item: len(item[1]), reverse=True
    )


def print_messages_in_batches(actor, messages, batch_size=5):
    total_messages = len(messages)
    for i in range(0, total_messages, batch_size):
        print(
            f"Actor: {actor}, Messages from {i + 1} to {min(i + batch_size, total_messages)}:"
        )
        for msg in messages[i : i + batch_size]:
            print(
                f" Date: {  msg['date'].strftime('%-d %b %H:%M') }, Content: {msg['content']}"
            )
        print("-" * 40)


def analyze_msg_freq(messages):
    window = 10  # window SMA
    alpha = 0.1  # coef EMA

    times = [msg["date"] for msg in messages]

    time_deltas = np.array(
        [(times[i] - times[0]).total_seconds() for i in range(len(times))]
    )

    messages_per_minute = np.diff(time_deltas, prepend=0)

    def simple_moving_average(values, window):
        sma = np.convolve(values, np.ones(window), "valid") / window
        return np.concatenate((np.zeros(window - 1), sma))

    def exponential_moving_average(values, alpha):
        ema = np.zeros_like(values)
        ema[0] = values[0]
        for i in range(1, len(values)):
            ema[i] = alpha * values[i] + (1 - alpha) * ema[i - 1]
        return ema

    sma = simple_moving_average(messages_per_minute, window)
    ema = exponential_moving_average(messages_per_minute, alpha)

    plt.figure(figsize=(10, 6))

    plt.plot(
        time_deltas / 60 / 60,
        messages_per_minute,
        label="Message Frequency",
        marker="o",
    )
    plt.plot(
        time_deltas / 60 / 60,
        sma,
        label=f"Simple Moving Average (SMA, window={window})",
        linestyle="--",
    )
    plt.plot(
        time_deltas / 60 / 60,
        ema,
        label=f"Exponential Moving Average (EMA, α={alpha})",
        linestyle="--",
    )

    plt.xlabel("Time (seconds since first message)")
    plt.ylabel("Time between messages (hours)")
    plt.legend()
    plt.grid(True)
    plt.title("Message Frequency Analysis")
    plt.show()


def analyze_word_freq(messages, method="lemm", exclude_stopwords=True):
    all_text = " ".join([msg["content"] for msg in messages])

    all_text = re.sub("[^a-zA-Zа-яА-Я]", " ", all_text)
    all_text = " ".join(all_text.split())
    all_text = all_text.strip()

    doc = nlp(all_text)

    if method == "lemm":
        tokens = [
            token.lemma_.lower()
            for token in doc
            if not token.is_punct and not token.is_space
        ]
    elif method == "stem":
        tokens = [
            stemmer.stem(token.text.lower())
            for token in doc
            if not token.is_punct and not token.is_space
        ]
    else:
        tokens = [
            token.text.lower()
            for token in doc
            if not token.is_punct and not token.is_space
        ]

    if exclude_stopwords:
        tokens = [token for token in tokens if token not in nlp.Defaults.stop_words]

    word_freq = Counter(tokens)

    most_common_words = word_freq.most_common(30)

    words, counts = zip(*most_common_words)
    plt.figure(figsize=(12, 6))
    plt.bar(words, counts)
    plt.xticks(rotation=90)
    plt.xlabel("Words")
    plt.ylabel("Freq")
    plt.title(f"Top 30 words ({method})")
    plt.grid(True)
    plt.show()

    print("Top 30 words:")
    for word, count in most_common_words:
        print(f"{word}: {count}")


def main():
    messages = get_items(pathlib.Path(args.input))

    message_info = clean_messages(messages)
    aggregated_messages = aggregate_messages(message_info)

    actor, msgs = aggregated_messages[0]
    # print_messages_in_batches(actor, msgs)

    analyze_msg_freq(msgs)
    analyze_word_freq(msgs, method="lemm")
    analyze_word_freq(msgs, method="stem")


if __name__ == "__main__":
    main()

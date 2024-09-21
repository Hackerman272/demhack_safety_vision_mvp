import argparse
import pathlib

from signal import signal, SIGPIPE, SIG_DFL

from module.export import get_items, get_user

signal(SIGPIPE, SIG_DFL)

argparser = argparse.ArgumentParser()
argparser.add_argument("--input", "-i")
args = argparser.parse_args()


def main():
    data_path = pathlib.Path(args.input)

    counter = 0
    for item in get_items(data_path):
        counter += 1

        line = f"{counter:03} {item.date} {get_user(item)} {item.message}".replace(
            "\n", ""
        )[:100]
        print(line)

        break


if __name__ == "__main__":
    main()

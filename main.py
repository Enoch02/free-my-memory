import argparse
import sys
import psutil
import time


# TODO: add a timer that kills this script after n amount of time
def main():
    parser = argparse.ArgumentParser(
        description="Automagically kill Java processes while using Android Studio on your low memory PC!!"
    )
    parser.add_argument(
        "--delay",
        "-d",
        help="Delay (in secs) to check for pesky Java processes",
        default=5,
        type=int,
    )
    args = parser.parse_args()

    kill_java(delay=args.delay)


def kill_java(delay: int):
    processes = psutil.process_iter()
    count = 0

    while True:
        type_and_erase("Searching for processes...")
        for process in processes:
            if "java" in process.name():
                cpu_percent = psutil.cpu_percent(interval=1)
                if cpu_percent < 15:
                    process.kill()
                    if not psutil.pid_exists(process.pid):
                        count += 1
                else:
                    type_and_erase("Probably working on something serious...")

        if count > 0:
            type_and_erase(f"{count} Java processes killed")
            time.sleep(delay)
        else:
            type_and_erase("None found!")


def type_and_erase(text, delay=0.1):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

    for char in text:
        sys.stdout.write("\b \b")
        sys.stdout.flush()
        time.sleep(delay)


if __name__ == "__main__":
    main()

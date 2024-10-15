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
        default=0,
        type=int,
    )
    args = parser.parse_args()

    while True:
        kill_java(delay=args.delay)


def kill_java(delay: int):
    processes = psutil.process_iter()
    count = 0
    java_processes = list(filter(lambda p: "java" in p.name(), list(processes)))

    if len(java_processes) <= 1:
        type_and_erase("Not enough processes")
        return

    type_and_erase("Searching for processes...")
    try:
        for process in java_processes:
            if "java" in process.name():
                cpu_percent = psutil.cpu_percent(interval=1)

                if cpu_percent < 10:

                    process.kill()
                    count += 1
                else:
                    type_and_erase("Probably working on something serious...")
    except psutil.NoSuchProcess:
        type_and_erase("Java process left peacefully!")

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
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram has ended")
        sys.exit()

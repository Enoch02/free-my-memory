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

    while True:
        type_and_erase("Running...")
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent < 10.0:  # TODO: figure out my typical usage while not building
            kill_java()
            time.sleep(args.delay)
        type_and_erase("Probably working on something serious...")


def kill_java():
    processes = psutil.process_iter()
    count = 0

    type_and_erase("Searching for processes...")
    for process in processes:
        if "java" in process.name():
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent < 5.0: # CPU util might have changed..
                process.kill()
                count += 1
            else:
                type_and_erase("Probably working on something serious...")
                
    if count > 0:
        type_and_erase(f"{count} Java processes killed")
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

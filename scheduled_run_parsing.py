import sys
import time
import schedule
import subprocess
import threading


def run_script(script_name):
    subprocess.run([sys.executable, script_name])


def schedule_script(script_name, times):
    for time_str in times:
        schedule.every().day.at(time_str).do(
            lambda script=script_name: threading.Thread(
                target=run_script, args=(script,)
            ).start()
        )


def main():
    schedule_script('run_parsing.py', ['00:00', '08:00', '16:00'])

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()

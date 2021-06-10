import getpass
import pathlib

from crontab import CronTab


def show_jobs(crons):
    for cron in crons:
        print(cron)


def add_job(crons, command):
    job = crons.new(command=command, comment="linux_battery_notifications")
    job.minute.every(5)
    crons.write()
    print("Cron Added:\n", crons[-1])


if __name__ == "__main__":
    my_crons = CronTab(user=getpass.getuser())

    # file paths
    user_info = "XDG_RUNTIME_DIR=/run/user/$(id -u)"
    cwd = str(pathlib.Path(__file__).parent.absolute())
    python_path = cwd + '/venv/bin/python3'
    main_path = cwd + '/main.py'
    output_path = cwd + '/data/out.txt'

    my_command = " ".join((user_info, python_path, main_path, ">>", output_path))
    add_job(my_crons, my_command)
import getpass

from crontab import CronTab


def delete_jobs(crons, my_comment):
    for job in crons:
        if job.comment == my_comment:
            crons.remove(job)
            crons.write()


def show_jobs(crons, comment):
    for job in crons:
        if job.comment == comment:
            print(job)


if __name__ == "__main__":
    my_crons = CronTab(user=getpass.getuser())
    show_jobs(my_crons, 'linux_battery_notifications')
    delete_jobs(my_crons, 'linux_battery_notifications')

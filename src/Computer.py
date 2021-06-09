import datetime
import os
import re
import subprocess
from datetime import datetime
from datetime import timedelta


class Computer:
    battery_percentage = None
    charging_status = None
    remaining_time = None
    timer = None
    session_status = None

    def __init__(self):
        self.session_mapping = {
            "owner": "Locked",
            "owned": "Unlocked"
        }

    def set_battery_percentage(self):
        battery_data = os.popen('acpi -b').read()
        print("battery_data:", battery_data)
        self.battery_percentage = int(re.search(r'\d{1,3}(?=%)', battery_data).group())
        self.charging_status = re.search(r'Charging|Discharging|Full', battery_data).group()
        self.remaining_time = re.search(r'(?<=, )\d*:\d*:\d*', battery_data).group()

        hh_mm_ss = list(map(int, self.remaining_time.split(":")))
        remaining_timedelta = timedelta(hours=hh_mm_ss[0], minutes=hh_mm_ss[1], seconds=hh_mm_ss[2])
        self.timer = datetime.now() + remaining_timedelta

    def set_session_status(self):
        command = [
            'timeout', '0.01', 'gdbus', 'monitor',
            '-e', '-d', 'com.canonical.Unity',
            '-o', '/com/canonical/Unity/Session'
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        session_data = result.stdout.decode("utf-8")
        self.session_status = self.session_mapping[re.search(r'owned|owner', session_data).group()]

    def __str__(self):
        statement = "{} in {} at {}."
        return statement.format(self.charging_status,
                                self.remaining_time,
                                self.timer.strftime("%I:%M %p")
                                )

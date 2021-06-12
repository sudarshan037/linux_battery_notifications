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
    statement = None

    def __init__(self):
        self.session_mapping = {
            "owner": "Locked",
            "owned": "Unlocked"
        }

    def set_battery_percentage(self):
        battery_data = os.popen('acpi -b').read()
        # battery_data = "Battery 0: Charging, 91%, rate information unavailable"
        print("battery_data:", battery_data)
        self.battery_percentage = int(re.search(r'\d{1,3}(?=%)', battery_data).group())
        self.charging_status = re.search(r'Full|Charging|Discharging', battery_data).group()
        self.remaining_time = re.search(r'(?<=, )\d*:\d*:\d*|rate|Full', battery_data).group()

        if self.remaining_time == "rate" or self.charging_status == "Full":
            self.statement = self.charging_status
        else:
            hh_mm_ss = list(map(int, self.remaining_time.split(":")))
            remaining_timedelta = timedelta(hours=hh_mm_ss[0], minutes=hh_mm_ss[1], seconds=hh_mm_ss[2])
            self.timer = (datetime.now() + remaining_timedelta).strftime("%I:%M %p")
            self.statement = "{} in {} at {}".format(
                self.charging_status,
                self.remaining_time,
                self.timer
            )

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
        return self.statement

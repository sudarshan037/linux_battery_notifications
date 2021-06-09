from notifypy import Notify

from src.Computer import Computer


def send_notification(title, message, icon, audio):
    notification = Notify()
    notification.title = title
    notification.message = message
    notification.icon = icon
    notification.audio = audio
    notification.send()


def notification_manager(computer):
    title = "Battery " + str(computer.battery_percentage) + "%"
    message = computer.__str__()
    icons = "data/icons/"
    audios = "data/sounds/"
    if computer.charging_status == "Charging":
        if computer.battery_percentage == 100:
            icon = icons+"battery_100_1.png"
            audio = audios+"battery_full.wav"
            send_notification(title, message, icon, audio)
        elif computer.battery_percentage > 95:
            icon = icons+"battery_100_1.png"
            audio = audios+"battery_full.wav"
            send_notification(title, message, icon, audio)
    elif computer.charging_status == "Discharging":
        if computer.battery_percentage < 15:
            icon = icons+"battery_100_1.png"
            audio = audios+"battery_full.wav"
            send_notification(title, message, icon, audio)
        elif computer.battery_percentage < 30:
            icon = icons+"battery_100_1.png"
            audio = audios+"battery_full.wav"
            send_notification(title, message, icon, audio)


if __name__ == "__main__":
    dell = Computer()
    dell.set_battery_percentage()
    dell.set_session_status()
    notification_manager(dell)

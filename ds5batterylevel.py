from pydualsense import pydualsense
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw, ImageFont
import threading
import time

font = ImageFont.truetype("arial.ttf", 52)
little_font = ImageFont.truetype("arial.ttf", 40)
init_icon = Image.open("icon.png")


def get_ps5_controller_battery():
    ds = pydualsense()
    try:
        ds.init()
        battery_level = ds.battery
        ds.close()
        return battery_level
    except:
        return None


def create_image(battery_level):
    # Create an image with text showing battery level
    image = init_icon.copy()
    draw = ImageDraw.Draw(image)
    print(str(battery_level))
    if int(battery_level) == 100:
        draw.text((0, 12), f"{str(battery_level)}", font=little_font, fill="white")
    else:
        draw.text((0, 5), f"{str(battery_level)}", font=font, fill="white")
    return image


def update_icon(icon):
    while True:
        battery = get_ps5_controller_battery()
        if battery:
            icon.icon = create_image(battery.Level)
            icon.visible = True
        else:
            icon.visible = False
        time.sleep(10)


def on_quit(icon):
    icon.stop()


def main():
    icon = Icon("ds5 Battery Level", icon=init_icon)
    icon.menu = Menu(MenuItem("Quit", on_quit))
    threading.Thread(target=update_icon, args=(icon,), daemon=True).start()
    icon.run()


if __name__ == "__main__":
    main()

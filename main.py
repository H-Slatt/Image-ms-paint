from PIL import Image
import pyautogui
import keyboard
import pydirectinput
import math
import time


pydirectinput.FAILSAFE = False
pydirectinput.PAUSE = 0
pyautogui.PAUSE = 0

stop_flag = False
scale = 2 #MAX 2 OR BREAKS + SET SIZE OF PAINTPRUSH TO SCALE EG 2px
starting_X = 500
starting_Y = 300

def main():
    global stop_flag
    file_path = "image.jpg"
    image = Image.open(file_path)
    image.save("output.jpg", dpi=(72, 72))
    width, height = image.size


    print("Drawing started. Press F8 to stop.")

    for x in range(width):
        for y in range(height):
            if stop_flag:   
                print("Stopped drawing.")
                return
            r, g, b = get_rgb(image, x, y)
            paint(r, g, b, starting_X + x*scale, starting_Y + y*scale)


def get_rgb(image: Image, x, y):
    r, g, b = image.getpixel((x, y))
    return r, g, b                


def paint(r, g, b, x, y):
    current_colour = get_nearest_colour(r, g, b)
    get_colour(current_colour)
    pyautogui.moveTo(x, y)
    pydirectinput.moveRel(1,1)
    pydirectinput.click(button="left")


def get_nearest_colour(r, g, b):
    colours = {
        "black": (0, 0, 0),
        "grey": (127, 127, 127),
        "dark_red": (128, 0, 0),
        "red": (255, 0, 0),
        "orange": (255, 127, 0),
        "yellow": (255, 255, 0),
        "green": (0, 255, 0),
        "turquoise": (0, 191, 255),
        "indigo": (0, 0, 255),
        "purple": (128, 0, 128),
        "white": (255, 255, 255),
        "light_grey": (192, 192, 192),
        "brown": (139, 69, 19),
        "rose": (255, 105, 180),
        "gold": (255, 215, 0),
        "light yellow": (245, 245, 220)
    }
    closest_colour = None
    min_dist = float("inf")
    for name, (R, G, B) in colours.items():
        dist = (r - R) ** 2 + (g - G) ** 2 + (b - B) ** 2
        if dist < min_dist:
            min_dist = dist
            closest_colour = name
    return closest_colour


def get_colour(colour):
    match colour:
        case "black": pyautogui.moveTo(792, 83)
        case "grey": pyautogui.moveTo(813, 84)
        case "dark_red": pyautogui.moveTo(837, 86)
        case "red": pyautogui.moveTo(868, 87)
        case "orange": pyautogui.moveTo(887, 86)
        case "yellow": pyautogui.moveTo(912, 86)
        case "green": pyautogui.moveTo(930, 86)
        case "turquoise": pyautogui.moveTo(957, 85)
        case "indigo": pyautogui.moveTo(980, 85)
        case "purple": pyautogui.moveTo(1004, 84)
        case "white": pyautogui.moveTo(788, 103)
        case "light_grey": pyautogui.moveTo(816, 106)
        case "brown": pyautogui.moveTo(842, 105)
        case "rose": pyautogui.moveTo(863, 105)
        case "gold": pyautogui.moveTo(886, 106)
        case "light yellow": pyautogui.moveTo(906, 107)
        case _: pyautogui.moveTo(1004, 84)
    pydirectinput.click(button="left")
    return colour


def stop():
    global stop_flag
    stop_flag = True


if __name__ == "__main__":
    # register stop hotkey before main
    keyboard.add_hotkey("f8", stop)
    main()

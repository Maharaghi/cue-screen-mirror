from PIL import Image, ImageEnhance
from cuesdk import CueSdk

import math
import numpy as np
import mss


def get_available_leds():
    leds = list()
    device_count = sdk.get_device_count()
    for device_index in range(device_count):
        led_positions = sdk.get_led_positions_by_device_index(device_index)
        leds.append(led_positions)
    return leds

def scaleImage(img):
    # return img.resize((24, 6), resample=Image.LANCZOS)
    # return img.resize((24, 6), resample=Image.ADAPTIVE)
    return img.resize((24, 6), resample=Image.ANTIALIAS)

def getClosestPoint(c1, keyList):
    closest = 9999999
    targetKey = keyList[0]
    for key in keyList:
        c2 = key[1]
        # Just check distance between 2 xy coordinates
        dist = math.sqrt(abs(c1[0] - c2[0])**2 + abs(c1[1] - c2[1])**2)
        if dist < closest:
            closest = dist
            targetKey = key
    return targetKey

def main():
    global sdk

    sdk = CueSdk()
    connected = sdk.connect()
    
    if not connected:
        err = sdk.get_last_error()
        print("Handshake failed: %s" % err)
        return

    colors = get_available_leds()

    # I couldn't be bothered making this play on all devices because I only have 1 anyway, but it shouldn't be too hard to implement
    firstDevice = colors[0]
    
    keyList = []
    for c in firstDevice:
        keyList.append([c, firstDevice[c]])

    y = []
    x = []
    for c in keyList:
        x.append(c[1][0])
        y.append(c[1][1])
    
    # Normalize and get min/max
    normY = (np.max(y) - np.min(y))
    normX = (np.max(x) - np.min(x))
    yMin = np.min(y)
    xMin = np.min(x)

    # Make sure the keyvals X:Y are set to 24:6 (just because the keyboard has basically 6 rows and 24 keys as width)
    # Change this as needed.
    for c in keyList:
        c[1] = ((c[1][0] - xMin)/normX * 24, (c[1][1] - yMin)/normY * 6)

    # Reset every key to black, because we might not write to all keys, and it will throw an error if a key doesnt have rgb value
    for key in firstDevice:
        firstDevice[key] = (0, 0, 0)

    # Lets just map all the keys right now so we can skip checking the distance every frame
    keymap = []
    for y in range(6):
        keymap.append([])
        for x in range(0, 24):
            # We add 1 to y here, because apparently that makes the top row work properly.
            key = getClosestPoint((x, y+1), keyList)
            keymap[y].append(key)

    # Use mss to capture screen
    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

        while "Screen capturing":
            # Get raw pixels from the screen, save it to a Numpy array
            image = np.array(sct.grab(monitor))
            image = Image.fromarray(image)
            image = scaleImage(image)

            # Change these values as you wish, they are there to enhance colours etc. to make it look nice on the keyboard
            # image = ImageEnhance.Brightness(image).enhance(3.0)
            image = ImageEnhance.Color(image).enhance(3.0)
            image = ImageEnhance.Contrast(image).enhance(2.0)
            
            image = np.asarray(image)

            for y in range(len(image)):
                for x in range(len(image[y])):
                    key = keymap[y][x]
                    firstDevice[key[0]] = (int(image[y,x,2]), int(image[y,x,1]), int(image[y,x,0]))

            sdk.set_led_colors_buffer_by_device_index(0, firstDevice)
            sdk.set_led_colors_flush_buffer()

main()
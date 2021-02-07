# cue-screen-mirror

Another simple and quite useless project I made because why not.
It uses cuesdk to play a video on your keyboard (or whatever device that supports cue, hopefully).  
It's only been tested on a K95 keyboard, [video here](https://youtu.be/zSJajImokt8), so I don't know how well it will run on other devices.

### Requirements

This program requires python>=3.7 (It was tested on 3.8.6).  
The modules required are:
* [cuesdk](https://pypi.org/project/cuesdk/)
* [numpy](https://pypi.org/project/numpy/)
* [Pillow](https://pypi.org/project/Pillow/)
* [mss](https://pypi.org/project/mss/)

These will be installed through the requirement.txt file.

### Install

Clone repo and install modules.
```
git clone https://github.com/Maharaghi/cue-screen-mirror.git
cd cue-screen-mirror
python -m pip install -r requirements.txt
```

Run the program with  
```
python main.py
```

Enjoy your monitor being mirrored to your really low resolution RGB keyboard  

P.S
If you want to change some settings you can modify `main.py` to fit your needs.  
The line numbers may have changed, but it's a small program so it won't be hard to find.
```
# Change the 24 and 6 to your desired X and Y values respectively.
[LINE 68]
for c in keyList:
  c[1] = ((c[1][0] - xMin)/normX * 24, (c[1][1] - yMin)/normY * 6)

# If you want to change the resolution change this too
[LINE 17]
def scaleImage(img):
  return img.resize((24, 6), resample=Image.ANTIALIAS)
                     ^   ^
# And also the 6 and 24 in this
[LINE 77]
for y in range(0, 6):
  keymap.append([])
  for x in range(0, 24):
    ...
---------------

# Change this to your screen settings
[LINE 87]
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

---------------
# Change the value or comment/uncomment these lines to changes the image's respective properties.
# You can also change the order of these if you need to.
[LINE 96]
image = ImageEnhance.Brightness(image).enhance(3.0)
image = ImageEnhance.Color(image).enhance(3.0)
image = ImageEnhance.Contrast(image).enhance(2.0)
```

import urllib
import praw
import requests
import re
import os
import shutil
import time
import socket
from PIL import Image

socket.setdefaulttimeout(10)

min_width = 1920
max_width = 3840
min_height = 1080
max_height = 2160
# 16:9 is 1.33
landscape_only = True

subreddit_to_search = (
    "ultrahdwallpapers"
    "+wallpapers"
    "+wallpaper"
    "+EarthPorn"
    "+ExposurePorn"
    "+ImaginaryLandscapes"
    "+LightGraffiti"
    "+SkyPorn"
    "+futureporn"
    "+lightpainting"
)
parent_dir = "C:\\Users\\olive\\source\\repos\\redditwallpaperspython"
photo_dir = "photos"
path = os.path.join(parent_dir, photo_dir)


def reset_photo_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        time.sleep(2)
    if not os.path.isdir(path):
        os.mkdir(path)
        time.sleep(2)


reset_photo_dir(path)

r = praw.Reddit(
    client_id="08tIozblDDVafw",
    client_secret="YB73i6J6Ezpiey5O9e69PZ11Eie-Ow",
    user_agent="redditwallpapers"
)


subreddit = r.subreddit(subreddit_to_search)
count = 0
image_type = ""

# Iterate through top submissions
for submission in subreddit.hot(limit=None):

    # Get the link of the submission
    url = str(submission.url)

    # Check if the link is an image
    if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
        if url.endswith("jpg"):
            image_type = ".jpg"
        elif url.endswith("jpeg"):
            image_type = ".jpeg"
        elif url.endswith("png"):
            image_type = ".png"

        # Retrieve the image and save it in current folder
        title = f"image{count}{image_type}"
        file_name = os.path.join(path, title)
        try:
            download = urllib.request.urlretrieve(url, file_name)
            image = Image.open(download[0])
            width, height = image.size
            image.close()
            if landscape_only:
                preferred = (
                    float(width) / height >= 1
                    and width >= min_width
                    and height >= min_height
                    and height <= max_height
                    and width <= max_width
                )
            else:
                preferred = (
                    width >= min_width
                    and height >= min_height
                    and height <= max_height
                    and width <= max_width
                )

            skip_msg = "" if preferred else "Removing, bad size"
            if (preferred):
                count += 1
            else:
                os.remove(file_name)

            print(title, width, height, skip_msg)

        except Exception as e:
            print(e)

        # Stop once you have x images
        if count == 10:
            break

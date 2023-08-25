import requests 
import uuid
import os 
from dotenv import load_dotenv
import time
import random

def create_img_dir():
    if (not os.path.exists(f'images/{os.getenv("IMG_DIR")}')):
        os.makedirs(f'images/{os.getenv("IMG_DIR")}')

def download_image(url):
    try:
        #print(f"requesting {url}...")
        img_data = requests.get(url).content
        time.sleep(random.randint(3, 6))
        img_filename = f'images/{os.getenv("IMG_DIR")}/{uuid.uuid4()}.jpg'
        
        
        with open(img_filename, "wb") as handler:
            handler.write(img_data)
            #print(f"url successfully downloaded")
            return img_filename
    except Exception as e:
        #print(f'error: {url} not downloaded')
        return ""

load_dotenv()
create_img_dir()


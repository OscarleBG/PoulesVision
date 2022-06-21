import os
from shutil import copy
from tqdm import tqdm
from sys import path
path.append('../old/image_collection/')
from image_collection.utils import try_mkdir

KEPT_NB = 200
OUTPUT = "latest"
IMAGE_COLLECTION_PATH = "captured_images"

try_mkdir(OUTPUT)

kept_images = os.listdir(IMAGE_COLLECTION_PATH)[-KEPT_NB:]
for im in tqdm(kept_images,desc='copying kept images'):
    src = os.path.join(IMAGE_COLLECTION_PATH,im)
    copy(src,OUTPUT)

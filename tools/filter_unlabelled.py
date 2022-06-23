"""
filters images that haven't been labelled
"""
import os, sys, shutil

from sys import path

path.append("../old/image_collection/")
from image_collection.utils import try_mkdir

path = os.path.join("/", "" if not any(sys.argv) else sys.argv[0])

files = os.listdir(path)
images = [f[:-4] for f in files if f.endswith(".png")]
labels = [f[:-4] for f in files if f.endswith(".xml")]

to_be_removed = [f + ".png" for f in images if f not in labels]

if input(
    f"From the {len(images)} images, {len(images) - len(to_be_removed)} will be kept. Continue? (Y/n)"
) not in ["n", "N"]:
    save_folder = os.path.join(path, "unlabelled")
    try_mkdir(save_folder)
    for f in to_be_removed:
        shutil.move(os.path.join(path, f), save_folder)

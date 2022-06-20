"""
Keeps only different enough images from a specified directory
"""

import os
import cv2
from numpy import mean
from shutil import copy
from tqdm import tqdm

from sys import path
path.append('../')
from image_collection.utils import try_mkdir



IMAGE_COLLECTION_PATH = './'
FILTERED_IMAGES_PATH = os.path.join(IMAGE_COLLECTION_PATH,'filtered')

#lower threshold <=> keep more images
DIFFERENCE_THRESHOLD = 35


def main():
    #create output dir if not already exists
    try_mkdir(FILTERED_IMAGES_PATH)

    #image list: dictionary of filename:str, cv2 images
    image_list = dict([(filename,cv2.imread(os.path.join(IMAGE_COLLECTION_PATH,filename))) for filename in tqdm(os.listdir(IMAGE_COLLECTION_PATH),desc='loading images')])
    kept_images = []

    for filename,image in tqdm(image_list.items(),desc='comparing images'):
        for filename2 in reversed(kept_images):
            image2 = image_list[filename2]
            if image_diff_evaluate(image,image2) < DIFFERENCE_THRESHOLD:
                break
        else:
            kept_images.append(filename)

    if input(f'from the {len(image_list)} images, {len(kept_images)} were filtered. Continue? (Y/n)') not in ['n','N']:
        for file in tqdm(kept_images,desc = 'copying filtered images'):
            src = os.path.join(IMAGE_COLLECTION_PATH, file)
            dst = os.path.join(FILTERED_IMAGES_PATH,file)
            copy(src,dst)

def image_diff_evaluate(img1, img2):
    if img1 is None or img2 is None:
        return 0
    if img1.shape != img2.shape:
        #in case two images have different shape, its like they are totally different
        return 99999
    return mean(cv2.absdiff(img1,img2))


if __name__ == '__main__':
    main()

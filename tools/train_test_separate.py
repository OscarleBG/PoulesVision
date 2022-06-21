import os
from random import shuffle
from shutil import move

TRAIN_PERCENT = 0.8


files = os.listdir('.')
files = [f[-4] for f in files if f.endswith('.png')]
shuffle(files)

train_files = files[:int(len(files) * TRAIN_PERCENT)]
test_files = files[int(len(files) * TRAIN_PERCENT):]

os.mkdir('train')
os.mkdir('test')

for f in train_files:
    move(f, 'train')

for f in test_files:
    move(f, 'test')
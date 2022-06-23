import os
from random import shuffle
from shutil import move

TRAIN_PERCENT = 0.8

def try_mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

files = os.listdir('.')
files = [f[:-4] for f in files if f.endswith('.png')]
shuffle(files)

train_files = files[:int(len(files) * TRAIN_PERCENT)]
test_files = files[int(len(files) * TRAIN_PERCENT):]

try_mkdir('train',)
try_mkdir('test')

for f in train_files:
    move(f+'.png', 'train')
    move(f+'.xml', 'train')

for f in test_files:
    move(f+'.png', 'test')
    move(f+'.xml', 'test')
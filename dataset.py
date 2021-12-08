import os
import numpy as np
import cv2
import logging
import random

from pathlib import Path
from classes import BBoxData
from tqdm import tqdm

img_types = ['.jpg', '.png']


def load_labels(src: Path) -> np.ndarray:
    txt_src = src[:-4] + '.txt'
    assert os.path.isfile(txt_src), f'File not exists: {txt_src}'
    """The file exists, loading labels"""
    with open(txt_src) as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        lines[i] = line.strip()
    """Store data in arrays"""
    labels = np.ndarray((len(lines), 5), dtype=float)
    for i, line in enumerate(lines):
        labels[i] = line.split(' ')

    return labels


"""Create a BBox class instance"""
def load_image_and_label(src_img: Path) -> BBoxData:
    img = cv2.imread(src_img, cv2.IMREAD_UNCHANGED)
    labels = load_labels(src_img)
    img_name = src_img.split('\\')[-1]

    return BBoxData(img, img_name, labels)

    
def check_data(src: Path):
    assert os.path.isdir(src), f"Folder not exists -> {src}"
    data = os.listdir(src)
    
    """Specifing the content of a folder"""
    img_files, txt_files, other_files = [], [], []
    for ele in data:
        if ele[-4:] in img_types: img_files.append(ele[:-4])
        elif ele[-4:] == '.txt': txt_files.append(ele[:-4])
        else: other_files.append(ele)

    """Chechking the dataset's image-txt datapairs"""
    dif_list = list(set(img_files) - set(txt_files)) + list(set(txt_files) - set(img_files))

    """Logging"""
    logging.info(f"{len(img_files)} images, {len(txt_files)} .txts and {len(other_files)} other files found!")
    if dif_list: logging.error(f"image or .txt file without pair: {dif_list}")
    logging.info(f"Other files, folders: {other_files}")
    assert not dif_list, "Problem with data pairs, see the [ERROR] above"


def set_new_img_size(img, max_img_size: int, w: int, h: int ) -> np.ndarray:
    ratio = w / h
    if w > h:
        new_w = max_img_size
        new_h = round(max_img_size * ratio)
    elif w < h:
        new_w = round(max_img_size * ratio)
        new_h = max_img_size
    elif w == h:
        new_w = new_h = max_img_size

    new_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    return new_img


"""Splitting data into train, valid, test, and saving the 3 .txts"""
def create_dataset_txts(src: Path, dest: Path, ratio: list[int]):
    assert sum(ratio) == 100, 'The sum of the data-split ratio is not 100'
    check_data(src)
    assert os.path.isdir(dest), f"Destination folder not exists {dest}"

    img_list = [file for file in os.listdir(src) if file[-4:] in img_types]
    
    """Giving the data random order"""
    random.shuffle(img_list)
    l = len(img_list) / 100
    
    """Splitting data first x % train, mid x % valid and the remaining test"""
    train_data = img_list[:int(l * ratio[0])]
    valid_data = img_list[int(l * ratio[0]) : int(l * ratio[0]) + int(l * ratio[1])]
    test_data = img_list[int(l * ratio[0]) + int(l * ratio[1]):]
    
    """Creating the .txts"""
    write_coco_to_file(src, os.path.join(dest, 'train.txt'), train_data)
    write_coco_to_file(src, os.path.join(dest, 'valid.txt'), valid_data)
    write_coco_to_file(src, os.path.join(dest, 'test.txt'), test_data)

    logging.info(f"Dataset .txts created at {dest}\n\t\t    data count --> Train: {len(train_data)}, Valid: {len(valid_data)}, Test: {len(test_data)}\n")


def write_coco_to_file(src: Path, dest: Path, data: list) -> None:
    with open(dest, 'w') as f:
        for ele in data:
            f.write(f"{os.path.join(src, ele)}\n{os.path.join(src, ele.split('.')[0])}.txt\n")
# Need RAM checker to be added
# Illegal characters for folders and file naming to be done
# < (less than)
# > (greater than)
# : (colon)
# " (double quote)
# / (forward slash)
# \ (backslash)
# | (vertical bar or pipe)
# ? (question mark)
# * (asterisk)

import time
from typing import List
from PIL import Image
import cv2
import imutils
import math
import numpy as np
import imagehash as hsh
import ntpath
from sys import argv
import os
import csv
import shutil  # to remove folder recursively


# Timer of the script start
start_time = time.monotonic()

# Get always 1st arguments (path)
root_path = argv[1]


# Extract file name and file path   // not in use
def path_leaf(any_path: str) -> str:
    head, tail = ntpath.split(any_path)
    return tail


def split_file_name(filename):
    split_tup = os.path.splitext(filename)  # split file name and extension
    file_name = split_tup[0]
    file_extension = split_tup[1]
    return file_name, file_extension


# DEBUG root_path = '/Users/alex/Python/PycharmProjects/SearchInsideVideoFiles/'
video_source_path = 'VideoSourceFiles/'
img_root_path = root_path + '/jpg/'


def make_dir(dir_path: str) -> str:
    print('DEBUG', dir_path)
    extracted_dir_name = path_leaf(dir_path)
    print('DEBUG', extracted_dir_name)
    if not os.path.exists(dir_path):
        try:
            os.mkdir(dir_path)
        except OSError:
            print(f'can\'t create {extracted_dir_name} directory, path: {dir_path}')
            pass


make_dir(img_root_path)  # create JPG directory


# Returns tuple of directories (to save RAM)
# def dirs_by_path_as_tup(dir_path: str) -> tuple:
#     return_value = ()
#     for (root, dirs, files) in os.walk(dir_path):
#         for _dir in sorted(dirs):
#             if _dir[0] == '.':
#                 dirs.pop(dirs.index(_dir))
#         return_value += tuple(dirs)
#     return return_value


# print('DIRECTORIES: ', dirs_by_path_as_tup(img_root_path))


# Returns sorted list of files
def files_list_by_path_filter_by_ext(file_path: str, ext: str) -> list:
    list_of_files_by_ext = []
    for (root, dirs, files) in os.walk(file_path):
        for _file in files:
            f_name, f_ext = split_file_name(_file)  # extract file extension
            if f_ext == ext:
                list_of_files_by_ext.append(_file)  # create list of files

    return sorted(list_of_files_by_ext)


# DEBUG print('VIDEO_FILES :', files_list_by_path_filter_by_ext(video_source_path, '.mp4'))
# DEBUG print('IMAGE_FILES :', files_list_by_path_filter_by_ext(img_root_path, '.jpg'))


# Extract frames as JPG and distribute them in folders named as Video files
def extract_frames_and_distribute(video_files_list):
    jpg_folders_list = []
    for video_file in video_files_list:
        f_name, f_ext = split_file_name(video_file)
        # split_tup = os.path.splitext(video_file)  # split file name and extension
        # DEBUG print(split_tup[0])  # take file name, for ext use [1]
        # f_name = split_tup[0]  # use file name for category naming
        jpg_folders_list.append(f_name)
        folder_path = f'{root_path}/jpg/{f_name}'
        if not os.path.exists(folder_path):
            make_dir(folder_path)
            cap = cv2.VideoCapture(
                # TEST1 video_source_path + video_file)  # cap = cv2.VideoCapture(os.path.abspath(video_file))
                root_path + '/' + video_file)  # cap = cv2.VideoCapture(os.path.abspath(video_file))

            # Read video parameters
            # frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
            total_frames_per_file = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # checks whether frames were extracted
            # while cap.isOpened():
            success, image = cap.read()
            count = 0
            while success:
                jpg_file_path = f'{folder_path}/{total_frames_per_file}frames_{str(count).zfill(6)}.jpg'
                cv2.imwrite(jpg_file_path, image)
                success, image = cap.read()
                # DEBUG print('Read a new frame: ', success)
                count += 1

                # Read image and define high and width
                img = cv2.imread(jpg_file_path)
                h, w = int(img.shape[0]) // 3, int(img.shape[1] // 3)   # 1/3 of original size
                resized_size = (w, h)
                resized_img = cv2.resize(img, resized_size, interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(jpg_file_path,
                            cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)[int(h * 0.333):int(h * 0.666),
                            0:w])  # Write & convert to grayscale, extract middle part of the image. Speed up...

            # break
            # cv2.destroyAllWindows()
            # cap.release()
        else:
            try:
                # Delete folder recursively
                shutil.rmtree(folder_path)
            except:
                print(f'Error. Can\'t delete dolder {folder_path}')

    return jpg_folders_list


# Save hashes per video
def build_hashes_list_file(img_folders_list: str) -> str:  # write hashes into CSV file
    for folder in img_folders_list:
        for (root, dirs, files) in os.walk(img_root_path + folder):
            header = ['VideoFileName', 'Hashes']   # building csv header
            with open(root + '/' + folder + '.csv', 'a', encoding='UTF8') as hashes_per_video_file:
                writer = csv.writer(hashes_per_video_file)
                # write the header
                writer.writerow(header)
                for jpg_file in files:
                    img_object = cv2.imread(img_root_path + folder + '/' + jpg_file)
                    image_pil = Image.fromarray(img_object)
                    hshperceptual = hsh.phash(image_pil, 10)  # number of hash characters, need to check

                    csv_data_row = [folder, str(hshperceptual)]  # building csv row
                    writer.writerow(csv_data_row)  # write row

    return img_folders_list


jpg_folder = extract_frames_and_distribute(files_list_by_path_filter_by_ext(root_path, '.mp4'))  # list of all JPG
# folders
build_hashes_list_file(jpg_folder)  # write hashes in file

csv_hash_files: list[str] = []  # prepare a placeholder for the function: build_hashes_list


# Build list of CSV files, which contain hashes to go through them
def build_hashes_list(img_path: str) -> list:
    for root, dirs, files in os.walk(img_path):
        for file in files:
            if file.endswith(".csv"):
                # print('DEBUG: ', os.path.join(root, file))
                csv_hash_files.append(os.path.join(root, file))  # build path to TXT in order to read it
    return csv_hash_files


build_hashes_list(img_root_path)

result_file = img_root_path + 'result.csv'


# Concatenate all CSV files with hashes
def concatenate_hash_files(result_csv_path: str, hash_csv_list: list) -> str:
    with open(result_csv_path, 'w') as combined_file:
        for csv_file in hash_csv_list:
            with open(csv_file) as source_file:
                combined_file.write(source_file.read())


concatenate_hash_files(result_file, build_hashes_list(img_root_path))


# Compare hashes for matches
def compare_files_by_group(total_num_frames, hash_list):
    chunks = (total_num_frames - 1) // 5 + 1
    for i in range(chunks):
        jpg_batch = hash_list[i * 50:(i + 1) * 50]
    return jpg_batch



# im_pil = Image.fromarray(
#     img)  # Takes the array object as the input and returns the image object made from the array object.
#
# hshperceptual = hsh.phash(im_pil, 20)
# # print('hshperceptual :' + str(hshperceptual))
# hashes_per_batch.append(hshperceptual)  # Tuple concatenation
# full_list_of_taga = '\n'.join(map(str, hashes_per_batch))


# import os
# import csv
# from csv import DictReader
# import re
# import glob
#
#
# source_path = '/Users/alex/PycharmProjects/pythonProject2/VideoSearch/jpg'
# frames_for_one_video = []
#
# for (root, dirs, file) in os.walk(source_path):
#     for _dir in dirs:
#         source_path.find()
#
# # with open(source_path + '/List of Files.csv', 'r') as video_file_list:
# #     csv_dict_reader = DictReader(video_file_list)
#
#     # for row in csv_dict_reader:
#     #     video_file_name_csv = list(row.items())[1][1]
# jpg_full_list = os.listdir('/Users/alex/PycharmProjects/pythonProject2/VideoSearch/jpg')
# for filename in jpg_full_list:
#     extract_name = re.sub(r"\.mp4\_\d{1,10}\.jpg$", "", filename)


# i = 0
# if jpg_full_list[i] == jpg_full_list[i+1]:
#     print(jpg_full_list[i])
#     print(jpg_full_list[i + 1])
#     frames_for_one_video.append()
#     print(frames_for_one_video)
#     i += 1
# else:
#     pass


# for row in csv_dict_reader:
# for root, dirs, files in os.walk('/Users/alex/PycharmProjects/pythonProject2/VideoSearch/VideoSourceFiles/',
#                                  topdown=False):
#     for name in files:
#         print(list(row.items())[name])
# print(type(name))
# for row in csv_dict_reader:
#     # print(row)
#     i = 1
#     # print(type(list(row.items())[1][i]))
#     print(list(row.items())[1][1])
#     if name <= list(row.items())[1][1]:
#         i += 1
#         # print(os.path.join(root, name))
#
#         print(name, i)
# import os
#
# jpg_path = './jpg/'
# for (root, dirs, file) in os.walk(jpg_path):
#     for f in file:


# import cv2
#
# count = 0
# cap = cv2.VideoCapture("/Users/alex/PycharmProjects/pythonProject2/VideoSearch/VideoSourceFiles"
#                        "/sample_1280x720_surfing_with_audio.mp4")
#
# print("Showing frames...")
# c = 1
# while cap.isOpened():
#     filepath = f'/Users/alex/PycharmProjects/pythonProject2/VideoSearch/jpg/{count}.jpg'
#     grabbed, frame = cap.read()
#     if not grabbed:
#         break
#     for a in range(60, 70):
#         if c % a == 0:
#             frameId = cap.get(1)
#             print(frameId)
#             cv2.imwrite(filepath, frame)
#
#
#     else:
#         pass
#
#     c += 1
#     count += 1
# cap.release()

# import cv2
# import os
# source_path = '/Users/alex/PycharmProjects/pythonProject2/VideoSearch/VideoSourceFiles/'
#
# source_video_files = os.listdir(source_path)
#
# for (root, dirs, file) in os.walk(source_path):
#     for f in file:
#         print(f)
#         if ".mp4" in file:
#             print(file)
#             cap = cv2.VideoCapture(source_path)  # capturing the video from the given path
#             frameRate = cap.get(5)  # frame rate


# import tkinter as tk
# from tkinter import filedialog
# import os
# import csv
#
# root = tk.Tk()
# root.withdraw()
# source_path = filedialog.askdirectory()
#
# source_video_files = os.listdir(source_path)
# print(source_video_files)
#
# file_num = 0
# with open(source_path + '/List of Files.csv', 'w') as result:
#     writer = csv.writer(result, delimiter=",")
#     writer.writerow(('Number', 'FileName'))
#     for row in source_video_files:
#         if '.jpg' in row:
#             file_num += 1
#             row = str(file_num) + ',' + row
#             columns = [c.strip() for c in row.strip(', ').split(',')]
#             writer.writerow(columns)
#         elif '.mp4' in row:
#             file_num += 1
#             row = str(file_num) + ',' + row
#             columns = [c.strip() for c in row.strip(', ').split(',')]
#             writer.writerow(columns)

# import itertools
#
# hashes = ([1, 2, 3], [3, 4, 5], [6, 1, 7])
# length = len(hashes)
#
# i = -1
# for list_ in itertools.combinations(hashes, length):
#     list_extracted = hashes[i + 1]
#     j = -1
#     for hashes in list_extracted:
#         print(list_extracted[j+1])
#         j += 1
#     i += 1

# print(hashes_per_video[0][i+1])
# hash_difference = hashes_per_video[0][i] - hashes_per_video[0][i+1]
# i += 1
# if hash_difference == 0:
#     print(hash_difference)

print(f'SCRIPT TOOK {time.monotonic() - start_time}')


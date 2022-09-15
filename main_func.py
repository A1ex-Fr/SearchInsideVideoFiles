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
from typing import List, Tuple
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

from threading import Thread
from queue import Queue

# Timer of the script start
start_time = time.monotonic()

# Get always 1st arguments (path)
root_path = argv[1]


# Extract file name and file path   // not in use
def path_leaf(any_path: str) -> tuple[str, str]:
    head, tail = ntpath.split(any_path)
    return head, tail


def split_file_name(filename):
    split_tup = os.path.splitext(filename)  # split file name and extension
    file_name = split_tup[0]
    file_extension = split_tup[1]
    return file_name, file_extension


# DEBUG root_path = '/Users/alex/Python/PycharmProjects/SearchInsideVideoFiles/'
video_source_path = 'VideoSourceFiles/'
img_root_path = root_path + '/jpg/'


def get_absolut_file_path(file):
    absolute_file_path = os.path.abspath(file)
    return absolute_file_path


def make_dir(dir_path: str) -> str:
    # print('DEBUG', dir_path)
    extracted_dir_name = path_leaf(dir_path)
    # print('DEBUG', extracted_dir_name)
    if not os.path.exists(dir_path):
        try:
            os.mkdir(dir_path)
        except OSError:
            print(f'can\'t create {extracted_dir_name} directory, path: {dir_path}')
    return dir_path


make_dir(img_root_path)  # create JPG directory


# print(f'Make_dir *Function {time.monotonic() - start_time}')

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


mp4_file_list = files_list_by_path_filter_by_ext(root_path, '.mp4')


# print(f'Get file list *Function {time.monotonic() - start_time}')

# DEBUG print('VIDEO_FILES :', files_list_by_path_filter_by_ext(video_source_path, '.mp4'))
# DEBUG print('IMAGE_FILES :', files_list_by_path_filter_by_ext(img_root_path, '.jpg'))
def create_jpg_folder(folder_path):
    os.mkdir(folder_path)
    return folder_path


# Extract frames as JPG and distribute them in folders named as Video files
def extract_frames(video_files_list: list) -> list:
    jpg_folders_list = []

    for mp4_file in video_files_list:
        f_name, f_ext = split_file_name(mp4_file)
        # f_path = path_leaf(mp4_file_path)  # VideoSourceFiles/, //Users../SearchInsideVideoFiles/VideoSourceFiles/jpg/
        mp4_file_path = root_path + '/' + mp4_file  # full file path for Capturing
        folder_path = f'{img_root_path}{f_name}'  # TO BE DELETED TEMP!!!!!!!!!!!
        print('folder_path',folder_path)
        if not os.path.exists(folder_path):  # TO BE DELETED TEMP!!!!!!!!!!!
            jpg_folder = create_jpg_folder(folder_path)  # function create a folder for JPGs
            cap = cv2.VideoCapture(mp4_file_path)
            total_frames_per_file = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            success, jpg = cap.read()
            count = 0
            while success:
                jpg = imutils.resize(jpg, width=480)
                jpg = cv2.cvtColor(jpg, cv2.COLOR_BGR2GRAY)[90:180, 0:480]
                jpg = np.dstack([jpg, jpg, jpg])
                jpg_file_path = f'{jpg_folder}/{f_name}_{str(count).zfill(6)}.jpg'
                cv2.imwrite(jpg_file_path, jpg)
                success, jpg = cap.read()
                print('Read a new frame: ', success)
                count += 1
                jpg_folders_list.append(jpg)
                # print('JPGs', jpg_folders_list)
        else:
            try:  # TO BE DELETED TEMP!!!!!!!!!!!
                # Delete folder recursively TO BE DELETED TEMP!!!!!!!!!!!
                shutil.rmtree(folder_path)  # TO BE DELETED TEMP!!!!!!!!!!!
            except:  # TO BE DELETED TEMP!!!!!!!!!!!
                print(f'Error. Can\'t delete folder {folder_path}')  # TO BE DELETED TEMP!!!!!!!!!!!
    return jpg_folders_list


extract_frames(mp4_file_list)


def distribute():
    pass
    return jpg_folders_list


#
#
# jpg_folders = extract_frames_and_distribute(mp4_file_list)  # list of all JPG folders
# print(f'Extract frames *Function {time.monotonic() - start_time}')
#
#
# # Save hashes per video
# def build_hashes_list_file(img_folders_list: str) -> str:  # write hashes into CSV file
#     for folder in img_folders_list:
#         for (root, dirs, files) in os.walk(img_root_path + folder):
#             header = ['VideoFileName', 'Hashes']   # building csv header
#             with open(root + '/' + folder + '.csv', 'a', encoding='UTF8') as hashes_per_video_file:
#                 writer = csv.writer(hashes_per_video_file)
#                 # write the header
#                 writer.writerow(header)
#                 for jpg_file in files:
#                     img_object = cv2.imread(img_root_path + folder + '/' + jpg_file)
#                     image_pil = Image.fromarray(img_object)
#                     hshperceptual = hsh.phash(image_pil, 10)  # number of hash characters, need to check
#
#                     csv_data_row = [folder, str(hshperceptual)]  # building csv row
#                     writer.writerow(csv_data_row)  # write row
#
#     return img_folders_list
#
#
#
# build_hashes_list_file(jpg_folders)  # write hashes in file
#
# csv_hash_files: list[str] = []  # prepare a placeholder for the function: build_hashes_list
#
#
# # Build list of CSV files, which contain hashes to go through them
# def build_list_of_csvs(img_path: str) -> list:
#     for root, dirs, files in os.walk(img_path):
#         for file in files:
#             if file.endswith(".csv"):
#                 # print('DEBUG: ', os.path.join(root, file))
#                 csv_hash_files.append(os.path.join(root, file))  # build path to TXT in order to read it
#     return csv_hash_files
#
#
# hashes_list = build_list_of_csvs(img_root_path)
# print(f'Build list of CSV *Function {time.monotonic() - start_time}')
# result_file = img_root_path + 'result.csv'
#
#
# # Concatenate all CSV files with hashes
# def concatenate_hash_files(result_csv_path: str, hash_csv_list: list) -> str:
#     with open(result_csv_path, 'w') as combined_file:
#         for csv_file in hash_csv_list:
#             with open(csv_file) as source_file:
#                 combined_file.write(source_file.read())
#
#
# concatenate_hash_files(result_file, hashes_list)
# print(f'Concatenate CSV *Function {time.monotonic() - start_time}')

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------


# Compare hashes for matches
# def compare_files_by_chunk(num_frames: int, hash_list: list) -> list:
#     chunks = (num_frames - 1) // 5 + 1
#     for i in range(chunks):
#         pass
#         # jpg_batch = hash_list[i * 50:(i + 1) * 50]
#     return jpg_batch


# print(compare_files_by_chunk(!!!!total_number_of_frames!!!!!, concatenate_hash_files))
# print(f'Compare files by chunk *Function {time.monotonic() - start_time}')
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

print(f'TOTAL SCRIPT TOOK {time.monotonic() - start_time}')

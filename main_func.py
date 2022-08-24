from PIL import Image
import cv2
import imutils
import math
import numpy as np
import imagehash as hsh
import timeit
import ntpath
from sys import argv
import os
import csv

# Timer of the script start
start_time = timeit.default_timer()

hashes_per_video = ()  # List of files and hashes
result_hashes = ()  # Result list of hashes lists

root_path = '/Users/alex/PycharmProjects/pythonProject2/VideoSearch/'
video_source_path = '/Users/alex/PycharmProjects/pythonProject2/VideoSearch/VideoSourceFiles'
img_root_path = '/Users/alex/PycharmProjects/pythonProject2/VideoSearch/jpg'


# Arguments
def read_source_folder(argument):
    return argument[1]


# Extract file name and file path
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail


# Returnes
def dirs_by_path_as_tup(dir_path):
    return_value = ()
    for (root, dirs, files) in os.walk(dir_path):
        for _dir in sorted(dirs):
            if _dir[0] == '.':
                dirs.pop(dirs.index(_dir))
        return_value += tuple(dirs)
    return return_value


print('DIRECTORIES: ', dirs_by_path_as_tup(img_root_path))


def files_by_path_as_tup(file_path):
    return_value = ()
    for (root, dirs, files) in os.walk(file_path):
        for _file in files:
            if _file[0] == '.' or _file[-1] != '4':
                files.pop(files.index(_file))

        return_value += tuple(files)
    return sorted(return_value)


print('VIDEO_FILES :', files_by_path_as_tup(video_source_path))

print('IMG_FILES :', files_by_path_as_tup(img_root_path + '/city'))





# scan_path_video(img_source_path)


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

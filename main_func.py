import time
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
print(root_path)
# DEBUG root_path = '/Users/alex/Python/PycharmProjects/SearchInsideVideoFiles/'
video_source_path = 'VideoSourceFiles/'
img_root_path = root_path + '/jpg/'
try:
    os.mkdir(img_root_path)
except OSError:
    print(f'cannot create JPG, it might already exists in {root_path}')
    pass


# Extract file name and file path
def path_leaf(any_path):
    head, tail = ntpath.split(any_path)
    return tail


# Returns list of directories
def dirs_by_path_as_tup(dir_path):
    return_value = ()
    for (root, dirs, files) in os.walk(dir_path):
        for _dir in sorted(dirs):
            if _dir[0] == '.':
                dirs.pop(dirs.index(_dir))
        return_value += tuple(dirs)
    return return_value


print('DIRECTORIES: ', dirs_by_path_as_tup(img_root_path))


# Returns sorted list of files
def get_files_by_path(file_path, ext):
    list_of_files_by_ext = []
    for (root, dirs, files) in os.walk(file_path):
        for _file in files:
            split_tup = os.path.splitext(_file)
            if split_tup[1] == ext:
                list_of_files_by_ext.append(_file)

    return sorted(list_of_files_by_ext)


# print('VIDEO_FILES :', get_files_by_path(video_source_path, '.mp4'))
# print('IMAGE_FILES :', get_files_by_path(img_root_path, '.jpg'))


# mp4_file_name_jpg_folder = 'N2__________'
# print(img_root_path + mp4_file_name_jpg_folder)
# print('IMG_FILES :', files_by_path_as_tup(img_root_path + mp4_file_name_jpg_folder))


# Extract frames as JPG and distribute them in folders named as Video files
def extract_frames_and_distribute(video_files_list):
    jpg_folders_list = []
    for video_file in video_files_list:
        split_tup = os.path.splitext(video_file)  # split file name and extension
        # DEBUG print(split_tup[0])  # take file name, for ext use [1]
        file_name_extracted = split_tup[0]  # use file name for category naming
        jpg_folders_list.append(file_name_extracted)
        folder_path = f'{root_path}/jpg/{file_name_extracted}'
        # frameId = 0
        if not os.path.exists(folder_path):
            try:
                os.mkdir(folder_path)
            except OSError as e:
                print("Creating folder Error: %s : %s" % (folder_path, e.strerror))
            cap = cv2.VideoCapture(
                # TEST1 video_source_path + video_file)  # cap = cv2.VideoCapture(os.path.abspath(video_file))
                root_path + '/' + video_file)  # cap = cv2.VideoCapture(os.path.abspath(video_file))

            # Read video parameters
            frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
            num_clip_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

            # checks whether frames were extracted
            # while cap.isOpened():
            success, image = cap.read()
            count = 0
            while success:
                jpg_file_path = f'{folder_path}/{count}.jpg'
                cv2.imwrite(jpg_file_path, image)
                success, image = cap.read()
                # DEBUG print('Read a new frame: ', success)
                count += 1

                # Read image and define high and width
                img = cv2.imread(jpg_file_path)
                h, w = int(img.shape[0]), int(img.shape[1]) // 3  # 1/3 of original size
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
                shutil.rmtree(folder_path)
            except:
                print(f'Error. Can\'t delete dolder {folder_path}')

    return jpg_folders_list


jpg_created_folders_by_func = extract_frames_and_distribute(get_files_by_path(root_path, '.mp4'))
print('CREATED JPG FOLDERS: ', jpg_created_folders_by_func)


# Save hashes per video
def build_hash_func(img_folders_name):  # Maybe SQLite needs to be connected to store hashes
    for folder in img_folders_name:
        for (root, dirs, files) in os.walk(img_root_path + folder):
            for jpg_file in files:
                # print('DEBUG:', jpg_file)
                # full_path_to_jpg = img_root_path + folder
                img_object = cv2.imread(img_root_path + folder + '/' + jpg_file)
                # print('IMAGE', img_object)
                image_pil = Image.fromarray(img_object)
                hshperceptual = hsh.phash(image_pil, 10)  # number of hash characters, need to check
                # print('hshperceptual :' + str(hshperceptual))
                with open(root + '/' + folder + '.txt', 'a') as hashes_list:
                    hashes_list.write('\n' + str(hshperceptual))

    return img_folders_name


build_hash_func(jpg_created_folders_by_func)
# print('build_hash_func: ', build_hash_func(jpg_created_folders_by_func))

# Compare hashes
full_jpg_categories_path = img_root_path

txt_hash_files = []
for root, dirs, files in os.walk(full_jpg_categories_path):
    for file in files:
        if file.endswith(".txt"):
            # print('DEBUG: ', os.path.join(root, file))
            txt_hash_files.append(os.path.join(root, file))
            print(txt_hash_files)
result_file = full_jpg_categories_path + 'result.txt'

with open(result_file, 'w') as outfile:
    for txt in txt_hash_files:
        with open(txt) as infile:
            outfile.write(infile.read())

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
